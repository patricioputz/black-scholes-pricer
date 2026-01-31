"""
Black-Scholes Option Pricing Model
Calculates European call and put option prices
"""

import numpy as np
from scipy.stats import norm


class BlackScholes:
    """
    Black-Scholes option pricing model for European options
    """
    
    def __init__(self, S, K, T, r, sigma):
        """
        Initialize Black-Scholes parameters
        
        Parameters:
        -----------
        S : float
            Current stock price
        K : float
            Strike price
        T : float
            Time to maturity (in years)
        r : float
            Risk-free interest rate (annualized)
        sigma : float
            Volatility (annualized standard deviation)
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        
    def _d1(self):
        """Calculate d1 parameter in Black-Scholes formula"""
        return (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
    
    def _d2(self):
        """Calculate d2 parameter in Black-Scholes formula"""
        return self._d1() - self.sigma * np.sqrt(self.T)
    
    def call_price(self):
        """
        Calculate European call option price
        
        Returns:
        --------
        float : Call option price
        """
        if self.T <= 0:
            return max(0, self.S - self.K)
        
        d1 = self._d1()
        d2 = self._d2()
        
        call = self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        return call
    
    def put_price(self):
        """
        Calculate European put option price
        
        Returns:
        --------
        float : Put option price
        """
        if self.T <= 0:
            return max(0, self.K - self.S)
        
        d1 = self._d1()
        d2 = self._d2()
        
        put = self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)
        return put
    
    def delta_call(self):
        """Calculate call option delta (rate of change with respect to stock price)"""
        if self.T <= 0:
            return 1.0 if self.S > self.K else 0.0
        return norm.cdf(self._d1())
    
    def delta_put(self):
        """Calculate put option delta"""
        if self.T <= 0:
            return -1.0 if self.S < self.K else 0.0
        return norm.cdf(self._d1()) - 1
    
    def gamma(self):
        """Calculate gamma (rate of change of delta)"""
        if self.T <= 0:
            return 0.0
        return norm.pdf(self._d1()) / (self.S * self.sigma * np.sqrt(self.T))
    
    def vega(self):
        """Calculate vega (sensitivity to volatility)"""
        if self.T <= 0:
            return 0.0
        return self.S * norm.pdf(self._d1()) * np.sqrt(self.T)
    
    def theta_call(self):
        """Calculate call option theta (time decay)"""
        if self.T <= 0:
            return 0.0
        d1 = self._d1()
        d2 = self._d2()
        theta = (-self.S * norm.pdf(d1) * self.sigma / (2 * np.sqrt(self.T)) 
                 - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2))
        return theta / 365  # Convert to daily theta
    
    def theta_put(self):
        """Calculate put option theta (time decay)"""
        if self.T <= 0:
            return 0.0
        d1 = self._d1()
        d2 = self._d2()
        theta = (-self.S * norm.pdf(d1) * self.sigma / (2 * np.sqrt(self.T)) 
                 + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2))
        return theta / 365  # Convert to daily theta
    
    def rho_call(self):
        """Calculate call option rho (sensitivity to interest rate)"""
        if self.T <= 0:
            return 0.0
        return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self._d2())
    
    def rho_put(self):
        """Calculate put option rho (sensitivity to interest rate)"""
        if self.T <= 0:
            return 0.0
        return -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-self._d2())


def calculate_option_price(S, K, T, r, sigma, option_type='call'):
    """
    Convenience function to calculate option price
    
    Parameters:
    -----------
    S : float
        Current stock price
    K : float
        Strike price
    T : float
        Time to maturity (in years)
    r : float
        Risk-free interest rate
    sigma : float
        Volatility
    option_type : str
        'call' or 'put'
    
    Returns:
    --------
    float : Option price
    """
    bs = BlackScholes(S, K, T, r, sigma)
    
    if option_type.lower() == 'call':
        return bs.call_price()
    elif option_type.lower() == 'put':
        return bs.put_price()
    else:
        raise ValueError("option_type must be 'call' or 'put'")
