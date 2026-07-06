# =============================================================================
# MOMENTUM ROTATION IMPROVED — Daily Update Script
# =============================================================================
# Improved version of the Large-Cap US Momentum Rotation Strategy.
# Runs in parallel with momentum_rotation_test to compare performance.
#
# IMPROVEMENTS OVER BASELINE:
#
#   1. MARKET REGIME FILTER
#      When SPY is below its 200-day SMA, reduce position sizes to 50%
#      and hold the remainder in cash. Targets the 822-day drawdown
#      recovery problem in the baseline strategy.
#
#   2. COMPOSITE MOMENTUM SIGNAL
#      Instead of 12-month return only, uses weighted composite:
#        1-month  return: 10% weight
#        3-month  return: 20% weight
#        6-month  return: 30% weight
#        12-month return: 40% weight
#      More robust signal than single lookback.
#
#   3. VOLATILITY FILTER
#      Excludes stocks whose 20-day realised volatility is in the top
#      20% of the universe. Removes high-vol names that crash hardest
#      during momentum reversals.
#
# EVERYTHING ELSE IS IDENTICAL TO BASELINE:
#   Universe: Top 50 large-cap US equities (S&P 100 proxy)
#   Portfolio: Top 5 momentum stocks
#   Rebalance: First trading day of each month
#   Starting NAV: $10,000
# =============================================================================

import os
import json
import time
import warnings
from datetime import datetime, timedelta, timezone, date

import numpy as np
import pandas as pd
import yfinance as yf

warnings.filterwarnings('ignore')

# =============================================================================
# CONFIG
# =============================================================================

STARTING_NAV       = 10_000.00
PORTFOLIO_SIZE     = 5
MIN_PRICE          = 5.0
MIN_DOLLAR_VOL     = 5e6
LOOKBACK_DAYS      = 252      # 12-month base lookback

# IMPROVEMENT 2: Composite momentum weights
MOMENTUM_WEIGHTS = {
    21:  0.10,   # 1-month
    63:  0.20,   # 3-month
    126: 0.30,   # 6-month
    252: 0.40,   # 12-month
}

# IMPROVEMENT 3: Volatility filter
VOL_LOOKBACK       = 20       # 20-day realised volatility
VOL_PERCENTILE     = 0.80     # Exclude top 20% most volatile

# IMPROVEMENT 1: Regime filter
REGIME_SMA_DAYS    = 200      # SPY 200-day SMA
REGIME_POSITION_SIZE_FULL   = 0.90   # Full allocation when above SMA
REGIME_POSITION_SIZE_REDUCED = 0.45  # Half allocation when below SMA

# Environment detection
if os.path.isdir('/content/drive/MyDrive'):
    BASE_DIR = '/content/drive/MyDrive/momentum_rotation_improved'
elif os.path.isdir('/home/runner/work'):
    BASE_DIR = os.environ.get('GITHUB_WORKSPACE', os.getcwd())
else:
    BASE_DIR = os.getcwd()

os.makedirs(os.path.join(BASE_DIR, 'data'), exist_ok=True)

DATA_DIR       = os.path.join(BASE_DIR, 'data')
PORTFOLIO_PATH = os.path.join(DATA_DIR, 'portfolio.csv')
NAV_PATH       = os.path.join(DATA_DIR, 'nav_snapshots.csv')
TRADE_LOG_PATH = os.path.join(DATA_DIR, 'trade_log.csv')
README_PATH    = os.path.join(BASE_DIR, 'README.md')
STATE_PATH     = os.path.join(DATA_DIR, 'state.json')

today = datetime.now(timezone.utc).date()
now   = datetime.now(timezone.utc)

# Skip weekends
if today.weekday() >= 5:
    print(f'Today is {today.strftime("%A")} — markets closed. Skipping.')
    exit(0)

print('=' * 60)
print('MOMENTUM ROTATION IMPROVED — Daily Update')
print(f'Date: {today} UTC')
print('=' * 60)


# =============================================================================
# S&P 100 UNIVERSE
# =============================================================================

SP100_TICKERS = [
    'AAPL', 'MSFT', 'NVDA', 'AMZN', 'META', 'GOOGL', 'GOOG', 'BRK-B',
    'LLY', 'JPM', 'V', 'UNH', 'XOM', 'TSLA', 'MA', 'AVGO', 'PG', 'JNJ',
    'HD', 'COST', 'MRK', 'ABBV', 'CVX', 'BAC', 'NFLX', 'CRM', 'KO', 'WMT',
    'AMD', 'PEP', 'TMO', 'ORCL', 'ACN', 'MCD', 'LIN', 'ABT', 'CSCO', 'IBM',
    'GE', 'NOW', 'PM', 'ISRG', 'CAT', 'TXN', 'GS', 'UBER', 'INTU', 'BKNG',
    'SPGI', 'AXP', 'AMGN', 'RTX', 'PFE', 'DHR', 'NEE', 'LOW', 'UNP', 'HON',
    'SYK', 'T', 'VRTX', 'MS', 'BLK', 'ADP', 'SCHW', 'MDT', 'BA', 'GILD',
    'BSX', 'MMC', 'CB', 'C', 'DE', 'SO', 'CI', 'ELV', 'CME', 'REGN',
    'MO', 'ZTS', 'WM', 'LRCX', 'PLD', 'CL', 'EOG', 'SLB', 'BDX', 'MMM',
    'DUK', 'ITW', 'CSX', 'APD', 'NOC', 'HUM', 'PGR', 'AON', 'FDX', 'MCK'
]


# =============================================================================
# SECTION 1: LOAD STATE
# =============================================================================

def load_state():
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, 'r') as f:
            return json.load(f)
    return {
        'nav':              STARTING_NAV,
        'cash':             STARTING_NAV,
        'last_rebalance':   None,
        'total_trades':     0,
        'start_date':       str(today),
        'start_nav':        STARTING_NAV,
        'regime':           'FULL',
    }

def save_state(state):
    with open(STATE_PATH, 'w') as f:
        json.dump(state, f, indent=2)

state = load_state()
print(f'\nCurrent NAV:     ${state["nav"]:,.2f}')
print(f'Cash:            ${state["cash"]:,.2f}')
print(f'Regime:          {state.get("regime", "FULL")}')
print(f'Last rebalance:  {state["last_rebalance"] or "Never"}')


# =============================================================================
# SECTION 2: LOAD DATA FILES
# =============================================================================

PORTFOLIO_COLS = [
    'symbol', 'entry_date', 'entry_price', 'shares', 'weight',
    'current_price', 'current_value', 'unrealised_pct', 'composite_momentum'
]
TRADE_COLS = [
    'date', 'action', 'symbol', 'shares', 'price',
    'value', 'reason', 'composite_momentum'
]
NAV_COLS = [
    'date', 'nav', 'daily_return_pct', 'holdings',
    'cash', 'total_trades', 'regime'
]

def load_csv(path, cols):
    if os.path.exists(path) and os.path.getsize(path) > len(','.join(cols)):
        df = pd.read_csv(path)
        for col in cols:
            if col not in df.columns:
                df[col] = None
        return df
    return pd.DataFrame(columns=cols)

portfolio_df = load_csv(PORTFOLIO_PATH, PORTFOLIO_COLS)
trade_log_df = load_csv(TRADE_LOG_PATH, TRADE_COLS)
nav_df       = load_csv(NAV_PATH,       NAV_COLS)

print(f'Holdings:        {len(portfolio_df)} positions')


# =============================================================================
# SECTION 3: FETCH PRICE DATA
# =============================================================================

def fetch_prices(tickers, period='2y'):
    """
    Fetch prices one ticker at a time to avoid Yahoo Finance rate limiting.
    Bulk downloads from GitHub Actions are blocked; individual requests work.
    """
    print(f'\nFetching price data for {len(tickers)} tickers (individual mode)...')
    all_closes = {}
    success = 0
    failed  = 0

    for ticker in tickers:
        try:
            data = yf.Ticker(ticker).history(period=period, auto_adjust=True)
            if not data.empty and len(data) > 50:
                all_closes[ticker] = data['Close']
                success += 1
            else:
                failed += 1
        except Exception:
            failed += 1
        time.sleep(0.5)  # Respectful rate limiting

    if not all_closes:
        print(f'  ERROR: No data retrieved ({failed} failures)')
        return pd.DataFrame()

    closes = pd.DataFrame(all_closes)
    print(f'  Retrieved {len(closes)} days for {success} tickers ({failed} failed)')
    return closes


def get_current_prices(tickers):
    """Fetch latest prices individually to avoid rate limiting."""
    prices = {}
    if not tickers:
        return prices
    for ticker in tickers:
        try:
            data = yf.Ticker(ticker).history(period='5d', auto_adjust=True)
            if not data.empty:
                prices[ticker] = float(data['Close'].iloc[-1])
        except Exception:
            pass
        time.sleep(0.3)
    return prices


# =============================================================================
# SECTION 4: IMPROVEMENT 1 — MARKET REGIME DETECTION
# =============================================================================

def get_market_regime(closes):
    """
    Returns 'FULL' or 'REDUCED' based on SPY vs 200-day SMA.
    FULL = SPY above 200-day SMA — deploy full position sizes.
    REDUCED = SPY below 200-day SMA — deploy half position sizes, hold rest in cash.
    """
    if 'SPY' not in closes.columns:
        print('  SPY not in price data — defaulting to FULL regime')
        return 'FULL'

    spy = closes['SPY'].dropna()
    if len(spy) < REGIME_SMA_DAYS:
        print(f'  Insufficient SPY history ({len(spy)} days) — defaulting to FULL')
        return 'FULL'

    current_price = float(spy.iloc[-1])
    sma_200       = float(spy.tail(REGIME_SMA_DAYS).mean())
    regime        = 'FULL' if current_price > sma_200 else 'REDUCED'

    print(f'\nMarket Regime: {regime}')
    print(f'  SPY current:  ${current_price:.2f}')
    print(f'  SPY 200-SMA:  ${sma_200:.2f}')
    print(f'  Position size: {REGIME_POSITION_SIZE_FULL*100:.0f}%' if regime == 'FULL'
          else f'  Position size: {REGIME_POSITION_SIZE_REDUCED*100:.0f}% (regime filter active)')

    return regime


# =============================================================================
# SECTION 5: IMPROVEMENT 2 — COMPOSITE MOMENTUM SCORE
# =============================================================================

def calculate_composite_momentum(series):
    """
    Weighted composite of 1, 3, 6, 12-month returns.
    Returns None if insufficient data.
    """
    if len(series) < max(MOMENTUM_WEIGHTS.keys()):
        return None

    current = float(series.iloc[-1])
    score   = 0.0

    for lookback, weight in MOMENTUM_WEIGHTS.items():
        past = float(series.iloc[-lookback])
        if past <= 0:
            return None
        period_return = (current / past) - 1
        score += period_return * weight

    return score


# =============================================================================
# SECTION 6: IMPROVEMENT 3 — VOLATILITY FILTER
# =============================================================================

def calculate_realised_vol(series, window=VOL_LOOKBACK):
    """
    20-day annualised realised volatility from daily returns.
    """
    if len(series) < window + 1:
        return None
    daily_returns = series.pct_change().dropna().tail(window)
    if len(daily_returns) < window:
        return None
    return float(daily_returns.std() * np.sqrt(252))


# =============================================================================
# SECTION 7: UPDATE CURRENT PORTFOLIO PRICES
# =============================================================================

if len(portfolio_df) > 0:
    print('\nUpdating current portfolio prices...')
    held         = portfolio_df['symbol'].tolist()
    curr_prices  = get_current_prices(held)

    for idx, row in portfolio_df.iterrows():
        sym = row['symbol']
        if sym in curr_prices and pd.notna(curr_prices[sym]):
            new_price  = float(curr_prices[sym])
            new_value  = new_price * float(row['shares'])
            unrealised = (new_price - float(row['entry_price'])) / float(row['entry_price']) * 100
            portfolio_df.at[idx, 'current_price']  = round(new_price, 4)
            portfolio_df.at[idx, 'current_value']  = round(new_value, 2)
            portfolio_df.at[idx, 'unrealised_pct'] = round(unrealised, 2)
            print(f'  {sym}: ${new_price:.2f} ({unrealised:+.1f}%)')

    holdings_value = portfolio_df['current_value'].astype(float).sum()
    state['nav']   = round(float(state['cash']) + holdings_value, 2)
    print(f'\nUpdated NAV: ${state["nav"]:,.2f}')


# =============================================================================
# SECTION 8: CHECK REBALANCE
# =============================================================================

def is_rebalance_due():
    if state['last_rebalance'] is None:
        return True
    last = date.fromisoformat(state['last_rebalance'])
    if today.month != last.month and today.weekday() < 5:
        return True
    if (today - last).days > 35:
        return True
    return False

rebalance_due = is_rebalance_due()
print(f'\nRebalance due: {rebalance_due}')


# =============================================================================
# SECTION 9: MONTHLY REBALANCE WITH ALL THREE IMPROVEMENTS
# =============================================================================

new_trades = []

if rebalance_due:
    print('\n' + '=' * 60)
    print('REBALANCING — IMPROVED VERSION')
    print('=' * 60)

    # Add SPY to fetch list for regime detection
    fetch_tickers = list(set(SP100_TICKERS + ['SPY']))
    closes        = fetch_prices(fetch_tickers, period='2y')

    if closes.empty:
        print('ERROR: Could not fetch price data. Skipping rebalance.')
    else:
        # IMPROVEMENT 1: Detect market regime
        regime = get_market_regime(closes)
        state['regime'] = regime
        position_size   = (REGIME_POSITION_SIZE_FULL if regime == 'FULL'
                           else REGIME_POSITION_SIZE_REDUCED)

        # IMPROVEMENT 3: Calculate volatility for all stocks first
        vol_scores = {}
        for ticker in SP100_TICKERS:
            if ticker not in closes.columns:
                continue
            series = closes[ticker].dropna()
            vol    = calculate_realised_vol(series)
            if vol is not None:
                vol_scores[ticker] = vol

        # Volatility threshold — exclude top 20%
        if vol_scores:
            vol_threshold = np.percentile(list(vol_scores.values()), VOL_PERCENTILE * 100)
            print(f'\nVolatility filter threshold (top 20% excluded): {vol_threshold*100:.1f}% annualised')
        else:
            vol_threshold = float('inf')

        # IMPROVEMENT 2: Calculate composite momentum for all stocks
        momentum_scores = {}
        skipped_history = skipped_vol = skipped_price = 0

        for ticker in SP100_TICKERS:
            if ticker not in closes.columns:
                continue

            series = closes[ticker].dropna()

            # Price filter
            if len(series) == 0 or float(series.iloc[-1]) < MIN_PRICE:
                skipped_price += 1
                continue

            # IMPROVEMENT 3: Volatility filter
            ticker_vol = vol_scores.get(ticker, float('inf'))
            if ticker_vol > vol_threshold:
                skipped_vol += 1
                continue

            # IMPROVEMENT 2: Composite momentum
            composite = calculate_composite_momentum(series)
            if composite is None:
                skipped_history += 1
                continue

            momentum_scores[ticker] = composite

        print(f'\nUniverse after filters:')
        print(f'  Valid (composite momentum):  {len(momentum_scores)} stocks')
        print(f'  Skipped (volatility filter): {skipped_vol} stocks')
        print(f'  Skipped (history):           {skipped_history} stocks')
        print(f'  Skipped (price):             {skipped_price} stocks')

        if len(momentum_scores) < PORTFOLIO_SIZE:
            print(f'ERROR: Insufficient stocks ({len(momentum_scores)}). Skipping.')
        else:
            # Select top 5 by composite momentum
            ranked = sorted(
                momentum_scores.items(), key=lambda x: x[1], reverse=True
            )
            top5 = ranked[:PORTFOLIO_SIZE]

            print(f'\nTop 5 by composite momentum (regime: {regime}):')
            for rank, (ticker, score) in enumerate(top5, 1):
                vol_pct = vol_scores.get(ticker, 0) * 100
                print(f'  {rank}. {ticker}: composite={score*100:+.2f}%  vol={vol_pct:.1f}%')

            new_symbols     = [t for t, _ in top5]
            current_symbols = portfolio_df['symbol'].tolist() if len(portfolio_df) > 0 else []

            # Liquidate dropped positions
            for sym in current_symbols:
                if sym not in new_symbols:
                    row      = portfolio_df[portfolio_df['symbol'] == sym].iloc[0]
                    proceeds = (float(row['current_value'])
                                if pd.notna(row.get('current_value'))
                                else float(row['entry_price']) * float(row['shares']))
                    state['cash']         = round(float(state['cash']) + proceeds, 2)
                    state['total_trades'] += 1
                    new_trades.append({
                        'date':                str(today),
                        'action':              'SELL',
                        'symbol':              sym,
                        'shares':              row['shares'],
                        'price':               row.get('current_price', row['entry_price']),
                        'value':               round(proceeds, 2),
                        'reason':              'Rebalance — dropped from top 5',
                        'composite_momentum':  row.get('composite_momentum', ''),
                    })
                    print(f'\n  SELL: {sym} — dropped. Proceeds: ${proceeds:,.2f}')

            portfolio_df = portfolio_df[portfolio_df['symbol'].isin(new_symbols)].copy()

            # Buy new positions
            new_entrants = [s for s in new_symbols if s not in current_symbols]
            new_prices   = get_current_prices(new_entrants) if new_entrants else {}

            total_nav      = state['nav']
            # IMPROVEMENT 1: Position size depends on regime
            target_per_pos = (total_nav * position_size) / PORTFOLIO_SIZE

            for ticker, comp_score in top5:
                if ticker in current_symbols:
                    idx = portfolio_df[portfolio_df['symbol'] == ticker].index
                    if len(idx) > 0:
                        portfolio_df.at[idx[0], 'composite_momentum'] = round(comp_score * 100, 2)
                    continue

                price = new_prices.get(ticker)
                if not price or price <= 0:
                    try:
                        tick  = yf.Ticker(ticker).history(period='5d')
                        if not tick.empty:
                            price = float(tick['Close'].iloc[-1])
                    except Exception:
                        pass

                if not price or price <= 0:
                    print(f'  Could not get price for {ticker} — skipping')
                    continue

                shares = int(target_per_pos / float(price))
                if shares <= 0:
                    continue

                cost = shares * float(price)
                if cost > float(state['cash']):
                    shares = int(float(state['cash']) / float(price))
                    if shares <= 0:
                        continue
                    cost = shares * float(price)

                state['cash']         = round(float(state['cash']) - cost, 2)
                state['total_trades'] += 1

                portfolio_df = pd.concat([portfolio_df, pd.DataFrame([{
                    'symbol':               ticker,
                    'entry_date':           str(today),
                    'entry_price':          round(float(price), 4),
                    'shares':               shares,
                    'weight':               round(position_size / PORTFOLIO_SIZE * 100, 1),
                    'current_price':        round(float(price), 4),
                    'current_value':        round(cost, 2),
                    'unrealised_pct':       0.0,
                    'composite_momentum':   round(comp_score * 100, 2),
                }])], ignore_index=True)

                new_trades.append({
                    'date':               str(today),
                    'action':             'BUY',
                    'symbol':             ticker,
                    'shares':             shares,
                    'price':              round(float(price), 4),
                    'value':              round(cost, 2),
                    'reason':             f'Rebalance — top 5 composite ({regime} regime)',
                    'composite_momentum': round(comp_score * 100, 2),
                })
                print(f'\n  BUY: {ticker} — {shares} @ ${price:.2f} = ${cost:,.2f}')

            holdings_value      = portfolio_df['current_value'].astype(float).sum()
            state['nav']        = round(float(state['cash']) + holdings_value, 2)
            state['last_rebalance'] = str(today)

            # If regime is REDUCED, remaining cash is intentional
            if regime == 'REDUCED':
                cash_pct = float(state['cash']) / state['nav'] * 100
                print(f'\n  Regime filter: holding {cash_pct:.1f}% cash (market below 200-SMA)')

            print(f'\nPost-rebalance NAV: ${state["nav"]:,.2f}')
            print(f'Cash:               ${state["cash"]:,.2f}')

else:
    # Update regime daily even without rebalancing
    print('\nNo rebalance — updating regime check...')
    spy_data = get_current_prices(['SPY'])
    if spy_data:
        spy_history = yf.download('SPY', period='1y', auto_adjust=True, progress=False)
        if not spy_history.empty and len(spy_history) >= REGIME_SMA_DAYS:
            closes_spy  = spy_history['Close']
            current_spy = float(closes_spy.iloc[-1])
            sma_200     = float(closes_spy.tail(REGIME_SMA_DAYS).mean())
            regime      = 'FULL' if current_spy > sma_200 else 'REDUCED'
            state['regime'] = regime
            print(f'  Regime: {regime} (SPY ${current_spy:.2f} vs 200-SMA ${sma_200:.2f})')


# =============================================================================
# SECTION 10: LOG NAV SNAPSHOT
# =============================================================================

already_logged = (
    len(nav_df) > 0 and
    nav_df['date'].astype(str).str.contains(str(today)).any()
)

if not already_logged:
    prev_nav  = float(nav_df.iloc[-1]['nav']) if len(nav_df) > 0 else STARTING_NAV
    daily_ret = (state['nav'] - prev_nav) / prev_nav * 100 if prev_nav > 0 else 0

    nav_df = pd.concat([nav_df, pd.DataFrame([{
        'date':             str(today),
        'nav':              state['nav'],
        'daily_return_pct': round(daily_ret, 4),
        'holdings':         len(portfolio_df),
        'cash':             state['cash'],
        'total_trades':     state['total_trades'],
        'regime':           state.get('regime', 'FULL'),
    }])], ignore_index=True)

    print(f'\nNAV snapshot: ${state["nav"]:,.2f} ({daily_ret:+.2f}%) [{state.get("regime","FULL")}]')

if new_trades:
    trade_log_df = pd.concat(
        [trade_log_df, pd.DataFrame(new_trades)],
        ignore_index=True
    )


# =============================================================================
# SECTION 11: PERFORMANCE METRICS
# =============================================================================

total_return = (state['nav'] - STARTING_NAV) / STARTING_NAV * 100
days_running = (today - date.fromisoformat(state['start_date'])).days
cagr         = ((state['nav'] / STARTING_NAV) ** (365 / max(days_running, 1)) - 1) * 100

sharpe = max_dd = None
if len(nav_df) > 20:
    returns = nav_df['daily_return_pct'].astype(float).dropna()
    if returns.std() > 0:
        sharpe = round(((returns.mean() - 4/252) / returns.std()) * (252 ** 0.5), 3)
if len(nav_df) > 1:
    navs   = nav_df['nav'].astype(float)
    peak   = navs.expanding().max()
    max_dd = round(((navs - peak) / peak * 100).min(), 2)


# =============================================================================
# SECTION 12: REGENERATE README
# =============================================================================

current_regime = state.get('regime', 'FULL')
regime_note    = ('⚪ FULL — SPY above 200-SMA, full position sizes'
                  if current_regime == 'FULL'
                  else '🔴 REDUCED — SPY below 200-SMA, 50% position sizes, rest in cash')

holdings_rows = ''
if len(portfolio_df) > 0:
    for _, row in portfolio_df.iterrows():
        sym  = row['symbol']
        ep   = f"${float(row['entry_price']):.2f}"     if pd.notna(row.get('entry_price'))        else '—'
        cp   = f"${float(row['current_price']):.2f}"   if pd.notna(row.get('current_price'))      else '—'
        val  = f"${float(row['current_value']):,.2f}"  if pd.notna(row.get('current_value'))      else '—'
        unr  = f"{float(row['unrealised_pct']):+.1f}%" if pd.notna(row.get('unrealised_pct'))     else '—'
        mom  = f"{float(row['composite_momentum']):+.2f}%" if pd.notna(row.get('composite_momentum')) else '—'
        ed   = str(row['entry_date'])                  if pd.notna(row.get('entry_date'))          else '—'
        holdings_rows += f'| {sym} | {ed} | {ep} | {cp} | {val} | {unr} | {mom} |\n'
else:
    holdings_rows = '| — | — | — | — | — | — | — |\n'

trade_rows = ''
for _, row in trade_log_df.tail(10).iterrows():
    mom = f"{float(row['composite_momentum']):+.2f}%" if pd.notna(row.get('composite_momentum')) else '—'
    trade_rows += (f"| {row['date']} | {row['action']} | {row['symbol']} | "
                   f"{row['shares']} | ${float(row['price']):.2f} | "
                   f"${float(row['value']):,.2f} | {mom} |\n")
if not trade_rows:
    trade_rows = '| — | — | — | — | — | — | — |\n'

nav_rows = ''
for _, row in nav_df.tail(10).iterrows():
    ret    = f"{float(row['daily_return_pct']):+.2f}%" if pd.notna(row.get('daily_return_pct')) else '—'
    regime = str(row.get('regime', '—'))
    nav_rows += f"| {row['date']} | ${float(row['nav']):,.2f} | {ret} | {int(row['holdings'])} | {regime} |\n"
if not nav_rows:
    nav_rows = '| — | — | — | — | — |\n'

sharpe_str   = f'{sharpe:.3f}' if sharpe is not None else 'Insufficient data'
max_dd_str   = f'{max_dd:.1f}%' if max_dd is not None else 'Insufficient data'
last_updated = now.strftime('%Y-%m-%d %H:%M UTC')

readme = f"""# Momentum Rotation Improved
## Enhanced Large-Cap Momentum Strategy — Paper Trading Portfolio

> Improved version of the Large-Cap US Momentum Rotation Strategy.
> Running in parallel with `momentum_rotation_test` to compare performance.
> Updated automatically every day at 08:15 UTC via GitHub Actions.

**Last updated:** {last_updated}

---

## Three Improvements Over Baseline

| # | Improvement | Purpose |
|---|-------------|---------|
| 1 | **Market Regime Filter** — SPY 200-day SMA | Reduces drawdown in bear markets |
| 2 | **Composite Momentum Signal** — weighted 1/3/6/12-month | More robust signal than 12-month only |
| 3 | **Volatility Filter** — excludes top 20% most volatile | Removes names that crash hardest |

---

## Current Market Regime

**{regime_note}**

The regime filter checks SPY against its 200-day moving average daily.
When below, position sizes are halved and the rest is held in cash.

---

## Portfolio Performance

| Metric | Value |
|--------|-------|
| Starting NAV | ${STARTING_NAV:,.2f} |
| Current NAV | ${state['nav']:,.2f} |
| Total return | {total_return:+.2f}% |
| CAGR (annualised) | {cagr:+.2f}% |
| Sharpe ratio | {sharpe_str} |
| Max drawdown | {max_dd_str} |
| Total trades | {state['total_trades']} |
| Days running | {days_running} |
| Last rebalance | {state['last_rebalance'] or 'Not yet'} |
| Current regime | {current_regime} |

---

## Current Holdings

| Symbol | Entry Date | Entry Price | Current Price | Value | Unrealised | Composite Momentum |
|--------|-----------|------------|--------------|-------|------------|-------------------|
{holdings_rows}
**Cash:** ${state['cash']:,.2f}
*(Cash above normal levels indicates regime filter is active)*

---

## Recent Trades (last 10)

| Date | Action | Symbol | Shares | Price | Value | Composite Momentum |
|------|--------|--------|--------|-------|-------|-------------------|
{trade_rows}

---

## NAV History (last 10 days)

| Date | NAV | Daily Return | Holdings | Regime |
|------|-----|-------------|----------|--------|
{nav_rows}

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
"""

with open(README_PATH, 'w') as f:
    f.write(readme)

portfolio_df.to_csv(PORTFOLIO_PATH,  index=False)
nav_df.to_csv(NAV_PATH,              index=False)
trade_log_df.to_csv(TRADE_LOG_PATH,  index=False)
save_state(state)

print('\nAll data saved')
print('README updated')
print('\n' + '=' * 60)
print(f'IMPROVED MOMENTUM — COMPLETE — {today}')
print(f'  NAV:          ${state["nav"]:,.2f}')
print(f'  Total return: {total_return:+.2f}%')
print(f'  Holdings:     {len(portfolio_df)}')
print(f'  Regime:       {current_regime}')
print(f'  Rebalanced:   {rebalance_due}')
print('=' * 60)
