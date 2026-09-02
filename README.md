# Momentum Rotation Improved
## Enhanced Large-Cap Momentum Strategy — Paper Trading Portfolio

> Improved version of the Large-Cap US Momentum Rotation Strategy.
> Running in parallel with `momentum_rotation_test` to compare performance.
> Updated automatically every day at 08:15 UTC via GitHub Actions.

**Last updated:** 2026-09-02 12:44 UTC

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
| Current NAV | $9,857.45 |
| Total return | -1.43% |
| CAGR (annualised) | -8.64% |
| Sharpe ratio | -0.805 |
| Max drawdown | -4.3% |
| Total trades | 17 |
| Days running | 58 |
| Last rebalance | 2026-09-01 |
| Current regime | FULL |

---

## Current Holdings

| Symbol | Entry Date | Entry Price | Current Price | Value | Unrealised | Composite Momentum |
|--------|-----------|------------|--------------|-------|------------|-------------------|
| HUM | 2026-07-07 | $394.62 | $394.88 | $1,579.52 | +0.1% | +47.98% |
| CAT | 2026-08-03 | $814.81 | $779.16 | $1,558.32 | -4.4% | +34.18% |
| FDX | 2026-09-01 | $327.40 | $324.88 | $1,624.40 | -0.8% | +33.43% |
| AMGN | 2026-09-01 | $429.88 | $438.12 | $1,752.48 | +1.9% | +33.26% |
| CSX | 2026-09-01 | $50.51 | $48.70 | $1,704.50 | -3.6% | +29.99% |

**Cash:** $1,638.23
*(Cash above normal levels indicates regime filter is active)*

---

## Recent Trades (last 10)

| Date | Action | Symbol | Shares | Price | Value | Composite Momentum |
|------|--------|--------|--------|-------|-------|-------------------|
| 2026-08-03 | SELL | JNJ | 6 | $256.35 | $1,538.10 | +44.27% |
| 2026-08-03 | BUY | UNH | 4 | $414.40 | $1,657.60 | +44.46% |
| 2026-08-03 | BUY | CAT | 2 | $814.81 | $1,629.62 | +39.23% |
| 2026-08-03 | BUY | MRK | 13 | $130.20 | $1,692.60 | +38.27% |
| 2026-09-01 | SELL | CSCO | 16 | $110.49 | $1,767.84 | +50.08% |
| 2026-09-01 | SELL | UNH | 4 | $389.41 | $1,557.64 | +44.46% |
| 2026-09-01 | SELL | MRK | 13 | $147.76 | $1,920.88 | +38.27% |
| 2026-09-01 | BUY | FDX | 5 | $327.40 | $1,637.00 | +33.43% |
| 2026-09-01 | BUY | AMGN | 4 | $429.88 | $1,719.52 | +33.26% |
| 2026-09-01 | BUY | CSX | 35 | $50.51 | $1,767.85 | +29.99% |


---

## NAV History (last 10 days)

| Date | NAV | Daily Return | Holdings | Regime |
|------|-----|-------------|----------|--------|
| 2026-08-20 | $9,962.46 | +1.20% | 5 | FULL |
| 2026-08-21 | $9,899.65 | -0.63% | 5 | FULL |
| 2026-08-24 | $10,007.79 | +1.09% | 5 | FULL |
| 2026-08-25 | $10,002.02 | -0.06% | 5 | FULL |
| 2026-08-26 | $10,095.63 | +0.94% | 5 | FULL |
| 2026-08-27 | $10,056.16 | -0.39% | 5 | FULL |
| 2026-08-28 | $9,917.91 | -1.37% | 5 | FULL |
| 2026-08-31 | $9,897.17 | -0.21% | 5 | FULL |
| 2026-09-01 | $9,890.46 | -0.07% | 5 | FULL |
| 2026-09-02 | $9,857.45 | -0.33% | 5 | FULL |


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
