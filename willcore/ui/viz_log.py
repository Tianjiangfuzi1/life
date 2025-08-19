import json
import sys
import matplotlib.pyplot as plt

def load_log(path):
    steps = []
    energy = []
    GA = []; CD = []; CS = []; SM = []; XR = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            rec = json.loads(line)
            steps.append(rec.get('step', 0))
            energy.append(rec.get('energy', 0))
            fwi = rec.get('fwi', {})
            GA.append(fwi.get('GA', 0.0))
            CD.append(fwi.get('CD', 0.0))
            CS.append(fwi.get('CS', 0.0))
            SM.append(fwi.get('SM', 0.0))
            XR.append(fwi.get('XR', 0.0))
    return steps, energy, GA, CD, CS, SM, XR

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m willcore.ui.viz_log <path/to/why_xxx.jsonl>")
        sys.exit(1)
    path = sys.argv[1]
    s, e, GA, CD, CS, SM, XR = load_log(path)

    # Chart 1: Energy over time
    plt.figure()
    plt.plot(s, e)
    plt.title("Energy over time")
    plt.xlabel("Step")
    plt.ylabel("Energy")
    plt.show()

    # Chart 2: FWI components
    plt.figure()
    plt.plot(s, GA, label="GA")
    plt.plot(s, CD, label="CD")
    plt.plot(s, CS, label="CS")
    plt.plot(s, SM, label="SM")
    plt.plot(s, XR, label="XR")
    plt.title("FWI components over time")
    plt.xlabel("Step")
    plt.ylabel("Score (0-1)")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
