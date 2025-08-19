# life-skeleton (MVP)

A sustainable architecture and **CPU-only** code skeleton for building an *information lifeform* with **emergent will**.  
It includes:
- Modular interfaces (`core/*`) and pluggable implementations (`impls/*`)
- A minimal **GridWorld** environment (2D) that runs on CPU only
- **GoalFactory** (rule-based v0), **ValueSystem**, **Planner (A*)**
- **CommitmentManager** (intent persistence + rational revision)
- **Why-Logger** (structured decision logs) and a tiny **FWI** (Free Will Index) readout
- Configuration via YAML

> Copy this skeleton into your repo and evolve modules without breaking interfaces.

## Quickstart
```bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python willcore/examples/gridworld_min/run.py
```

You should see the agent moving in a 2D world, printing its current intent, candidate goals, and an FWI summary.

## Layout
```
willcore/
  core/                 # stable interfaces & dataclasses
  impls/                # pluggable implementations (v0 baselines)
  runtime/              # loop, event bus, registry
  ui/                   # simple CLI FWI readout
  configs/              # YAML configs
  data/
    logs/               # JSONL why-logs
    checkpoints/        # (reserved)
  examples/
    gridworld_min/      # runnable CPU-only demo
```

## Evolving Roadmap
- v0.x: Rule-based GoalFactory, A*, no learned world model
- v0.7: Lightweight learned dynamics (GRU), short-horizon counterfactual rollout
- v0.8: Skills/options & improved commitment logic
- v0.9: Self-model & meta-learning pass
- v1.x: Multi-agent & social drives
