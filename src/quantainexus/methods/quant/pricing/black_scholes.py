"""
QuantAINexus — methods/quant/pricing/black_scholes.py
Black-Scholes-Merton model.
"""
import numpy as np
from scipy.stats import norm
from . import QUANT
from .._base import QuantModel

@QUANT.register_module(force=True)
class BlackScholes(QuantModel):
    def __init__(self, risk_free: float = 0.05, div_yield: float = 0.0):
        super().__init__(name="black_scholes")
        self.risk_free = risk_free
        self.div_yield = div_yield
        
    def price(self, instrument: dict) -> float:
        """
        instrument dict needs: S, K, T, sigma, type ("call" or "put")
        """
        S = instrument.get("S")
        K = instrument.get("K")
        T = instrument.get("T")
        sigma = instrument.get("sigma")
        opt_type = instrument.get("type", "call").lower()
        
        try:
            from quantainexus._native import bs_price_rs
            return bs_price_rs(S, K, T, sigma, self.risk_free, self.div_yield, opt_type)
        except ImportError:
            d1 = (np.log(S / K) + (self.risk_free - self.div_yield + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)
            
            if opt_type == "call":
                return S * np.exp(-self.div_yield * T) * norm.cdf(d1) - K * np.exp(-self.risk_free * T) * norm.cdf(d2)
            else:
                return K * np.exp(-self.risk_free * T) * norm.cdf(-d2) - S * np.exp(-self.div_yield * T) * norm.cdf(-d1)
