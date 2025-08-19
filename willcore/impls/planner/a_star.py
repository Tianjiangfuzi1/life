from typing import Dict, Any, List, Tuple
import heapq
import numpy as np
from willcore.core.interfaces import IPlanner
from willcore.core.types import Goal

ACTIONS = [(0,0), (-1,0), (1,0), (0,-1), (0,1)]
ACTION_IDS = {a:i for i,a in enumerate(ACTIONS)}

def _neighbors(p, shape):
    y, x = p
    H, W = shape
    cand = [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]
    return [(ny,nx) for ny,nx in cand if 0 <= ny < H and 0 <= nx < W]

def _heur(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

class AStarPlanner(IPlanner):
    def plan(self, obs: Dict[str, Any], goal: Goal, memory: Dict[str, Any]) -> List[int]:
        start = obs["pos"]
        target = goal.target or start
        H, W = obs["grid_shape"]
        walls = memory.get("last_walls")
        if walls is None:
            walls = np.zeros((H,W), dtype=bool)
            memory["last_walls"] = walls

        patch, (y0,x0) = obs["patch"], obs["patch_origin"]
        for yy in range(patch.shape[0]):
            for xx in range(patch.shape[1]):
                if patch[yy,xx] == 1:
                    walls[y0+yy, x0+xx] = True

        open_set = [(0 + _heur(start, target), 0, start)]
        came = {start: None}
        g = {start: 0}
        found = False
        while open_set:
            f, cost, node = heapq.heappop(open_set)
            if node == target:
                found = True
                break
            for nb in _neighbors(node, (H,W)):
                if walls[nb[0], nb[1]]:
                    continue
                nd = cost + 1
                if nb not in g or nd < g[nb]:
                    g[nb] = nd
                    came[nb] = node
                    heapq.heappush(open_set, (nd + _heur(nb, target), nd, nb))
        if not found:
            return []

        path = []
        cur = target
        while cur != start:
            path.append(cur)
            cur = came[cur]
            if cur is None:
                break
        path.reverse()

        actions: List[int] = []
        prev = start
        for ny, nx in path:
            dy, dx = ny - prev[0], nx - prev[1]
            actions.append(ACTION_IDS.get((dy,dx), 0))
            prev = (ny, nx)
        if not actions:
            actions = [0]
        return actions
