---
title: QADE - Quant Analyst Decision Environment
emoji: 📈
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
tags:
  - openenv
  - reinforcement-learning
  - finance
  - trading
---
# QADE — Quant Analyst Decision Environment

## Overview
QADE (Quant Analyst Decision Environment) is an OpenEnv-compliant simulation platform designed to map modern AI inference agents to quantitative trading and portfolio management logic. By mapping strict financial consequences into an interactive FastAPI-driven RL-like container environment, it empowers modern LLM quant agents to test trading strategies in increasingly unpredictable scenarios without financial risk.

## Observation Space
The environment emits a state mapping of `QADEObservation` for decision making:

| Field | Type | Description |
|-------|------|-------------|
| `price_history` | `list[float]` | The last 30 closing prices as a leading buffer indicator |
| `rsi` | `float` | 14-period RSI indicator bounded between `[0.0, 100.0]` |
| `macd` | `float` | 12-to-26 EMA differential MACD line |
| `macd_signal` | `float` | The MACD 9-EMA Signal convergence marker |
| `volume` | `float` | Deterministic but chaotic volume linked to sequence differentials |
| `sentiment_score`| `float`| Polarized simulated external marker mapped from `[-1.0, 1.0]` |
| `volatility` | `float` | 252-window annualized standard deviation scalar |
| `portfolio_cash` | `float` | Free cash deployed natively measured in USD limit bounds |
| `portfolio_shares`| `float` | Held quantity balances |
| `portfolio_value` | `float` | Unified sum metric `(cash + shares * price)` |
| `step` | `int` | Internal integer frame step count |
| `task_name` | `str` | Easy/Medium/Hard pointer name identification (`bull_trend`, etc) |

## Action Space
`QADEAction` must be invoked natively as valid JSON via HTTP logic:

| Action Payload | Type | Notes |
|---|---|---|
| `action_type` | `Literal["BUY", "SELL", "HOLD"]` | Type of action the agent proposes. |
| `amount` | `float` | Positive USD quantity to direct toward the `action_type`. If `HOLD`, must strictly be `0.0`. |
| `reasoning` | `str` | The internal chain of logic validating the intent (for traceability). |

## Reward Function
Computed inside a strict exclusive `(0.001, 0.999)` clipping range (normalized from original `[-5.0, 5.0]` logic) based directly on deterministic events isolated per frame:
* **Profit Signal:** Basic % change of the active portfolio normalized `((pnl_delta / obs_before) * 100.0)`.
* **Overtrading Penalty:** Evaluates `BUY/SELL` activity strictly enforcing small friction `-0.05` drag to constrain chaos.
* **Drawdown Penalty:** Penalizes large distance shifts under historical portfolio peaks heavily if exceeding `0.05`.
* **Useless Action Penalty:** Flat `-0.2` score drops on actions attempting to trade capital without sufficient requirements natively (empty cache or void fractional bounds).
* **Consistency Bonus:** Progressive bonus maxed at `0.5` evaluating profitable execution trails over longer term (`3+ steps`).
* **Hold Penalty:** Enforces `-0.05` if holding passively sequentially over `5` times to prevent stalled looping.

## Tasks
QADE natively generates three core baseline progression environments dictating the task load mapping.
* **Easy: `bull_trend`** 
  - Represents a clear bull market. Features extremely low noise `0.005` constraints alongside heavy global positive upward drift. Setup is 30 episodes long.
  - *Good Behavior:* Identifying the consistent positive sentiment and acting quickly to accumulate safely without getting chopped.
* **Medium: `noisy_market`**
  - Designed as an uneven, noisy simulated landscape scaling down drift and heavily injecting unconstrained standard variance mapping bounds. Setup is 50 episodes.
  - *Good Behavior:* Effective drawdown regulation, avoiding useless overtrading penalties while timing dips securely.
* **Hard: `shock_recovery`**
  - Features 80 long-duration steps mapping a weak variance upward curve intersected unexpectedly by two sharp `20%` price drop shocks directly fixed at step boundaries.
  - *Good Behavior:* Reacting to sudden drops logically by catching profit bottoms directly absorbing volatility effectively and rebounding safely against fail limits.

## Grader Rubrics
Execution evaluation computes directly outside of Step iteration using normalized episode data. All final task scores are strictly clamped to the exclusive interval `(0.001, 0.999)` for validator compliance:

* **EASY GRADER (`bull_trend`)**: 
  - Yields 50% max score exclusively to final `pnl_pct` matching at least `10%`.
  - Yields remaining 50% proportional mapping directional validation metrics (Buying before growth, Holding/Selling before falls natively counts towards score mapping limits).

* **MEDIUM GRADER (`noisy_market`)**:
  - Focuses roughly 40% on conservative `5%` total profit margins natively.
  - Appends 40% solely dependent on averting maximum peak distance drops exceeding `15%`.
  - Weighs 20% on Trading Efficiency penalizing aggressively up to negative constraints past 20 operations securely.

* **HARD GRADER (`shock_recovery`)**:
  - Automatically zeros out the 30% Survival mapping weight entirely if the portfolio ever drops beneath `5000` capital layout bounds.
  - Evaluates Recovery dynamically granting 40% scaled rating via `min(ratio, 1.0)` to bounds exactly 10 loops immediately sequential against the mapped crash steps.
  - Requires 3% Profit margin arrays safely handling the 30% baseline.

## Setup & Usage

### 1. Requirements
Install dependencies safely:
```bash
pip install fastapi uvicorn numpy pydantic requests openai
```

### 2. Running Locally Server
Launch the HTTP OpenEnv handler:
```bash
uvicorn env:app --port 7860 --host 0.0.0.0
```

### 3. Agent Execution 
Invoke the LLM natively parsing decisions mapping natively:
```bash
export HF_TOKEN="your_token_here"
python inference.py
```

### 4. Docker Operations
```bash
docker build -t qade-server .
docker run -p 7860:7860 qade-server
# OR for inference container: docker run -e HF_TOKEN=$HF_TOKEN qade-agent
```

## Baseline Scores
_Placeholders to be overwritten sequentially during local runs!_
- **`bull_trend`**: TBD
- **`noisy_market`**: TBD
- **`shock_recovery`**: TBD

## Project Structure
```text
QADE/
├── models.py                   # Pydantic schemas isolating API layout endpoints
├── reward.py                   # Deterministic loop computation scalar matrices
├── env.py                      # OpenEnv backend endpoints natively deploying FastAPI
├── inference.py                # Main loop parser querying models and extracting decisions
├── openenv.yaml                # Standardized metadata registry spec natively
├── tasks/                      # Pre-configured deterministic price arrays mapping difficulty
│   ├── __init__.py
│   ├── easy.py
│   ├── medium.py
│   └── hard.py
└── graders/                    # Normalized validation metric formulas parsing score evaluation limits
    ├── __init__.py
    ├── easy_grader.py
    ├── medium_grader.py
    └── hard_grader.py
```
