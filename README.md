# Momentum Rotation Improved
## Enhanced Large-Cap Momentum Strategy — Paper Trading Portfolio

> Improved version of the Large-Cap US Momentum Rotation Strategy.
> Running in parallel with `momentum_rotation_test` to compare performance.
> Updated automatically every day at 08:15 UTC via GitHub Actions.

**Last updated:** 2026-10-05 17:06 UTC

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
| Current NAV | $9,652.01 |
| Total return | -3.48% |
| CAGR (annualised) | -13.24% |
| Sharpe ratio | -1.205 |
| Max drawdown | -6.7% |
| Total trades | 25 |
| Days running | 91 |
| Last rebalance | 2026-10-01 |
| Current regime | FULL |

---

## Current Holdings

| Symbol | Entry Date | Entry Price | Current Price | Value | Unrealised | Composite Momentum |
|--------|-----------|------------|--------------|-------|------------|-------------------|
| CAT | 2026-08-03 | $814.81 | $852.80 | $1,705.60 | +4.7% | +29.61% |
| TXN | 2026-10-01 | $279.45 | $292.44 | $1,754.67 | +4.7% | +36.47% |
| MRK | 2026-10-01 | $144.91 | $140.23 | $1,542.53 | -3.2% | +35.38% |
| CSCO | 2026-10-01 | $107.96 | $112.09 | $1,681.35 | +3.8% | +33.96% |
| TMO | 2026-10-01 | $665.24 | $666.62 | $1,333.25 | +0.2% | +27.66% |

**Cash:** $1,634.61
*(Cash above normal levels indicates regime filter is active)*

---

## Recent Trades (last 10)

| Date | Action | Symbol | Shares | Price | Value | Composite Momentum |
|------|--------|--------|--------|-------|-------|-------------------|
| 2026-09-01 | BUY | AMGN | 4 | $429.88 | $1,719.52 | +33.26% |
| 2026-09-01 | BUY | CSX | 35 | $50.51 | $1,767.85 | +29.99% |
| 2026-10-01 | SELL | HUM | 4 | $381.00 | $1,524.00 | +47.98% |
| 2026-10-01 | SELL | FDX | 5 | $284.87 | $1,424.35 | +33.43% |
| 2026-10-01 | SELL | AMGN | 4 | $413.39 | $1,653.56 | +33.26% |
| 2026-10-01 | SELL | CSX | 35 | $46.15 | $1,615.08 | +29.99% |
| 2026-10-01 | BUY | TXN | 6 | $279.45 | $1,676.73 | +36.47% |
| 2026-10-01 | BUY | MRK | 11 | $144.91 | $1,594.01 | +35.38% |
| 2026-10-01 | BUY | CSCO | 15 | $107.96 | $1,619.40 | +33.96% |
| 2026-10-01 | BUY | TMO | 2 | $665.24 | $1,330.47 | +27.66% |


---

## NAV History (last 10 days)

| Date | NAV | Daily Return | Holdings | Regime |
|------|-----|-------------|----------|--------|
| 2026-09-22 | $9,446.79 | -0.10% | 5 | FULL |
| 2026-09-23 | $9,465.96 | +0.20% | 5 | FULL |
| 2026-09-24 | $9,461.14 | -0.05% | 5 | FULL |
| 2026-09-25 | $9,532.30 | +0.75% | 5 | FULL |
| 2026-09-28 | $9,603.55 | +0.75% | 5 | FULL |
| 2026-09-29 | $9,561.99 | -0.43% | 5 | FULL |
| 2026-09-30 | $9,611.60 | +0.52% | 5 | FULL |
| 2026-10-01 | $9,481.91 | -1.35% | 5 | FULL |
| 2026-10-02 | $9,640.03 | +1.67% | 5 | FULL |
| 2026-10-05 | $9,652.01 | +0.12% | 5 | FULL |


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
