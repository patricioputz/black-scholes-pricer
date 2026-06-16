# Black-Scholes Option Pricer

European option pricing tool built with Python and Streamlit. Calculates call/put prices, all five Greeks, and renders heat maps across volatility and spot price ranges.

[![Live Demo](https://img.shields.io/badge/Live-Demo-blue?style=for-the-badge)](https://huggingface.co/spaces/patricioputz/black-scholes-pricer)

---

## Run Locally

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## Model

**Call:** `C = S₀N(d₁) - Ke^(-rT)N(d₂)`

**Put:** `P = Ke^(-rT)N(-d₂) - S₀N(-d₁)`

Where `d₁ = [ln(S₀/K) + (r + σ²/2)T] / (σ√T)` and `d₂ = d₁ - σ√T`

**Greeks:** Δ, Γ, ν, Θ (daily), ρ

Assumptions: European exercise, no dividends, constant vol and rate, log-normal returns.

---

## Structure

```
├── app.py              # Streamlit UI
├── black_scholes.py    # Pricing engine + Greeks
└── requirements.txt
```

---

**Patricio Putz** · [LinkedIn](https://www.linkedin.com/in/patricioputz) · [GitHub](https://github.com/patricioputz)
