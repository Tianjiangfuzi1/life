from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any, Optional

Pos = Tuple[int, int]

@dataclass
class Goal:
    kind: str                 # e.g. "collect_food", "explore_frontier"
    target: Optional[Pos]     # cell target (if applicable)
    desc: str                 # human-readable description

@dataclass
class TrajStats:
    path_len: int = 0
    extrinsic: float = 0.0
    curiosity: float = 0.0
    empowerment: float = 0.0
    novelty: float = 0.0
    risk: float = 0.0

@dataclass
class DecisionReason:
    candidates: List[Dict[str, Any]]  # each: {goal, score, stats}
    chosen: Dict[str, Any]
    switching_cost_applied: float
    reeval_triggered: bool

@dataclass
class StepLog:
    step: int
    pos: Pos
    energy: int
    reason: DecisionReason
    fwi: Dict[str, float] = field(default_factory=dict)

@dataclass
class Prefs:
    a: float = 1.0  # extrinsic
    b: float = 0.4  # curiosity
    c: float = 0.0  # empowerment (unused in v0)
    d: float = 0.2  # novelty
    l: float = 0.3  # risk (lambda)

@dataclass
class Mood:
    valence: float = 0.0
    arousal: float = 0.0
    control: float = 0.0
