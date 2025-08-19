class SimpleSelfModel:
    # Tracks naive success rates by goal kind (placeholder for v0).
    def __init__(self):
        self.success_count = {}
        self.attempt_count = {}

    def record(self, goal_kind: str, success: bool):
        self.attempt_count[goal_kind] = self.attempt_count.get(goal_kind, 0) + 1
        if success:
            self.success_count[goal_kind] = self.success_count.get(goal_kind, 0) + 1

    def success_rate(self, goal_kind: str) -> float:
        a = self.attempt_count.get(goal_kind, 0)
        s = self.success_count.get(goal_kind, 0)
        return (s / a) if a else 0.0
