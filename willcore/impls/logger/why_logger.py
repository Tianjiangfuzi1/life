from typing import Dict, Any
import json, os, time

# —— 新增：把 numpy 类型递归地变成原生 Python —— #
def _to_py(obj):
    try:
        import numpy as np
        np_types = (np.integer, np.floating, np.bool_)
    except Exception:
        np_types = tuple()

    if isinstance(obj, dict):
        return {k: _to_py(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [_to_py(v) for v in obj]
    # numpy 数字/布尔
    if np_types and isinstance(obj, np_types):
        return obj.item()
    # numpy 数组
    try:
        import numpy as np
        if isinstance(obj, np.ndarray):
            return obj.tolist()
    except Exception:
        pass
    return obj

class WhyLogger:
    def __init__(self, log_dir: str):
        os.makedirs(log_dir, exist_ok=True)
        ts = time.strftime("%Y%m%d_%H%M%S")
        self.fp = open(os.path.join(log_dir, f"why_{ts}.jsonl"), "a", encoding="utf-8")

    def log(self, record: Dict[str, Any]):
        safe = _to_py(record)  # ← 关键：先转成原生类型
        self.fp.write(json.dumps(safe, ensure_ascii=False) + "\n")
        self.fp.flush()

    def close(self):
        try:
            self.fp.close()
        except Exception:
            pass

