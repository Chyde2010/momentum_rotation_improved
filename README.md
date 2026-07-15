# Momentum Rotation Improved
## Enhanced Large-Cap Momentum Strategy — Paper Trading Portfolio

> Improved version of the Large-Cap US Momentum Rotation Strategy.
> Running in parallel with `momentum_rotation_test` to compare performance.
> Updated automatically every day at 08:15 UTC via GitHub Actions.

**Last updated:** 2026-07-15 10:14 UTC

---

## Three Improvements Over Baseline

| # | Improvement | Purpose |
|---|-------------|---------|
| 1 | **Market Regime Filter** — SPY 200-day SMA | Reduces drawdown in bear markets |
| 2 | **Composite Momentum Signal** — weighted 1/3/6/12-month | More robust signal than 12-month only |
| 3 | **Volatility Filter** — excludes top 20% most volatile | Removes names that crash hardest |

---

## Current Market Regime

**🔴 REDUCED — SPY below 200-SMA, 50% position sizes, rest in cash**

The regime filter checks SPY against its 200-day moving average daily.
When below, position sizes are halved and the rest is held in cash.

---

## Portfolio Performance

| Metric | Value |
|--------|-------|
| Starting NAV | $10,000.00 |
| Current NAV | $10,024.82 |
| Total return | +0.25% |
| CAGR (annualised) | +10.58% |
| Sharpe ratio | Insufficient data |
| Max drawdown | -0.2% |
| Total trades | 5 |
| Days running | 9 |
| Last rebalance | 2026-07-07 |
| Current regime | REDUCED |

---

## Current Holdings

| Symbol | Entry Date | Entry Price | Current Price | Value | Unrealised | Composite Momentum |
|--------|-----------|------------|--------------|-------|------------|-------------------|
| HUM | 2026-07-07 | $394.62 | $406.00 | $1,624.00 | +2.9% | +62.17% |
| GOOGL | 2026-07-07 | $367.03 | $352.51 | $1,410.04 | -4.0% | +52.12% |
| GOOG | 2026-07-07 | $363.62 | $357.33 | $1,429.32 | -1.7% | +50.46% |
| CSCO | 2026-07-07 | $111.79 | $119.25 | $1,908.00 | +6.7% | +48.04% |
| JNJ | 2026-07-07 | $267.24 | $257.77 | $1,546.62 | -3.5% | +44.27% |

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
| 2026-07-06 | $10,000.00 | +0.00% | 0 | FULL |
| 2026-07-07 | $10,000.00 | +0.00% | 0 | FULL |
| 2026-07-08 | $10,000.00 | +0.00% | 5 | FULL |
| 2026-07-09 | $9,976.04 | -0.24% | 5 | FULL |
| 2026-07-10 | $10,005.96 | +0.30% | 5 | FULL |
| 2026-07-13 | $10,007.40 | +0.01% | 5 | FULL |
| 2026-07-14 | $9,998.18 | -0.09% | 5 | FULL |
| 2026-07-15 | $10,024.82 | +0.27% | 5 | REDUCED |


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
