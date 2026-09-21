# Momentum Rotation Improved
## Enhanced Large-Cap Momentum Strategy — Paper Trading Portfolio

> Improved version of the Large-Cap US Momentum Rotation Strategy.
> Running in parallel with `momentum_rotation_test` to compare performance.
> Updated automatically every day at 08:15 UTC via GitHub Actions.

**Last updated:** 2026-09-21 15:04 UTC

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
| Current NAV | $9,456.03 |
| Total return | -5.44% |
| CAGR (annualised) | -23.29% |
| Sharpe ratio | -2.027 |
| Max drawdown | -6.7% |
| Total trades | 17 |
| Days running | 77 |
| Last rebalance | 2026-09-01 |
| Current regime | FULL |

---

## Current Holdings

| Symbol | Entry Date | Entry Price | Current Price | Value | Unrealised | Composite Momentum |
|--------|-----------|------------|--------------|-------|------------|-------------------|
| HUM | 2026-07-07 | $394.62 | $382.20 | $1,528.82 | -3.1% | +47.98% |
| CAT | 2026-08-03 | $814.81 | $817.71 | $1,635.42 | +0.4% | +34.18% |
| FDX | 2026-09-01 | $327.40 | $294.06 | $1,470.30 | -10.2% | +33.43% |
| AMGN | 2026-09-01 | $429.88 | $391.96 | $1,567.84 | -8.8% | +33.26% |
| CSX | 2026-09-01 | $50.51 | $46.16 | $1,615.42 | -8.6% | +29.99% |

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
| 2026-09-08 | $9,963.14 | +0.00% | 5 | FULL |
| 2026-09-09 | $9,753.88 | -2.10% | 5 | FULL |
| 2026-09-10 | $9,673.41 | -0.82% | 5 | FULL |
| 2026-09-11 | $9,656.43 | -0.18% | 5 | FULL |
| 2026-09-14 | $9,623.96 | -0.34% | 5 | FULL |
| 2026-09-15 | $9,635.01 | +0.11% | 5 | FULL |
| 2026-09-16 | $9,538.79 | -1.00% | 5 | FULL |
| 2026-09-17 | $9,433.05 | -1.11% | 5 | FULL |
| 2026-09-18 | $9,498.47 | +0.69% | 5 | FULL |
| 2026-09-21 | $9,456.03 | -0.45% | 5 | FULL |


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
