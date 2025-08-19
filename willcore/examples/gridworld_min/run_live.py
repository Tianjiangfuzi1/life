from willcore.impls.envs.gridworld import GridWorld
from willcore.impls.sensors.basic import BasicSensors
from willcore.impls.goals.factory_rule_based import RuleGoalFactory
from willcore.impls.planner.a_star import AStarPlanner
from willcore.impls.value.basic import BasicValue
from willcore.impls.meta.commitment import SimpleCommitment
from willcore.impls.memory.simple import SimpleMemory
from willcore.runtime.loop import RuntimeLoop
from willcore.core.types import Prefs, Mood
from willcore.ui.live_ascii import LiveAscii
from willcore.ui.cli import print_fwi_banner

def main():
    env = GridWorld()
    sensors = BasicSensors()
    goals = RuleGoalFactory()
    planner = AStarPlanner()
    value = BasicValue()
    commitment = SimpleCommitment()
    memory = SimpleMemory()
    prefs = Prefs()
    mood = Mood()

    # enable live view via on_step callback
    viewer = LiveAscii(sleep_sec=0.05, clear=True)
    memory['on_step'] = lambda ctx: viewer.render(ctx['env'], ctx['fwi'], ctx['step'], ctx['energy'], ctx['goal'])

    loop = RuntimeLoop(env, sensors, goals, planner, value, commitment,
                       prefs, mood, memory,
                       max_steps=200, t_min=6, switching_cost=0.8,
                       log_dir="data/logs")
    print_fwi_banner()
    stats = loop.run(seed=0)
    print("Run finished:", stats)

if __name__ == "__main__":
    main()
