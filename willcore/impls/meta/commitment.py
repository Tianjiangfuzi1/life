from typing import List, Tuple, Optional, Dict, Any
from willcore.core.interfaces import ICommitmentManager
from willcore.core.types import Goal, TrajStats

class SimpleCommitment(ICommitmentManager):
    def decide(self, step_idx: int, current_goal: Optional[Goal],
               candidates: List[Tuple[Goal, float, TrajStats]],
               last_switch_step: int,
               switching_cost: float,
               t_min: int):
        if not candidates:
            if current_goal is not None:
                reason = {
                   "ranked": [],
                   "chosen": {"kind": current_goal.kind, "target": current_goal.target, "desc": current_goal.desc},
                   "switching_cost_applied": 0.0,
                   "reeval_triggered": False,
                }
                return current_goal, reason
            # 没有 current_goal 的情况——造一个占位的 hold（target 先用 None；上层 planner 会当作 stay）
            from willcore.core.types import Goal
            fallback = Goal(kind="hold", target=None, desc="Commitment fallback hold")
            reason = {
                "ranked": [],
                "chosen": {"kind": fallback.kind, "target": fallback.target, "desc": fallback.desc},
                "switching_cost_applied": 0.0,
                "reeval_triggered": False,
            }
            return fallback, reason
        ranked = sorted(candidates, key=lambda x: x[1], reverse=True)
        best_goal, best_score, best_stats = ranked[0]

        reeval_triggered = False
        chosen = best_goal
        applied_switch_cost = 0.0
        if current_goal is not None and (step_idx - last_switch_step) < t_min:
            cur = [(g,s,st) for (g,s,st) in candidates if g.kind == current_goal.kind and g.target == current_goal.target]
            if cur:
                chosen, cur_score, _ = cur[0]
                if best_score - cur_score > switching_cost:
                    chosen = best_goal
                    applied_switch_cost = switching_cost
                    reeval_triggered = True
            else:
                chosen = best_goal
                applied_switch_cost = switching_cost
                reeval_triggered = True
        else:
            if current_goal is not None and (best_goal.kind != current_goal.kind or best_goal.target != current_goal.target):
                applied_switch_cost = switching_cost
                reeval_triggered = True

        reason = {
            "ranked": [{"goal": {"kind":g.kind, "target":g.target, "desc":g.desc}, "score": float(s)} for (g,s,_) in ranked],
            "chosen": {"kind":chosen.kind, "target":chosen.target, "desc":chosen.desc},
            "switching_cost_applied": float(applied_switch_cost),
            "reeval_triggered": bool(reeval_triggered),
        }
        return chosen, reason
