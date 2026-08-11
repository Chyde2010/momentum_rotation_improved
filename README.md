# Momentum Rotation Improved
## Enhanced Large-Cap Momentum Strategy — Paper Trading Portfolio

> Improved version of the Large-Cap US Momentum Rotation Strategy.
> Running in parallel with `momentum_rotation_test` to compare performance.
> Updated automatically every day at 08:15 UTC via GitHub Actions.

**Last updated:** 2026-08-11 09:11 UTC

---

## Three Improvements Over Baseline

| # | Improvement | Purpose |
|---|-------------|---------|
| 1 | **Market Regime Filter** — SPY 200-day SMA | Reduces drawdown in bear markets |
| 2 | **Composite Momentum Signal** — weighted 1/3/6/12-month | More robust signal than 12-month only |
| 3 | **Volatility Filter** — excludes top 20% most volatile | Removes names that crash hardest |

---

## Current Market Regime

**⚪ FULL — SPY above 200-SMA, full position sizes**

The regime filter checks SPY against its 200-day moving average daily.
When below, position sizes are halved and the rest is held in cash.

---

## Portfolio Performance

| Metric | Value |
|--------|-------|
| Starting NAV | $10,000.00 |
| Current NAV | $10,032.24 |
| Total return | +0.32% |
| CAGR (annualised) | +3.32% |
| Sharpe ratio | -0.009 |
| Max drawdown | -4.3% |
| Total trades | 11 |
| Days running | 36 |
| Last rebalance | 2026-08-03 |
| Current regime | FULL |

---

## Current Holdings

| Symbol | Entry Date | Entry Price | Current Price | Value | Unrealised | Composite Momentum |
|--------|-----------|------------|--------------|-------|------------|-------------------|
| HUM | 2026-07-07 | $394.62 | $385.70 | $1,542.80 | -2.3% | +55.82% |
| CSCO | 2026-07-07 | $111.79 | $122.57 | $1,961.12 | +9.6% | +50.08% |
| UNH | 2026-08-03 | $414.40 | $408.74 | $1,634.96 | -1.4% | +44.46% |
| CAT | 2026-08-03 | $814.81 | $837.58 | $1,675.16 | +2.8% | +39.23% |
| MRK | 2026-08-03 | $130.20 | $130.92 | $1,701.96 | +0.6% | +38.27% |

**Cash:** $1,516.24
*(Cash above normal levels indicates regime filter is active)*

---

## Recent Trades (last 10)

| Date | Action | Symbol | Shares | Price | Value | Composite Momentum |
|------|--------|--------|--------|-------|-------|-------------------|
| 2026-07-07 | BUY | GOOGL | 4 | $367.03 | $1,468.12 | +52.12% |
| 2026-07-07 | BUY | GOOG | 4 | $363.62 | $1,454.48 | +50.46% |
| 2026-07-07 | BUY | CSCO | 16 | $111.79 | $1,788.64 | +48.04% |
| 2026-07-07 | BUY | JNJ | 6 | $267.24 | $1,603.44 | +44.27% |
| 2026-08-03 | SELL | GOOGL | 4 | $356.13 | $1,424.52 | +52.12% |
| 2026-08-03 | SELL | GOOG | 4 | $356.65 | $1,426.60 | +50.46% |
| 2026-08-03 | SELL | JNJ | 6 | $256.35 | $1,538.10 | +44.27% |
| 2026-08-03 | BUY | UNH | 4 | $414.40 | $1,657.60 | +44.46% |
| 2026-08-03 | BUY | CAT | 2 | $814.81 | $1,629.62 | +39.23% |
| 2026-08-03 | BUY | MRK | 13 | $130.20 | $1,692.60 | +38.27% |


---

## NAV History (last 10 days)

| Date | NAV | Daily Return | Holdings | Regime |
|------|-----|-------------|----------|--------|
| 2026-07-29 | $9,672.78 | +0.00% | 5 | REDUCED |
| 2026-07-30 | $9,651.22 | -0.22% | 5 | FULL |
| 2026-07-31 | $9,594.72 | -0.59% | 5 | FULL |
| 2026-08-03 | $9,807.34 | +2.22% | 5 | FULL |
| 2026-08-04 | $9,807.34 | +0.00% | 5 | REDUCED |
| 2026-08-05 | $9,960.00 | +1.56% | 5 | FULL |
| 2026-08-06 | $9,976.97 | +0.17% | 5 | FULL |
| 2026-08-07 | $9,917.89 | -0.59% | 5 | FULL |
| 2026-08-10 | $9,983.36 | +0.66% | 5 | FULL |
| 2026-08-11 | $10,032.24 | +0.49% | 5 | FULL |


---

## Composite Momentum Formula

Score = (1M return × 10%) + (3M return × 20%) + (6M return × 30%) + (12M return × 40%)

Weights reflect academic evidence that longer-term momentum is more predictive
but shorter-term signals add useful information at the margin.

---

## Comparison With Baseline

Both strategies start with $10,000 on the same date.
Check `momentum_rotation_test` for the baseline results.

Expected differences when improvements are working:
- **Lower drawdown** during bear markets (regime filter)
- **Different stock selection** (composite vs 12M, vol filter)
- **Cash allocation** visible when regime is REDUCED

---

## Repository Structure

```
momentum_rotation_improved/
├── .github/workflows/momentum_improved_update.yml
├── data/
│   ├── portfolio.csv
│   ├── nav_snapshots.csv
│   ├── trade_log.csv
│   └── state.json
├── src/momentum_improved_update.py
├── requirements.txt
└── README.md
```

---

*Paper trading only. Not investment advice. No real capital deployed.*
