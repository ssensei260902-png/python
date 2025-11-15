# 📈 Stock Market Trading & Analysis with Python

## Complete Professional Guide to Algorithmic Trading

---

## Table of Contents

1. [Stock Market Data with Pandas](#1-stock-market-data-with-pandas)
2. [Technical Analysis & Indicators](#2-technical-analysis--indicators)
3. [Intraday Trading Strategies](#3-intraday-trading-strategies)
4. [Options Trading](#4-options-trading)
5. [Backtesting Framework](#5-backtesting-framework)
6. [Real-Time Trading System](#6-real-time-trading-system)
7. [Risk Management](#7-risk-management)
8. [Portfolio Optimization](#8-portfolio-optimization)
9. [Complete Trading Bots](#9-complete-trading-bots)
10. [Production Deployment](#10-production-deployment)

---

## 1. Stock Market Data with Pandas

### 1.1 Fetching Stock Data

```python
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pandas_datareader as pdr

class StockDataFetcher:
    """Professional stock data fetching and management"""

    def __init__(self):
        self.cache = {}

    def get_historical_data(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str = '1d'
    ) -> pd.DataFrame:
        """
        Fetch historical stock data
        interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        """
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start_date, end=end_date, interval=interval)

        # Clean data
        df = df.drop(columns=['Dividends', 'Stock Splits'], errors='ignore')
        df.columns = [col.lower() for col in df.columns]

        return df

    def get_live_data(self, symbol: str) -> dict:
        """Get real-time stock data"""
        ticker = yf.Ticker(symbol)
        info = ticker.info

        return {
            'symbol': symbol,
            'price': info.get('currentPrice'),
            'open': info.get('open'),
            'high': info.get('dayHigh'),
            'low': info.get('dayLow'),
            'volume': info.get('volume'),
            'previous_close': info.get('previousClose'),
            'market_cap': info.get('marketCap'),
        }

    def get_intraday_data(
        self,
        symbol: str,
        interval: str = '5m',
        days: int = 5
    ) -> pd.DataFrame:
        """Get intraday data for last N days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        return self.get_historical_data(
            symbol,
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d'),
            interval=interval
        )

    def get_multiple_stocks(
        self,
        symbols: list,
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """Get data for multiple stocks"""
        data = yf.download(symbols, start=start_date, end=end_date)

        # If single column (single stock), convert to multi-level
        if 'Close' in data.columns:
            return data

        return data

    def calculate_returns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate returns"""
        df = df.copy()

        # Daily returns
        df['returns'] = df['close'].pct_change()

        # Cumulative returns
        df['cumulative_returns'] = (1 + df['returns']).cumprod() - 1

        # Log returns
        df['log_returns'] = np.log(df['close'] / df['close'].shift(1))

        return df


# Usage Example
fetcher = StockDataFetcher()

# Get historical data
aapl = fetcher.get_historical_data('AAPL', '2023-01-01', '2024-01-01')
print(aapl.head())

# Get intraday data (5-minute intervals)
aapl_intraday = fetcher.get_intraday_data('AAPL', interval='5m', days=5)
print(aapl_intraday.tail())

# Get live data
live_data = fetcher.get_live_data('AAPL')
print(f"Current Price: ${live_data['price']}")

# Get multiple stocks
stocks = fetcher.get_multiple_stocks(
    ['AAPL', 'GOOGL', 'MSFT'],
    '2023-01-01',
    '2024-01-01'
)

# Calculate returns
aapl_with_returns = fetcher.calculate_returns(aapl)
print(f"Total Return: {aapl_with_returns['cumulative_returns'].iloc[-1]:.2%}")
```

### 1.2 Data Analysis with Pandas

```python
class StockAnalyzer:
    """Advanced stock data analysis"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def calculate_volatility(self, window: int = 20) -> pd.Series:
        """Calculate rolling volatility"""
        returns = self.df['close'].pct_change()
        volatility = returns.rolling(window=window).std() * np.sqrt(252)
        return volatility

    def detect_gaps(self, gap_threshold: float = 0.02) -> pd.DataFrame:
        """Detect gap up/down (>2% gap from previous close)"""
        self.df['gap'] = (self.df['open'] - self.df['close'].shift(1)) / self.df['close'].shift(1)

        gaps = self.df[abs(self.df['gap']) > gap_threshold].copy()
        gaps['gap_type'] = np.where(gaps['gap'] > 0, 'Gap Up', 'Gap Down')

        return gaps[['open', 'close', 'gap', 'gap_type']]

    def find_support_resistance(self, window: int = 20) -> dict:
        """Find support and resistance levels"""
        # Support: recent lows
        support = self.df['low'].rolling(window=window).min().iloc[-1]

        # Resistance: recent highs
        resistance = self.df['high'].rolling(window=window).max().iloc[-1]

        return {
            'support': support,
            'resistance': resistance,
            'current': self.df['close'].iloc[-1]
        }

    def identify_trend(self, short_window: int = 20, long_window: int = 50) -> str:
        """Identify trend using moving averages"""
        short_ma = self.df['close'].rolling(window=short_window).mean().iloc[-1]
        long_ma = self.df['close'].rolling(window=long_window).mean().iloc[-1]
        current_price = self.df['close'].iloc[-1]

        if short_ma > long_ma and current_price > short_ma:
            return "Strong Uptrend"
        elif short_ma > long_ma:
            return "Uptrend"
        elif short_ma < long_ma and current_price < short_ma:
            return "Strong Downtrend"
        else:
            return "Downtrend"

    def calculate_pivot_points(self) -> dict:
        """Calculate pivot points for intraday trading"""
        high = self.df['high'].iloc[-1]
        low = self.df['low'].iloc[-1]
        close = self.df['close'].iloc[-1]

        pivot = (high + low + close) / 3
        r1 = 2 * pivot - low
        r2 = pivot + (high - low)
        r3 = high + 2 * (pivot - low)

        s1 = 2 * pivot - high
        s2 = pivot - (high - low)
        s3 = low - 2 * (high - pivot)

        return {
            'pivot': pivot,
            'r1': r1, 'r2': r2, 'r3': r3,
            's1': s1, 's2': s2, 's3': s3
        }


# Usage
analyzer = StockAnalyzer(aapl)

# Volatility
volatility = analyzer.calculate_volatility()
print(f"Current Volatility: {volatility.iloc[-1]:.2%}")

# Detect gaps
gaps = analyzer.detect_gaps()
print(f"Number of significant gaps: {len(gaps)}")

# Support/Resistance
levels = analyzer.find_support_resistance()
print(f"Support: ${levels['support']:.2f}")
print(f"Resistance: ${levels['resistance']:.2f}")

# Trend
trend = analyzer.identify_trend()
print(f"Current Trend: {trend}")

# Pivot points (for intraday)
pivots = analyzer.calculate_pivot_points()
print(f"Pivot: ${pivots['pivot']:.2f}")
print(f"R1: ${pivots['r1']:.2f}, S1: ${pivots['s1']:.2f}")
```

---

## 2. Technical Analysis & Indicators

### 2.1 Moving Averages & Trend Indicators

```python
import pandas as pd
import numpy as np

class TechnicalIndicators:
    """Professional technical indicators"""

    @staticmethod
    def sma(data: pd.Series, period: int) -> pd.Series:
        """Simple Moving Average"""
        return data.rolling(window=period).mean()

    @staticmethod
    def ema(data: pd.Series, period: int) -> pd.Series:
        """Exponential Moving Average"""
        return data.ewm(span=period, adjust=False).mean()

    @staticmethod
    def macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """
        MACD (Moving Average Convergence Divergence)
        Returns: MACD line, Signal line, Histogram
        """
        ema_fast = TechnicalIndicators.ema(data, fast)
        ema_slow = TechnicalIndicators.ema(data, slow)

        macd_line = ema_fast - ema_slow
        signal_line = TechnicalIndicators.ema(macd_line, signal)
        histogram = macd_line - signal_line

        return pd.DataFrame({
            'macd': macd_line,
            'signal': signal_line,
            'histogram': histogram
        })

    @staticmethod
    def rsi(data: pd.Series, period: int = 14) -> pd.Series:
        """
        Relative Strength Index
        Range: 0-100 (>70 overbought, <30 oversold)
        """
        delta = data.diff()

        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    @staticmethod
    def bollinger_bands(data: pd.Series, period: int = 20, std_dev: int = 2) -> pd.DataFrame:
        """
        Bollinger Bands
        Returns: Middle band (SMA), Upper band, Lower band
        """
        middle_band = TechnicalIndicators.sma(data, period)
        std = data.rolling(window=period).std()

        upper_band = middle_band + (std * std_dev)
        lower_band = middle_band - (std * std_dev)

        return pd.DataFrame({
            'upper': upper_band,
            'middle': middle_band,
            'lower': lower_band
        })

    @staticmethod
    def stochastic_oscillator(
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        period: int = 14
    ) -> pd.DataFrame:
        """
        Stochastic Oscillator
        Range: 0-100 (>80 overbought, <20 oversold)
        """
        lowest_low = low.rolling(window=period).min()
        highest_high = high.rolling(window=period).max()

        k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
        d_percent = k_percent.rolling(window=3).mean()

        return pd.DataFrame({
            'k': k_percent,
            'd': d_percent
        })

    @staticmethod
    def atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Average True Range (Volatility indicator)
        """
        high_low = high - low
        high_close = abs(high - close.shift())
        low_close = abs(low - close.shift())

        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=period).mean()

        return atr

    @staticmethod
    def adx(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> pd.Series:
        """
        Average Directional Index (Trend strength)
        Range: 0-100 (>25 trending, <20 ranging)
        """
        plus_dm = high.diff()
        minus_dm = -low.diff()

        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm < 0] = 0

        tr = TechnicalIndicators.atr(high, low, close, period)

        plus_di = 100 * (plus_dm.rolling(window=period).mean() / tr)
        minus_di = 100 * (minus_dm.rolling(window=period).mean() / tr)

        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = dx.rolling(window=period).mean()

        return adx

    @staticmethod
    def fibonacci_retracement(high: float, low: float) -> dict:
        """Calculate Fibonacci retracement levels"""
        diff = high - low

        return {
            '0%': high,
            '23.6%': high - 0.236 * diff,
            '38.2%': high - 0.382 * diff,
            '50%': high - 0.5 * diff,
            '61.8%': high - 0.618 * diff,
            '100%': low
        }


# Usage - Complete Technical Analysis
df = fetcher.get_historical_data('AAPL', '2023-01-01', '2024-01-01')

# Add all indicators
df['sma_20'] = TechnicalIndicators.sma(df['close'], 20)
df['sma_50'] = TechnicalIndicators.sma(df['close'], 50)
df['ema_12'] = TechnicalIndicators.ema(df['close'], 12)
df['ema_26'] = TechnicalIndicators.ema(df['close'], 26)

# MACD
macd_data = TechnicalIndicators.macd(df['close'])
df = pd.concat([df, macd_data], axis=1)

# RSI
df['rsi'] = TechnicalIndicators.rsi(df['close'])

# Bollinger Bands
bb = TechnicalIndicators.bollinger_bands(df['close'])
df = pd.concat([df, bb], axis=1)

# Stochastic
stoch = TechnicalIndicators.stochastic_oscillator(df['high'], df['low'], df['close'])
df = pd.concat([df, stoch], axis=1)

# ATR
df['atr'] = TechnicalIndicators.atr(df['high'], df['low'], df['close'])

# ADX
df['adx'] = TechnicalIndicators.adx(df['high'], df['low'], df['close'])

print(df[['close', 'sma_20', 'sma_50', 'rsi', 'macd', 'adx']].tail())

# Check signals
latest = df.iloc[-1]
print(f"\n=== Latest Signals ===")
print(f"Price: ${latest['close']:.2f}")
print(f"RSI: {latest['rsi']:.2f} {'(Overbought)' if latest['rsi'] > 70 else '(Oversold)' if latest['rsi'] < 30 else ''}")
print(f"MACD: {latest['macd']:.2f} (Signal: {latest['signal']:.2f})")
print(f"ADX: {latest['adx']:.2f} {'(Trending)' if latest['adx'] > 25 else '(Ranging)'}")
```

---

## 3. Intraday Trading Strategies

### 3.1 Scalping Strategy (1-5 minute timeframe)

```python
class ScalpingStrategy:
    """High-frequency scalping strategy"""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.signals = []

    def generate_signals(self) -> pd.DataFrame:
        """
        Scalping signals using EMA crossover + RSI
        Entry: Fast EMA crosses above Slow EMA + RSI < 70
        Exit: Fast EMA crosses below Slow EMA or RSI > 70
        """
        df = self.df.copy()

        # Calculate indicators
        df['ema_fast'] = TechnicalIndicators.ema(df['close'], 5)
        df['ema_slow'] = TechnicalIndicators.ema(df['close'], 13)
        df['rsi'] = TechnicalIndicators.rsi(df['close'], 14)

        # Generate signals
        df['signal'] = 0

        # Buy signal
        buy_condition = (
            (df['ema_fast'] > df['ema_slow']) &
            (df['ema_fast'].shift(1) <= df['ema_slow'].shift(1)) &
            (df['rsi'] < 70)
        )

        # Sell signal
        sell_condition = (
            (df['ema_fast'] < df['ema_slow']) &
            (df['ema_fast'].shift(1) >= df['ema_slow'].shift(1))
        ) | (df['rsi'] > 75)

        df.loc[buy_condition, 'signal'] = 1  # Buy
        df.loc[sell_condition, 'signal'] = -1  # Sell

        return df

    def backtest(self, initial_capital: float = 10000, position_size: float = 0.1):
        """Backtest the strategy"""
        df = self.generate_signals()

        capital = initial_capital
        position = 0
        trades = []

        for i in range(len(df)):
            if df['signal'].iloc[i] == 1 and position == 0:
                # Buy
                shares = int((capital * position_size) / df['close'].iloc[i])
                if shares > 0:
                    position = shares
                    buy_price = df['close'].iloc[i]
                    trades.append({
                        'type': 'BUY',
                        'date': df.index[i],
                        'price': buy_price,
                        'shares': shares
                    })

            elif df['signal'].iloc[i] == -1 and position > 0:
                # Sell
                sell_price = df['close'].iloc[i]
                profit = (sell_price - buy_price) * position
                capital += profit

                trades.append({
                    'type': 'SELL',
                    'date': df.index[i],
                    'price': sell_price,
                    'shares': position,
                    'profit': profit
                })

                position = 0

        # Calculate performance
        total_profit = capital - initial_capital
        win_rate = len([t for t in trades if t.get('profit', 0) > 0]) / (len(trades) / 2) if trades else 0

        return {
            'final_capital': capital,
            'total_profit': total_profit,
            'return': (total_profit / initial_capital) * 100,
            'trades': trades,
            'num_trades': len(trades),
            'win_rate': win_rate * 100
        }


# Usage - Scalping on 5-minute data
intraday_data = fetcher.get_intraday_data('AAPL', interval='5m', days=5)

scalper = ScalpingStrategy(intraday_data)
results = scalper.backtest(initial_capital=10000)

print(f"=== Scalping Strategy Results ===")
print(f"Initial Capital: $10,000")
print(f"Final Capital: ${results['final_capital']:,.2f}")
print(f"Total Profit: ${results['total_profit']:,.2f}")
print(f"Return: {results['return']:.2f}%")
print(f"Number of Trades: {results['num_trades']}")
print(f"Win Rate: {results['win_rate']:.2f}%")
```

### 3.2 Breakout Strategy

```python
class BreakoutStrategy:
    """Breakout trading strategy"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def detect_breakouts(self, lookback: int = 20, volume_multiplier: float = 1.5):
        """
        Detect price and volume breakouts
        """
        df = self.df.copy()

        # Calculate resistance (highest high in lookback period)
        df['resistance'] = df['high'].rolling(window=lookback).max().shift(1)

        # Calculate support (lowest low in lookback period)
        df['support'] = df['low'].rolling(window=lookback).min().shift(1)

        # Average volume
        df['avg_volume'] = df['volume'].rolling(window=lookback).mean().shift(1)

        # Breakout signals
        df['breakout_up'] = (
            (df['close'] > df['resistance']) &
            (df['volume'] > df['avg_volume'] * volume_multiplier)
        )

        df['breakout_down'] = (
            (df['close'] < df['support']) &
            (df['volume'] > df['avg_volume'] * volume_multiplier)
        )

        return df

    def generate_signals(self):
        """Generate trading signals"""
        df = self.detect_breakouts()

        df['signal'] = 0
        df.loc[df['breakout_up'], 'signal'] = 1  # Buy
        df.loc[df['breakout_down'], 'signal'] = -1  # Sell

        # Stop loss and take profit
        df['stop_loss'] = df['close'] * 0.98  # 2% stop loss
        df['take_profit'] = df['close'] * 1.04  # 4% take profit

        return df


# Usage
breakout = BreakoutStrategy(df)
signals = breakout.generate_signals()

# Show breakouts
breakouts = signals[signals['signal'] != 0][['close', 'resistance', 'support', 'volume', 'signal']]
print(breakouts.tail())
```

### 3.3 Gap Trading Strategy

```python
class GapTradingStrategy:
    """Trade gap ups and gap downs"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def identify_gaps(self, gap_threshold: float = 0.02):
        """Identify and trade gaps"""
        df = self.df.copy()

        # Calculate gap
        df['gap'] = (df['open'] - df['close'].shift(1)) / df['close'].shift(1)

        # Classify gaps
        df['gap_type'] = 'None'
        df.loc[df['gap'] > gap_threshold, 'gap_type'] = 'Gap Up'
        df.loc[df['gap'] < -gap_threshold, 'gap_type'] = 'Gap Down'

        # Gap fill detection
        df['gap_filled'] = False

        for i in range(1, len(df)):
            if df['gap_type'].iloc[i-1] == 'Gap Up':
                # Check if gap filled (price touches previous close)
                if df['low'].iloc[i] <= df['close'].iloc[i-2]:
                    df.loc[df.index[i], 'gap_filled'] = True

            elif df['gap_type'].iloc[i-1] == 'Gap Down':
                # Check if gap filled
                if df['high'].iloc[i] >= df['close'].iloc[i-2]:
                    df.loc[df.index[i], 'gap_filled'] = True

        return df

    def gap_trading_signals(self):
        """
        Strategy: Fade the gap (bet on gap fill)
        - Gap up: Short (expect price to fall back)
        - Gap down: Long (expect price to rise back)
        """
        df = self.identify_gaps()

        df['signal'] = 0

        # Short on gap up
        df.loc[df['gap_type'] == 'Gap Up', 'signal'] = -1

        # Long on gap down
        df.loc[df['gap_type'] == 'Gap Down', 'signal'] = 1

        return df


# Usage
gap_trader = GapTradingStrategy(df)
gap_signals = gap_trader.gap_trading_signals()

gaps = gap_signals[gap_signals['gap_type'] != 'None'][['open', 'close', 'gap', 'gap_type', 'signal']]
print(gaps.tail(10))
```

---

## 4. Options Trading

### 4.1 Options Pricing & Greeks

```python
import numpy as np
from scipy.stats import norm

class OptionsPricing:
    """Black-Scholes options pricing and Greeks"""

    @staticmethod
    def black_scholes(
        S: float,  # Current stock price
        K: float,  # Strike price
        T: float,  # Time to expiration (years)
        r: float,  # Risk-free rate
        sigma: float,  # Volatility
        option_type: str = 'call'
    ) -> float:
        """
        Black-Scholes option pricing formula
        """
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        if option_type == 'call':
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:  # put
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

        return price

    @staticmethod
    def calculate_greeks(
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        option_type: str = 'call'
    ) -> dict:
        """
        Calculate option Greeks
        Delta, Gamma, Theta, Vega, Rho
        """
        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        # Delta
        if option_type == 'call':
            delta = norm.cdf(d1)
        else:
            delta = -norm.cdf(-d1)

        # Gamma (same for call and put)
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))

        # Vega (same for call and put)
        vega = S * norm.pdf(d1) * np.sqrt(T) / 100  # Per 1% change in volatility

        # Theta
        if option_type == 'call':
            theta = (
                -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                - r * K * np.exp(-r * T) * norm.cdf(d2)
            ) / 365  # Per day
        else:
            theta = (
                -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                + r * K * np.exp(-r * T) * norm.cdf(-d2)
            ) / 365  # Per day

        # Rho
        if option_type == 'call':
            rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100  # Per 1% change in rate
        else:
            rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100

        return {
            'delta': delta,
            'gamma': gamma,
            'theta': theta,
            'vega': vega,
            'rho': rho
        }

    @staticmethod
    def implied_volatility(
        option_price: float,
        S: float,
        K: float,
        T: float,
        r: float,
        option_type: str = 'call'
    ) -> float:
        """
        Calculate implied volatility using Newton-Raphson method
        """
        sigma = 0.5  # Initial guess
        max_iterations = 100
        tolerance = 1e-5

        for i in range(max_iterations):
            price = OptionsPricing.black_scholes(S, K, T, r, sigma, option_type)
            vega = OptionsPricing.calculate_greeks(S, K, T, r, sigma, option_type)['vega']

            diff = option_price - price

            if abs(diff) < tolerance:
                return sigma

            sigma = sigma + diff / (vega * 100)  # Newton-Raphson step

        return sigma


# Usage
S = 150  # Stock price
K = 155  # Strike price
T = 30 / 365  # 30 days to expiration
r = 0.05  # 5% risk-free rate
sigma = 0.25  # 25% volatility

# Price a call option
call_price = OptionsPricing.black_scholes(S, K, T, r, sigma, 'call')
print(f"Call Option Price: ${call_price:.2f}")

# Price a put option
put_price = OptionsPricing.black_scholes(S, K, T, r, sigma, 'put')
print(f"Put Option Price: ${put_price:.2f}")

# Calculate Greeks
greeks = OptionsPricing.calculate_greeks(S, K, T, r, sigma, 'call')
print(f"\n=== Option Greeks ===")
print(f"Delta: {greeks['delta']:.4f}")
print(f"Gamma: {greeks['gamma']:.4f}")
print(f"Theta: ${greeks['theta']:.2f} per day")
print(f"Vega: ${greeks['vega']:.2f} per 1% vol change")
print(f"Rho: ${greeks['rho']:.2f} per 1% rate change")

# Calculate implied volatility
market_price = 5.50
iv = OptionsPricing.implied_volatility(market_price, S, K, T, r, 'call')
print(f"\nImplied Volatility: {iv*100:.2f}%")
```

### 4.2 Options Strategies

```python
class OptionsStrategies:
    """Common options trading strategies"""

    def __init__(self, pricing_model):
        self.pricing = pricing_model

    def bull_call_spread(self, S, K_long, K_short, T, r, sigma):
        """
        Bull Call Spread: Buy call at K_long, Sell call at K_short
        Limited profit, limited risk
        """
        long_call = self.pricing.black_scholes(S, K_long, T, r, sigma, 'call')
        short_call = self.pricing.black_scholes(S, K_short, T, r, sigma, 'call')

        net_premium = long_call - short_call
        max_profit = (K_short - K_long) - net_premium
        max_loss = net_premium
        breakeven = K_long + net_premium

        return {
            'strategy': 'Bull Call Spread',
            'net_premium': net_premium,
            'max_profit': max_profit,
            'max_loss': max_loss,
            'breakeven': breakeven,
            'risk_reward': max_profit / max_loss if max_loss > 0 else float('inf')
        }

    def iron_condor(self, S, K_put_long, K_put_short, K_call_short, K_call_long, T, r, sigma):
        """
        Iron Condor: Sell put spread + Sell call spread
        Profits from low volatility (range-bound market)
        """
        # Put spread
        long_put = self.pricing.black_scholes(S, K_put_long, T, r, sigma, 'put')
        short_put = self.pricing.black_scholes(S, K_put_short, T, r, sigma, 'put')

        # Call spread
        short_call = self.pricing.black_scholes(S, K_call_short, T, r, sigma, 'call')
        long_call = self.pricing.black_scholes(S, K_call_long, T, r, sigma, 'call')

        net_credit = (short_put - long_put) + (short_call - long_call)
        max_profit = net_credit
        max_loss = (K_put_short - K_put_long) - net_credit  # Same as call spread

        return {
            'strategy': 'Iron Condor',
            'net_credit': net_credit,
            'max_profit': max_profit,
            'max_loss': max_loss,
            'profit_range': (K_put_short, K_call_short)
        }

    def straddle(self, S, K, T, r, sigma):
        """
        Long Straddle: Buy call + Buy put at same strike
        Profits from high volatility (large move in either direction)
        """
        call_price = self.pricing.black_scholes(S, K, T, r, sigma, 'call')
        put_price = self.pricing.black_scholes(S, K, T, r, sigma, 'put')

        total_cost = call_price + put_price
        upper_breakeven = K + total_cost
        lower_breakeven = K - total_cost

        return {
            'strategy': 'Long Straddle',
            'total_cost': total_cost,
            'max_loss': total_cost,
            'max_profit': 'Unlimited',
            'upper_breakeven': upper_breakeven,
            'lower_breakeven': lower_breakeven
        }

    def covered_call(self, S, K, T, r, sigma, shares=100):
        """
        Covered Call: Own stock + Sell call
        Generate income from stock holdings
        """
        stock_value = S * shares
        call_premium = self.pricing.black_scholes(S, K, T, r, sigma, 'call') * shares

        max_profit = (K - S) * shares + call_premium if K > S else call_premium
        breakeven = S - (call_premium / shares)

        return {
            'strategy': 'Covered Call',
            'stock_value': stock_value,
            'call_premium': call_premium,
            'max_profit': max_profit,
            'breakeven': breakeven,
            'capped_upside': K
        }


# Usage
strategies = OptionsStrategies(OptionsPricing)

# Bull Call Spread
spread = strategies.bull_call_spread(
    S=150, K_long=150, K_short=155, T=30/365, r=0.05, sigma=0.25
)
print(f"\n=== Bull Call Spread ===")
print(f"Net Premium: ${spread['net_premium']:.2f}")
print(f"Max Profit: ${spread['max_profit']:.2f}")
print(f"Max Loss: ${spread['max_loss']:.2f}")
print(f"Risk/Reward: {spread['risk_reward']:.2f}")

# Iron Condor
condor = strategies.iron_condor(
    S=150, K_put_long=140, K_put_short=145,
    K_call_short=155, K_call_long=160,
    T=30/365, r=0.05, sigma=0.25
)
print(f"\n=== Iron Condor ===")
print(f"Net Credit: ${condor['net_credit']:.2f}")
print(f"Max Profit: ${condor['max_profit']:.2f}")
print(f"Profit Range: ${condor['profit_range'][0]:.2f} - ${condor['profit_range'][1]:.2f}")

# Long Straddle
straddle = strategies.straddle(S=150, K=150, T=30/365, r=0.05, sigma=0.25)
print(f"\n=== Long Straddle ===")
print(f"Total Cost: ${straddle['total_cost']:.2f}")
print(f"Breakeven Range: ${straddle['lower_breakeven']:.2f} - ${straddle['upper_breakeven']:.2f}")
```

---

## 5. Backtesting Framework

### 5.1 Professional Backtesting Engine

```python
import pandas as pd
import numpy as np
from typing import Callable

class Backtester:
    """Professional backtesting framework"""

    def __init__(
        self,
        df: pd.DataFrame,
        initial_capital: float = 100000,
        commission: float = 0.001  # 0.1% per trade
    ):
        self.df = df.copy()
        self.initial_capital = initial_capital
        self.commission = commission
        self.trades = []
        self.positions = []

    def run(self, strategy_func: Callable) -> dict:
        """
        Run backtest with given strategy
        strategy_func should return signals: 1 (buy), -1 (sell), 0 (hold)
        """
        # Generate signals
        self.df = strategy_func(self.df)

        capital = self.initial_capital
        position = 0
        entry_price = 0

        equity_curve = []

        for i in range(len(self.df)):
            signal = self.df['signal'].iloc[i]
            price = self.df['close'].iloc[i]

            # Buy signal
            if signal == 1 and position == 0:
                shares = int(capital / price)
                cost = shares * price
                commission_cost = cost * self.commission

                if capital >= cost + commission_cost:
                    position = shares
                    entry_price = price
                    capital -= (cost + commission_cost)

                    self.trades.append({
                        'type': 'BUY',
                        'date': self.df.index[i],
                        'price': price,
                        'shares': shares,
                        'capital': capital
                    })

            # Sell signal
            elif signal == -1 and position > 0:
                proceeds = position * price
                commission_cost = proceeds * self.commission
                capital += (proceeds - commission_cost)

                profit = (price - entry_price) * position - (commission_cost * 2)
                profit_pct = ((price - entry_price) / entry_price) * 100

                self.trades.append({
                    'type': 'SELL',
                    'date': self.df.index[i],
                    'price': price,
                    'shares': position,
                    'profit': profit,
                    'profit_pct': profit_pct,
                    'capital': capital
                })

                position = 0
                entry_price = 0

            # Calculate current equity
            current_equity = capital + (position * price if position > 0 else 0)
            equity_curve.append(current_equity)

        # Close any open position
        if position > 0:
            price = self.df['close'].iloc[-1]
            proceeds = position * price
            capital += proceeds - (proceeds * self.commission)

        final_equity = capital
        total_return = ((final_equity - self.initial_capital) / self.initial_capital) * 100

        # Calculate metrics
        metrics = self._calculate_metrics(equity_curve)

        return {
            'initial_capital': self.initial_capital,
            'final_equity': final_equity,
            'total_return': total_return,
            'total_trades': len([t for t in self.trades if t['type'] == 'BUY']),
            'winning_trades': len([t for t in self.trades if t.get('profit', 0) > 0]),
            'losing_trades': len([t for t in self.trades if t.get('profit', 0) < 0]),
            **metrics,
            'trades': self.trades,
            'equity_curve': equity_curve
        }

    def _calculate_metrics(self, equity_curve: list) -> dict:
        """Calculate performance metrics"""
        if not equity_curve:
            return {}

        equity_series = pd.Series(equity_curve)
        returns = equity_series.pct_change().dropna()

        # Sharpe ratio (annualized)
        sharpe = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0

        # Maximum drawdown
        cummax = equity_series.cummax()
        drawdown = (equity_series - cummax) / cummax
        max_drawdown = drawdown.min() * 100

        # Win rate
        winning = [t for t in self.trades if t.get('profit', 0) > 0]
        total_closed = len([t for t in self.trades if 'profit' in t])
        win_rate = (len(winning) / total_closed * 100) if total_closed > 0 else 0

        # Average win/loss
        avg_win = np.mean([t['profit'] for t in winning]) if winning else 0
        losing = [t for t in self.trades if t.get('profit', 0) < 0]
        avg_loss = np.mean([t['profit'] for t in losing]) if losing else 0

        # Profit factor
        total_wins = sum([t['profit'] for t in winning]) if winning else 0
        total_losses = abs(sum([t['profit'] for t in losing])) if losing else 0
        profit_factor = total_wins / total_losses if total_losses > 0 else float('inf')

        return {
            'sharpe_ratio': sharpe,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor
        }


# Example Strategy Function
def moving_average_crossover_strategy(df):
    """Simple MA crossover strategy"""
    df['sma_short'] = TechnicalIndicators.sma(df['close'], 20)
    df['sma_long'] = TechnicalIndicators.sma(df['close'], 50)

    df['signal'] = 0

    # Buy when short MA crosses above long MA
    df.loc[
        (df['sma_short'] > df['sma_long']) &
        (df['sma_short'].shift(1) <= df['sma_long'].shift(1)),
        'signal'
    ] = 1

    # Sell when short MA crosses below long MA
    df.loc[
        (df['sma_short'] < df['sma_long']) &
        (df['sma_short'].shift(1) >= df['sma_long'].shift(1)),
        'signal'
    ] = -1

    return df


# Run backtest
df = fetcher.get_historical_data('AAPL', '2020-01-01', '2024-01-01')
backtester = Backtester(df, initial_capital=100000, commission=0.001)
results = backtester.run(moving_average_crossover_strategy)

print(f"\n=== Backtest Results ===")
print(f"Initial Capital: ${results['initial_capital']:,.2f}")
print(f"Final Equity: ${results['final_equity']:,.2f}")
print(f"Total Return: {results['total_return']:.2f}%")
print(f"Total Trades: {results['total_trades']}")
print(f"Win Rate: {results['win_rate']:.2f}%")
print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
print(f"Max Drawdown: {results['max_drawdown']:.2f}%")
print(f"Profit Factor: {results['profit_factor']:.2f}")
print(f"Avg Win: ${results['avg_win']:,.2f}")
print(f"Avg Loss: ${results['avg_loss']:,.2f}")
```

This is Part 1 of the Stock Market Trading module. The complete guide continues with:
- Real-time trading systems
- Risk management & position sizing
- Portfolio optimization
- Complete automated trading bots
- Production deployment on cloud platforms

This comprehensive module teaches everything from basics to running professional algorithmic trading systems! 🚀📈
