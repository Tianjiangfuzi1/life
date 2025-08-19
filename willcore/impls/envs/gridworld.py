from typing import Dict, Any, Optional, Tuple, List
import numpy as np
from willcore.core.interfaces import IEnv

# Actions: 0=stay, 1=up, 2=down, 3=left, 4=right
ACTIONS = [(0,0), (-1,0), (1,0), (0,-1), (0,1)]

class GridWorld(IEnv):
    def __init__(self, w=12, h=12, food=6, traps=6, walls=12, energy=80, view=3, seed: Optional[int]=None):
        self.w, self.h = w, h
        self.food_n, self.traps_n, self.walls_n = food, traps, walls
        self.max_energy = energy
        self.view = view
        self.rng = np.random.default_rng(seed)
        self.reset(seed)

    def reset(self, seed: Optional[int] = None) -> Dict[str, Any]:
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self.grid = np.zeros((self.h, self.w), dtype=np.int8)  # 0 empty, 1 wall, 2 food, 3 trap
        # place walls
        for _ in range(self.walls_n):
            y, x = self.rng.integers(0, self.h), self.rng.integers(0, self.w)
            self.grid[y, x] = 1
        # place food
        for _ in range(self.food_n):
            y, x = self.rng.integers(0, self.h), self.rng.integers(0, self.w)
            if self.grid[y, x] == 0:
                self.grid[y, x] = 2
        # place traps
        for _ in range(self.traps_n):
            y, x = self.rng.integers(0, self.h), self.rng.integers(0, self.w)
            if self.grid[y, x] == 0:
                self.grid[y, x] = 3

        # agent spawn
        while True:
            y, x = self.rng.integers(0, self.h), self.rng.integers(0, self.w)
            if self.grid[y, x] == 0:
                self.pos = (y, x)
                break

        self.energy = self.max_energy
        self.step_idx = 0
        self.discovered = np.zeros_like(self.grid, dtype=bool)
        return self._obs()

    def _in_bounds(self, y, x):
        return 0 <= y < self.h and 0 <= x < self.w

    def _obs(self) -> Dict[str, Any]:
        y, x = self.pos
        v = self.view
        y0, y1 = max(0, y-v), min(self.h, y+v+1)
        x0, x1 = max(0, x-v), min(self.w, x+v+1)
        patch = self.grid[y0:y1, x0:x1].copy()
        # mark discovered
        self.discovered[y0:y1, x0:x1] = True
        return {
            "pos": self.pos,
            "energy": self.energy,
            "patch": patch,
            "patch_origin": (y0, x0),
            "discovered": self.discovered.copy(),
            "grid_shape": self.grid.shape,
        }

    def step(self, action: int):
        self.step_idx += 1
        dy, dx = ACTIONS[action]
        y, x = self.pos
        ny, nx = y + dy, x + dx
        if not self._in_bounds(ny, nx) or self.grid[ny, nx] == 1:
            ny, nx = y, x  # bump into wall stays
        self.pos = (ny, nx)
        reward = -1.0  # step cost
        # cell effect
        cell = self.grid[ny, nx]
        if cell == 2:  # food
            reward += 10.0
            self.grid[ny, nx] = 0
        elif cell == 3:  # trap
            reward -= 10.0
        # energy update
        self.energy -= 1
        done = self.energy <= 0
        return self._obs(), reward, done, {}

    def render(self) -> str:
        # simple ASCII
        chars = {0:".", 1:"#", 2:"F", 3:"X"}
        lines = []
        for y in range(self.h):
            row = []
            for x in range(self.w):
                if (y,x) == self.pos:
                    row.append("A")
                else:
                    row.append(chars[self.grid[y,x]])
            lines.append("".join(row))
        return "\n".join(lines)
