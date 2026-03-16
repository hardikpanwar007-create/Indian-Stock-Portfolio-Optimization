# 📈 Indian Stock Portfolio Optimization
## Markowitz Model | Efficient Frontier | Sharpe Ratio Maximization

> **A Quantitative Finance project** implementing Harry Markowitz's Modern Portfolio Theory on 5 Indian NSE-listed stocks — optimizing portfolio weights to maximize Sharpe Ratio and minimize volatility using Python, Monte Carlo Simulation and the Efficient Frontier.

---

## 📌 Project Overview

This project applies **Modern Portfolio Theory (MPT)** — the Nobel Prize winning framework developed by Harry Markowitz — to construct an optimal portfolio of 5 Indian stocks. Using 3 years of real market data, the model identifies the ideal allocation that maximizes return per unit of risk.

### Three Core Outputs

| Output | Description |
| 📊 Efficient Frontier | Visual curve of all possible portfolio combinations |
| 🏆 Maximum Sharpe Portfolio | Optimal risk-return portfolio |
| 🛡️ Minimum Volatility Portfolio | Safest possible portfolio |

---

## 🎯 Stocks Analysed

| Stock | Sector | Ticker |
| Reliance Industries | Conglomerate | RELIANCE.NS |
| TCS | IT Services | TCS.NS |
| HDFC Bank | Banking | HDFCBANK.NS |
| ITC | FMCG | ITC.NS |
| Sun Pharma | Pharma | SUNPHARMA.NS |

> Stocks deliberately chosen from different sectors for maximum diversification benefit!

---

## 📈 Key Results

### Individual Stock Performance (FY2022-FY2024)

| Stock | Annual Return | Annual Risk | Risk-Return |
| TCS | 32.54% | 19.14% | 🏆 Best |
| ITC | 30.19% | 19.35% | ⭐ Strong |
| Reliance | 9.01% | 21.89% | ⚠️ Weak |
| Sun Pharma | 7.43% | 20.94% | ⚠️ Weak |
| HDFC Bank | 5.89% | 22.62% | ❌ Poor |

---

### 🏆 Maximum Sharpe Ratio Portfolio

> Best risk-adjusted return — maximizes return per unit of risk

| Metric | Value |
| Expected Annual Return | 29.26% |
| Expected Annual Risk | 14.28% |
| Sharpe Ratio | 1.59 |

**Optimal Weights:**

| Stock | Weight |
| TCS | 51.35% |
| ITC | 39.02% |
| Reliance | 4.48% |
| Sun Pharma | 4.31% |
| HDFC Bank | 0.85% |

---

### 🛡️ Minimum Volatility Portfolio

> Safest portfolio — minimizes risk regardless of return

| Metric | Value |
| Expected Annual Return | 20.60% |
| Expected Annual Risk | 12.81% |
| Sharpe Ratio | 1.10 |

**Optimal Weights:**

| Stock | Weight |
| TCS | 29.46% |
| ITC | 24.64% |
| Sun Pharma | 20.43% |
| Reliance | 17.90% |
| HDFC Bank | 7.57% |

---

## 🔍 Correlation Matrix

| Reliance | 1.000 | 0.183 | 0.347 | 0.165 | 0.262 |
| TCS | 0.183 | 1.000 | 0.303 | 0.226 | 0.186 |
| HDFC Bank | 0.347 | 0.303 | 1.000 | 0.248 | 0.299 |
| ITC | 0.165 | 0.226 | 0.248 | 1.000 | 0.244 |
| Sun Pharma | 0.262 | 0.186 | 0.299 | 0.244 | 1.000 |

> All correlations below 0.35 — confirming strong diversification benefit across sectors! ✅

---

## 💡 Key Insights

- 📊 **TCS + ITC dominate** the optimal portfolio — together comprising 90% of Max Sharpe allocation due to superior risk-adjusted returns
- 🔄 **Low correlations** across all pairs confirm sector diversification effectively reduces portfolio risk
- 📉 **Risk reduction** — Max Sharpe portfolio achieves 14.28% risk vs 22.62% for the riskiest individual stock (HDFC Bank)
- 🎯 **Sharpe Ratio of 1.59** — significantly above the 1.0 threshold considered excellent in portfolio management
- ⚖️ **Minimum Volatility portfolio** is more diversified — spreading across all 5 stocks vs concentrated Max Sharpe

---

## 🧮 Methodology

### 1. Data Collection
- Source: Yahoo Finance via `yfinance` library
- Period: January 2022 — December 2024
- Frequency: Daily closing prices
- Total observations: 738 trading days

### 2. Returns Calculation
```python
# Daily returns
returns = prices.pct_change().dropna()

# Annualised returns
annual_returns = returns.mean() * 252

# Annualised volatility
annual_volatility = returns.std() * np.sqrt(252)
```

### 3. Monte Carlo Simulation
```python
# Generate 10,000 random portfolios
num_portfolios = 10,000
results = np.zeros((3, num_portfolios))

for i in range(num_portfolios):
    weights = np.random.random(5)
    weights /= np.sum(weights)
    # Calculate portfolio return, risk, Sharpe
```

### 4. Optimization
```python
# Maximize Sharpe Ratio
def neg_sharpe(weights):
    ret = np.sum(returns.mean() * weights) * 252
    vol = np.sqrt(weights.T @ cov_matrix @ weights)
    return -(ret - risk_free_rate) / vol

# Minimize Volatility
def portfolio_volatility(weights):
    return np.sqrt(weights.T @ cov_matrix @ weights)
```

---

## 🛠️ Tools & Libraries

| Python 3.11 | Core programming language |
| `yfinance` | Real-time NSE stock data download |
| `pandas` | Data manipulation and analysis |
| `numpy` | Matrix operations and math |
| `matplotlib` | Efficient Frontier visualization |
| `scipy` | Portfolio optimization solver |
| `openpyxl` | Excel output generation |

---

## 💡 Skills Demonstrated

- ✅ Quantitative Finance — Modern Portfolio Theory
- ✅ Python Programming — data analysis & optimization
- ✅ Monte Carlo Simulation — 10,000 portfolio simulations
- ✅ Mathematical Optimization — Sharpe Ratio maximization
- ✅ Financial Data Analysis — real NSE market data
- ✅ Data Visualization — Efficient Frontier chart
- ✅ Excel Integration — automated results export

---

## 📚 Theory Background

### Modern Portfolio Theory (Markowitz, 1952)
> *"Diversification is the only free lunch in finance"* — Harry Markowitz

Key principles:
- **Expected Return** = Weighted average of individual stock returns
- **Portfolio Risk** = Not just weighted average — correlation between stocks reduces total risk!
- **Efficient Frontier** = Set of optimal portfolios — maximum return for each level of risk
- **Sharpe Ratio** = (Return - Risk Free Rate) / Volatility — measures return per unit of risk

---

## 👤 Author

**Hardik Parmar**
📧 hardikpanwar007@gmail.com
🔗 [LinkedIn](www.linkedin.com/in/hardiksinghparmar)

---

> *BSc Mathematics & Economics | Passionate about Quantitative Finance & Investment Banking*
> *Data Source: Yahoo Finance via yfinance | For educational purposes only*
