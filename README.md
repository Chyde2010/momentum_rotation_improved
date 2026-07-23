# Momentum Rotation Improved
## Enhanced Large-Cap Momentum Strategy — Paper Trading Portfolio

> Improved version of the Large-Cap US Momentum Rotation Strategy.
> Running in parallel with `momentum_rotation_test` to compare performance.
> Updated automatically every day at 08:15 UTC via GitHub Actions.

**Last updated:** 2026-07-23 10:34 UTC

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
| Current NAV | $9,762.38 |
| Total return | -2.38% |
| CAGR (annualised) | -40.33% |
| Sharpe ratio | Insufficient data |
| Max drawdown | -2.8% |
| Total trades | 5 |
| Days running | 17 |
| Last rebalance | 2026-07-07 |
| Current regime | FULL |

---

## Current Holdings

| Symbol | Entry Date | Entry Price | Current Price | Value | Unrealised | Composite Momentum |
|--------|-----------|------------|--------------|-------|------------|-------------------|
| HUM | 2026-07-07 | $394.62 | $397.60 | $1,590.40 | +0.8% | +62.17% |
| GOOGL | 2026-07-07 | $367.03 | $342.09 | $1,368.36 | -6.8% | +52.12% |
| GOOG | 2026-07-07 | $363.62 | $341.91 | $1,367.64 | -6.0% | +50.46% |
| CSCO | 2026-07-07 | $111.79 | $112.21 | $1,795.36 | +0.4% | +48.04% |
| JNJ | 2026-07-07 | $267.24 | $255.63 | $1,533.78 | -4.3% | +44.27% |

**Cash:** $2,106.84
*(Cash above normal levels indicates regime filter is active)*

---

## Recent Trades (last 10)

| Date | Action | Symbol | Shares | Price | Value | Composite Momentum |
|------|--------|--------|--------|-------|-------|-------------------|
| 2026-07-07 | BUY | HUM | 4 | $394.62 | $1,578.48 | +62.17% |
| 2026-07-07 | BUY | GOOGL | 4 | $367.03 | $1,468.12 | +52.12% |
| 2026-07-07 | BUY | GOOG | 4 | $363.62 | $1,454.48 | +50.46% |
| 2026-07-07 | BUY | CSCO | 16 | $111.79 | $1,788.64 | +48.04% |
| 2026-07-07 | BUY | JNJ | 6 | $267.24 | $1,603.44 | +44.27% |


---

## NAV History (last 10 days)

| Date | NAV | Daily Return | Holdings | Regime |
|------|-----|-------------|----------|--------|
| 2026-07-10 | $10,005.96 | +0.30% | 5 | FULL |
| 2026-07-13 | $10,007.40 | +0.01% | 5 | FULL |
| 2026-07-14 | $9,998.18 | -0.09% | 5 | FULL |
| 2026-07-15 | $10,024.82 | +0.27% | 5 | REDUCED |
| 2026-07-16 | $9,972.92 | -0.52% | 5 | FULL |
| 2026-07-17 | $9,740.22 | -2.33% | 5 | FULL |
| 2026-07-20 | $9,787.68 | +0.49% | 5 | FULL |
| 2026-07-21 | $9,777.20 | -0.11% | 5 | FULL |
| 2026-07-22 | $9,796.10 | +0.19% | 5 | FULL |
| 2026-07-23 | $9,762.38 | -0.34% | 5 | FULL |


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
