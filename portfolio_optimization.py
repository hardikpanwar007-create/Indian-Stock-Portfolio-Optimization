import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')



stocks = {
    'Reliance': 'RELIANCE.NS',
    'TCS': 'TCS.NS',
    'HDFC Bank': 'HDFCBANK.NS',
    'ITC': 'ITC.NS',
    'Sun Pharma': 'SUNPHARMA.NS'
}

print("Downloading stock data...")
raw_data = yf.download(
    list(stocks.values()),
    start='2022-01-01',
    end='2024-12-31',
    auto_adjust=True
)

prices = raw_data['Close']
prices.columns = list(stocks.keys())

print(f"\nData downloaded successfully!")
print(f"Shape: {prices.shape}")
print(f"Date range: {prices.index[0].date()} to {prices.index[-1].date()}")
print(f"\nMissing values:")
print(prices.isnull().sum())

prices.to_csv('stock_prices.csv')
print("\nStock prices saved ✅")



returns = prices.pct_change().dropna()

print("\n--- ANNUAL RETURNS ---")
annual_returns = returns.mean() * 252
for stock, ret in annual_returns.items():
    print(f"{stock}: {ret:.2%}")

print("\n--- ANNUAL VOLATILITY (RISK) ---")
annual_volatility = returns.std() * np.sqrt(252)
for stock, vol in annual_volatility.items():
    print(f"{stock}: {vol:.2%}")

print("\n--- CORRELATION MATRIX ---")
correlation = returns.corr()
print(correlation.round(3))

covariance = returns.cov() * 252

returns.to_csv('stock_returns.csv')
print("\nReturns saved to stock_returns.csv ✅")



print("\nRunning Monte Carlo Simulation...")
print("Generating 10,000 random portfolios...")

num_stocks = len(stocks)
num_portfolios = 10000
risk_free_rate = 0.065  # India 10Y bond yield ~6.5%

# Arrays to store results
port_returns = np.zeros(num_portfolios)
port_volatility = np.zeros(num_portfolios)
port_sharpe = np.zeros(num_portfolios)
port_weights = np.zeros((num_portfolios, num_stocks))

# Generate random portfolios
for i in range(num_portfolios):
    # Random weights
    weights = np.random.random(num_stocks)
    weights = weights / np.sum(weights)  # normalize to sum to 1

    # Portfolio return
    p_return = np.dot(weights, annual_returns)

    # Portfolio volatility
    p_volatility = np.sqrt(
        np.dot(weights.T, np.dot(covariance, weights))
    )

    # Sharpe ratio
    p_sharpe = (p_return - risk_free_rate) / p_volatility

    port_returns[i] = p_return
    port_volatility[i] = p_volatility
    port_sharpe[i] = p_sharpe
    port_weights[i] = weights

print(f"Simulation complete! ✅")
print(f"Return range: {port_returns.min():.2%} to {port_returns.max():.2%}")
print(f"Risk range: {port_volatility.min():.2%} to {port_volatility.max():.2%}")
print(f"Sharpe range: {port_sharpe.min():.2f} to {port_sharpe.max():.2f}")



# Portfolio with Maximum Sharpe Ratio
max_sharpe_idx = np.argmax(port_sharpe)
max_sharpe_return = port_returns[max_sharpe_idx]
max_sharpe_vol = port_volatility[max_sharpe_idx]
max_sharpe_weights = port_weights[max_sharpe_idx]

# Portfolio with Minimum Volatility
min_vol_idx = np.argmin(port_volatility)
min_vol_return = port_returns[min_vol_idx]
min_vol_vol = port_volatility[min_vol_idx]
min_vol_weights = port_weights[min_vol_idx]

print("\n--- MAXIMUM SHARPE RATIO PORTFOLIO ---")
print(f"Expected Return: {max_sharpe_return:.2%}")
print(f"Expected Risk: {max_sharpe_vol:.2%}")
print(f"Sharpe Ratio: {port_sharpe[max_sharpe_idx]:.2f}")
print("\nOptimal Weights:")
for stock, weight in zip(stocks.keys(), max_sharpe_weights):
    print(f"  {stock}: {weight:.2%}")

print("\n--- MINIMUM VOLATILITY PORTFOLIO ---")
print(f"Expected Return: {min_vol_return:.2%}")
print(f"Expected Risk: {min_vol_vol:.2%}")
print(f"Sharpe Ratio: {port_sharpe[min_vol_idx]:.2f}")
print("\nOptimal Weights:")
for stock, weight in zip(stocks.keys(), min_vol_weights):
    print(f"  {stock}: {weight:.2%}")



print("\nGenerating Efficient Frontier chart...")

fig, ax = plt.subplots(1, 1, figsize=(12, 8))

# Plot all random portfolios
scatter = ax.scatter(
    port_volatility,
    port_returns,
    c=port_sharpe,
    cmap='viridis',
    alpha=0.5,
    s=10
)

# Add colorbar
plt.colorbar(scatter, ax=ax, label='Sharpe Ratio')

# Plot Maximum Sharpe Portfolio
ax.scatter(
    max_sharpe_vol,
    max_sharpe_return,
    color='red',
    marker='*',
    s=500,
    zorder=5,
    label=f'Max Sharpe ({port_sharpe[max_sharpe_idx]:.2f})'
)

# Plot Minimum Volatility Portfolio
ax.scatter(
    min_vol_vol,
    min_vol_return,
    color='green',
    marker='*',
    s=500,
    zorder=5,
    label=f'Min Volatility'
)

# Plot individual stocks
for stock, ret, vol in zip(
    stocks.keys(),
    annual_returns,
    annual_volatility
):
    ax.scatter(vol, ret, marker='D', s=100, zorder=5)
    ax.annotate(
        stock,
        (vol, ret),
        textcoords="offset points",
        xytext=(10, 5),
        fontsize=9
    )

# Formatting
ax.set_xlabel('Annual Volatility (Risk)', fontsize=12)
ax.set_ylabel('Annual Return', fontsize=12)
ax.set_title(
    'Efficient Frontier — Indian Stock Portfolio Optimization\n'
    'Markowitz Model | 10,000 Random Portfolios',
    fontsize=14,
    fontweight='bold'
)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_facecolor('#f8f9fa')
fig.patch.set_facecolor('white')

plt.tight_layout()
plt.savefig('efficient_frontier.png', dpi=150, bbox_inches='tight')
plt.show()
print("Efficient Frontier saved as efficient_frontier.png ✅")


print("\nExporting results to Excel...")

with pd.ExcelWriter('portfolio_optimization_results.xlsx',
                     engine='openpyxl') as writer:

    # Sheet 1 — Stock Prices
    prices.to_excel(writer, sheet_name='Stock_Prices')

    # Sheet 2 — Daily Returns
    returns.to_excel(writer, sheet_name='Daily_Returns')

    # Sheet 3 — Annual Statistics
    stats = pd.DataFrame({
        'Annual Return': annual_returns,
        'Annual Volatility': annual_volatility,
        'Sharpe Ratio': (annual_returns - risk_free_rate) / annual_volatility
    })
    stats.to_excel(writer, sheet_name='Stock_Statistics')

    # Sheet 4 — Correlation Matrix
    correlation.to_excel(writer, sheet_name='Correlation_Matrix')

    # Sheet 5 — Optimal Portfolios
    optimal = pd.DataFrame({
        'Max Sharpe Portfolio': max_sharpe_weights,
        'Min Volatility Portfolio': min_vol_weights
    }, index=list(stocks.keys()))
    optimal.to_excel(writer, sheet_name='Optimal_Portfolios')

    # Sheet 6 — All Simulated Portfolios
    sim_df = pd.DataFrame({
        'Return': port_returns,
        'Volatility': port_volatility,
        'Sharpe Ratio': port_sharpe
    })
    for i, stock in enumerate(stocks.keys()):
        sim_df[f'Weight_{stock}'] = port_weights[:, i]
    sim_df.to_excel(writer, sheet_name='Simulation_Results')

print("Excel file saved ✅")
print("\n✅ Portfolio Optimization Complete!")
print("=" * 50)
print(f"Files generated:")
print(f"  1. stock_prices.csv")
print(f"  2. stock_returns.csv")
print(f"  3. efficient_frontier.png")
print(f"  4. portfolio_optimization_results.xlsx")