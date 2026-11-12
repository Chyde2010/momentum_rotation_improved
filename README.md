# Momentum Rotation Improved
## Enhanced Large-Cap Momentum Strategy — Paper Trading Portfolio

> Improved version of the Large-Cap US Momentum Rotation Strategy.
> Running in parallel with `momentum_rotation_test` to compare performance.
> Updated automatically every day at 08:15 UTC via GitHub Actions.

**Last updated:** 2026-11-12 16:46 UTC

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
| Current NAV | $9,215.78 |
| Total return | -7.84% |
| CAGR (annualised) | -20.63% |
| Sharpe ratio | -1.669 |
| Max drawdown | -12.0% |
| Total trades | 31 |
| Days running | 129 |
| Last rebalance | 2026-11-02 |
| Current regime | FULL |

---

## Current Holdings

| Symbol | Entry Date | Entry Price | Current Price | Value | Unrealised | Composite Momentum |
|--------|-----------|------------|--------------|-------|------------|-------------------|
| TXN | 2026-10-01 | $279.45 | $312.27 | $1,873.62 | +11.7% | +44.19% |
| MRK | 2026-10-01 | $144.91 | $148.38 | $1,632.18 | +2.4% | +45.01% |
| AMGN | 2026-11-02 | $466.28 | $471.04 | $1,413.12 | +1.0% | +41.82% |
| XOM | 2026-11-02 | $180.78 | $169.06 | $1,521.54 | -6.5% | +35.57% |
| GILD | 2026-11-02 | $170.00 | $170.54 | $1,534.86 | +0.3% | +34.60% |

**Cash:** $1,240.46
*(Cash above normal levels indicates regime filter is active)*

---

## Recent Trades (last 10)

| Date | Action | Symbol | Shares | Price | Value | Composite Momentum |
|------|--------|--------|--------|-------|-------|-------------------|
| 2026-10-01 | BUY | TXN | 6 | $279.45 | $1,676.73 | +36.47% |
| 2026-10-01 | BUY | MRK | 11 | $144.91 | $1,594.01 | +35.38% |
| 2026-10-01 | BUY | CSCO | 15 | $107.96 | $1,619.40 | +33.96% |
| 2026-10-01 | BUY | TMO | 2 | $665.24 | $1,330.47 | +27.66% |
| 2026-11-02 | SELL | CAT | 2 | $621.60 | $1,243.20 | +29.61% |
| 2026-11-02 | SELL | CSCO | 15 | $103.13 | $1,546.95 | +33.96% |
| 2026-11-02 | SELL | TMO | 2 | $685.83 | $1,371.66 | +27.66% |
| 2026-11-02 | BUY | AMGN | 3 | $466.28 | $1,398.84 | +41.82% |
| 2026-11-02 | BUY | XOM | 9 | $180.78 | $1,627.07 | +35.57% |
| 2026-11-02 | BUY | GILD | 9 | $170.00 | $1,530.05 | +34.60% |


---

## NAV History (last 10 days)

| Date | NAV | Daily Return | Holdings | Regime |
|------|-----|-------------|----------|--------|
| 2026-10-30 | $9,340.13 | -1.50% | 5 | FULL |
| 2026-11-02 | $9,280.59 | -0.64% | 5 | FULL |
| 2026-11-03 | $9,253.75 | -0.29% | 5 | FULL |
| 2026-11-04 | $9,241.62 | -0.13% | 5 | FULL |
| 2026-11-05 | $9,167.60 | -0.80% | 5 | FULL |
| 2026-11-06 | $8,898.93 | -2.93% | 5 | FULL |
| 2026-11-09 | $9,024.61 | +1.41% | 5 | FULL |
| 2026-11-10 | $8,986.94 | -0.42% | 5 | FULL |
| 2026-11-11 | $9,099.03 | +1.25% | 5 | FULL |
| 2026-11-12 | $9,215.78 | +1.28% | 5 | FULL |


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
