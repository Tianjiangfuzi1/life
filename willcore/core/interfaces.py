from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from .types import Goal, TrajStats

class IEnv(ABC):
    @abstractmethod
    def reset(self, seed: Optional[int] = None) -> Dict[str, Any]:
        ...

    @abstractmethod
    def step(self, action: int) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        ...

    @abstractmethod
    def render(self) -> str:
        ...

class IGoalFactory(ABC):
    @abstractmethod
    def propose(self, obs: Dict[str, Any], memory: Dict[str, Any]) -> List[Goal]:
        ...

class IPlanner(ABC):
    @abstractmethod
    def plan(self, obs: Dict[str, Any], goal: Goal, memory: Dict[str, Any]) -> List[int]:
        # Return a planned action sequence; empty if no plan.
        ...

class IValueSystem(ABC):
    @abstractmethod
    def score(self, stats: TrajStats, prefs: Any, mood: Any) -> float:
        ...

class ICommitmentManager(ABC):
    @abstractmethod
    def decide(self, step_idx: int, current_goal: Optional[Goal], 
               candidates: List[Tuple[Goal, float, TrajStats]],
               last_switch_step: int,
               switching_cost: float,
               t_min: int) -> Tuple[Goal, Dict[str, Any]]:
        ...
