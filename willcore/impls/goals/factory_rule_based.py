from typing import Dict, Any, List, Tuple, Optional
import numpy as np
from willcore.core.interfaces import IGoalFactory
from willcore.core.types import Goal

def _find_cells(value, patch, origin) -> List[Tuple[int,int]]:
    ys, xs = np.where(patch == value)
    return [(int(y+origin[0]), int(x+origin[1])) for y, x in zip(ys, xs)]

def _nearest(src, targets):
    if not targets:
        return None
    sy, sx = src
    targets = sorted(targets, key=lambda p: abs(p[0]-sy) + abs(p[1]-sx))
    return targets[0]

class RuleGoalFactory(IGoalFactory):
    def propose(self, obs: Dict[str, Any], memory: Dict[str, Any]) -> List[Goal]:
        pos = obs["pos"]
        patch = obs["patch"]
        origin = obs["patch_origin"]
        discovered = obs["discovered"]

        foods = _find_cells(2, patch, origin)

        goals: List[Goal] = []

        # 1) collect nearest visible food
        nf = _nearest(pos, foods)
        if nf is not None:
            goals.append(Goal(kind="collect_food", target=nf, desc=f"Collect food at {nf}"))

        # 2) explore frontier: an undiscovered cell near discovered boundary
        undiscovered = np.argwhere(~discovered)
        if undiscovered.size > 0:
            dyx = sorted([(int(y),int(x)) for y,x in undiscovered],
                         key=lambda p: abs(p[0]-pos[0]) + abs(p[1]-pos[1]))
            goals.append(Goal(kind="explore_frontier", target=dyx[0], desc=f"Explore frontier {dyx[0]}"))

        # 3) hold if energy low
        if obs["energy"] <= 5:
            goals.append(Goal(kind="hold", target=pos, desc="Hold position (low energy)"))

        return goals
