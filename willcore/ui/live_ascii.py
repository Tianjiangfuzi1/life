import os
import time

class LiveAscii:
    """
    Very simple terminal viewer: renders env grid and a small FWI panel.
    Usage:
        viewer = LiveAscii(sleep_sec=0.05)
        memory['on_step'] = lambda ctx: viewer.render(ctx['env'], ctx['fwi'], ctx['step'], ctx['energy'], ctx['goal'])
    """
    def __init__(self, sleep_sec: float = 0.05, clear: bool = True):
        self.sleep_sec = sleep_sec
        self.clear = clear

    def render(self, env, fwi: dict, step: int, energy: int, goal: dict):
        if self.clear:
            # ANSI clear
            print("\033[2J\033[H", end="")
        print(env.render())
        print()
        print(f"Step: {step}  Energy: {energy}")
        print(f"Goal: {goal}")
        print("FWI:", ", ".join([f"{k}={v:.2f}" for k, v in fwi.items()]))
        time.sleep(self.sleep_sec)
