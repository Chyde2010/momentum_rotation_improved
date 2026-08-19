# Momentum Rotation Improved
## Enhanced Large-Cap Momentum Strategy — Paper Trading Portfolio

> Improved version of the Large-Cap US Momentum Rotation Strategy.
> Running in parallel with `momentum_rotation_test` to compare performance.
> Updated automatically every day at 08:15 UTC via GitHub Actions.

**Last updated:** 2026-08-19 08:51 UTC

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
| Current NAV | $9,844.67 |
| Total return | -1.55% |
| CAGR (annualised) | -12.18% |
| Sharpe ratio | -1.013 |
| Max drawdown | -4.3% |
| Total trades | 11 |
| Days running | 44 |
| Last rebalance | 2026-08-03 |
| Current regime | FULL |

---

## Current Holdings

| Symbol | Entry Date | Entry Price | Current Price | Value | Unrealised | Composite Momentum |
|--------|-----------|------------|--------------|-------|------------|-------------------|
| HUM | 2026-07-07 | $394.62 | $382.00 | $1,528.00 | -3.2% | +55.82% |
| CSCO | 2026-07-07 | $111.79 | $111.61 | $1,785.76 | -0.2% | +50.08% |
| UNH | 2026-08-03 | $414.40 | $393.93 | $1,575.72 | -4.9% | +44.46% |
| CAT | 2026-08-03 | $814.81 | $840.87 | $1,681.74 | +3.2% | +39.23% |
| MRK | 2026-08-03 | $130.20 | $135.17 | $1,757.21 | +3.8% | +38.27% |

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
| 2026-08-06 | $9,976.97 | +0.17% | 5 | FULL |
| 2026-08-07 | $9,917.89 | -0.59% | 5 | FULL |
| 2026-08-10 | $9,983.36 | +0.66% | 5 | FULL |
| 2026-08-11 | $10,032.24 | +0.49% | 5 | FULL |
| 2026-08-12 | $9,925.36 | -1.07% | 5 | FULL |
| 2026-08-13 | $10,115.16 | +1.91% | 5 | FULL |
| 2026-08-14 | $9,939.23 | -1.74% | 5 | FULL |
| 2026-08-17 | $9,945.30 | +0.06% | 5 | FULL |
| 2026-08-18 | $9,945.30 | +0.00% | 5 | REDUCED |
| 2026-08-19 | $9,844.67 | -1.01% | 5 | FULL |


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
