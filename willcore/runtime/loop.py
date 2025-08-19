from typing import Dict, Any, Optional, List, Tuple
from willcore.core.types import Goal, Prefs, Mood, TrajStats, DecisionReason, StepLog
from willcore.impls.logger.why_logger import WhyLogger

class RuntimeLoop:
    def __init__(self, env, sensors, goal_factory, planner, value_system, commitment, prefs: Prefs, mood: Mood,
                 memory: Dict[str, Any], max_steps: int = 300, t_min: int = 6, switching_cost: float = 0.8,
                 log_dir: str = "data/logs"):
        self.env = env
        self.sensors = sensors
        self.goal_factory = goal_factory
        self.planner = planner
        self.value_system = value_system
        self.commitment = commitment
        self.prefs = prefs
        self.mood = mood
        self.memory = memory
        self.max_steps = max_steps
        self.t_min = t_min
        self.switching_cost = switching_cost
        self.current_goal: Optional[Goal] = None
        self.last_switch_step = -999999
        self.why = WhyLogger(log_dir=log_dir)
        self.intent_stable_steps = 0
        self.intent_total_switches = 0
        self.internally_generated_goals = 0

    def _evaluate_candidates(self, obs: Dict[str, Any], goals: List[Goal]):
        candidates = []
        actions_cache = []
        for g in goals:
            actions = self.planner.plan(obs, g, self.memory)
            actions_cache.append((g, actions))
        for g, actions in actions_cache:
            from willcore.impls.value.basic import estimate_traj
            stats = estimate_traj(obs, g, actions)
            score = self.value_system.score(stats, self.prefs, self.mood)
            candidates.append((g, score, stats))
        return candidates

    def _fwi(self, step_idx: int, candidates, reason: Dict[str, Any]) -> Dict[str, float]:
        self.internally_generated_goals += 1
        GA = min(1.0, self.internally_generated_goals / (step_idx + 1))
        CD = min(1.0, len(candidates) / 5.0)
        CS = min(1.0, self.intent_stable_steps / max(1, self.t_min))
        SM = 0.5
        XR = 1.0 if ("ranked" in reason and "chosen" in reason) else 0.0
        return {"GA": GA, "CD": CD, "CS": CS, "SM": SM, "XR": XR}

    def run(self, seed: Optional[int] = 0):
        obs = self.env.reset(seed=seed)
        total_reward = 0.0
        for step in range(self.max_steps):
            enc = self.sensors.encode(obs)
            goals = self.goal_factory.propose(enc, self.memory)
            if not goals:
                goals = [Goal(kind="hold", target=enc["pos"], desc="Fallback hold at current position")]
            candidates = self._evaluate_candidates(enc, goals)
            chosen, reason = self.commitment.decide(step, self.current_goal, candidates,
                                                    self.last_switch_step, self.switching_cost, self.t_min)
            if (self.current_goal is None) or (chosen.kind != self.current_goal.kind or chosen.target != self.current_goal.target):
                self.current_goal = chosen
                self.last_switch_step = step
                self.intent_total_switches += 1
                self.intent_stable_steps = 0
            else:
                self.intent_stable_steps += 1

            actions = self.planner.plan(enc, self.current_goal, self.memory)
            act = actions[0] if actions else 0
            obs, reward, done, info = self.env.step(act)
            total_reward += reward

            fwi = self._fwi(step, candidates, reason)
            log = StepLog(step=step, pos=obs["pos"], energy=obs["energy"],
                          reason=DecisionReason(candidates=[{"goal": {"kind": g.kind, "target": g.target, "desc": g.desc}, "score": float(s)} for (g,s,_) in candidates],
                                                chosen={"goal": {"kind": self.current_goal.kind, "target": self.current_goal.target, "desc": self.current_goal.desc}},
                                                switching_cost_applied=float(reason.get("switching_cost_applied", 0.0)),
                                                reeval_triggered=bool(reason.get("reeval_triggered", False))),
                          fwi=fwi)
            self.why.log({
                "step": log.step,
                "pos": log.pos,
                "energy": log.energy,
                "reason": {
                    "candidates": log.reason.candidates,
                    "chosen": log.reason.chosen,
                    "switching_cost_applied": log.reason.switching_cost_applied,
                    "reeval_triggered": log.reason.reeval_triggered
                },
                "fwi": log.fwi
            })
            on_step = self.memory.get("on_step")
            if on_step is not None:
                try:
                    on_step({
                        "env": self.env,
                        "fwi": fwi,
                        "step": step,
                        "energy": log.energy,
                        "goal": log.reason.chosen["goal"],
                    })
                except Exception as e:
                    print(f"[live_view] error: {e}")

            if done:
                break
        self.why.close()
        return {"steps": step+1, "total_reward": total_reward, "switches": self.intent_total_switches}
