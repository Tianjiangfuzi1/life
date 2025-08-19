from typing import Dict, Any
import numpy as np
from willcore.core.interfaces import IValueSystem
from willcore.core.types import TrajStats, Goal, Prefs, Mood

def estimate_traj(obs: Dict[str, Any], goal: Goal, actions) -> TrajStats:
    patch = obs["patch"]
    oy, ox = obs["patch_origin"]
    pos = obs["pos"]
    H, W = obs["grid_shape"]
    stats = TrajStats()
    stats.path_len = len(actions)
    ty, tx = goal.target or pos
    if (oy <= ty < oy + patch.shape[0]) and (ox <= tx < ox + patch.shape[1]):
        if patch[ty-oy, tx-ox] == 2:
            stats.extrinsic += 10.0
        elif patch[ty-oy, tx-ox] == 3:
            stats.risk += 5.0
    discovered = obs["discovered"]
    mask = np.zeros_like(discovered, dtype=bool)
    for y in range(max(0, ty-2), min(H, ty+3)):
        for x in range(max(0, tx-2), min(W, tx+3)):
            if abs(y-ty)+abs(x-tx) <= 2:
                mask[y,x] = True
    new_cells = np.logical_and(mask, ~discovered).sum()
    stats.curiosity = float(new_cells) / float(mask.sum() or 1)
    if goal.kind == "explore_frontier":
        stats.novelty += 0.2
    stats.risk += 0.05 * stats.path_len
    return stats

class BasicValue(IValueSystem):
    def score(self, stats: TrajStats, prefs: Prefs, mood: Mood) -> float:
        return (prefs.a * stats.extrinsic +
                prefs.b * stats.curiosity +
                prefs.c * stats.empowerment +
                prefs.d * stats.novelty -
                prefs.l * stats.risk)
