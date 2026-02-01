# Black-Scholes Option Pricer

A Python-based application for pricing European options using the Black–Scholes model.

## Features

**Core Functionality:**
- Calculate European call and put option prices using the Black-Scholes formula
- Real-time pricing updates with interactive parameter adjustment
- Support for all standard inputs (S, K, T, r, σ)

## Technologies Used

- **Python 3.8+**: Application logic
- **NumPy**: Vectorized numerical computation
- **SciPy**: Statistical distributions
- **Streamlit**: UI layer
- **Plotly**: Visualization
- **Pandas**: Data handling

## How to Run Locally

### Prerequisites
- Python 3.8+
- pip

## Run locally

- python3 -m venv venv
- source venv/bin/activate    (macOS/Linux)
- venv\Scripts\activate           (Windows)

- pip install -r requirements.txt
- streamlit run app.py



### Basic Pricing

1. Adjust the option parameters in the left sidebar:
   - **Current Stock Price**: Current market price of the underlying asset
   - **Strike Price**: Exercise price of the option
   - **Time to Maturity**: Time remaining until expiration (in years)
   - **Volatility**: Annualized standard deviation of returns
   - **Risk-Free Rate**: Annualized risk-free interest rate

2. **Option prices, Greeks, and charts update automatically as parameters change**

### P&L Analysis

1. Enable "P&L Tracking" in the sidebar
2. Enter the purchase prices for call and put options
3. Heat maps and metrics will show profit/loss relative to purchase price
4. Green indicates profit, red indicates loss

### Heat Maps

- Visualize how option values change with different stock prices and volatilities
- Customize the ranges using the input fields above each heat map
- Hover over cells to see exact values
- Use tabs to switch between call and put options

### Payoff Diagrams

- View theoretical payoffs at expiration
- Understand breakeven points and maximum profit/loss scenarios
- Toggle between raw payoffs and P&L (if tracking enabled)

## Project Structure

```
black-scholes-pricer/
│
├── app.py                  # Main Streamlit application
├── black_scholes.py        # Black-Scholes pricing engine
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## The Black-Scholes Model

The Black-Scholes model calculates the theoretical price of European options based on:

**Call Price:**
```
C = S₀N(d₁) - Ke^(-rT)N(d₂)
```

**Put Price:**
```
P = Ke^(-rT)N(-d₂) - S₀N(-d₁)
```

Where:
- `d₁ = [ln(S₀/K) + (r + σ²/2)T] / (σ√T)`
- `d₂ = d₁ - σ√T`
- `N(x)` = Cumulative standard normal distribution

## The Greeks

The application calculates all major option Greeks:

- **Delta (Δ)**: Rate of change of option price with respect to stock price
- **Gamma (Γ)**: Rate of change of delta with respect to stock price
- **Vega (ν)**: Sensitivity to volatility changes
- **Theta (Θ)**: Time decay (daily)
- **Rho (ρ)**: Sensitivity to interest rate changes

## Limitations & Assumptions

The Black-Scholes model assumes:
- European-style options (can only be exercised at expiration)
- No dividends paid during option lifetime
- Efficient markets with no transaction costs
- Constant volatility and risk-free rate
- Log-normal distribution of stock prices

## Future Enhancements

Potential improvements to showcase additional skills:
- [ ] Add support for American options (binomial tree model)
- [ ] Monte Carlo simulation comparison

## Contact

**Patricio Putz**  
LinkedIn: https://www.linkedin.com/in/patricioputz  
GitHub: https://github.com/patricioputz

---

**Note**: This is an educational tool and should not be used for actual trading decisions. Always consult with a qualified financial advisor before making investment decisions.
