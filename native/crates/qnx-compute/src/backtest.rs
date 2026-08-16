use pyo3::prelude::*;

#[pyclass]
#[derive(Clone)]
pub struct Trade {
    #[pyo3(get)]
    pub index: usize,
    #[pyo3(get)]
    pub price: f64,
    #[pyo3(get)]
    pub qty: f64,
    #[pyo3(get)]
    pub side: String,
    #[pyo3(get)]
    pub pnl: f64,
}

#[pyclass]
pub struct BacktestResult {
    #[pyo3(get)]
    pub sharpe: f64,
    #[pyo3(get)]
    pub mdd: f64,
    #[pyo3(get)]
    pub total_return: f64,
    #[pyo3(get)]
    pub equity_curve: Vec<f64>,
    #[pyo3(get)]
    pub trades: Vec<Trade>,
}

#[pyclass]
pub struct FastBacktest {
    initial_capital: f64,
    commission_pct: f64,
    slippage_pct: f64,
}

#[pymethods]
impl FastBacktest {
    #[new]
    pub fn new(initial_capital: f64, commission_pct: f64, slippage_pct: f64) -> Self {
        FastBacktest {
            initial_capital,
            commission_pct,
            slippage_pct,
        }
    }

    /// Run vectorized backtest in Rust
    pub fn run_vectorized(
        &self,
        signals: Vec<f64>, // 1.0=Buy, -1.0=Sell, 0.0=Hold
        prices: Vec<f64>,
    ) -> PyResult<BacktestResult> {
        if signals.len() != prices.len() {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "signals and prices must have same length",
            ));
        }

        let n = prices.len();
        let mut equity_curve = Vec::with_capacity(n);
        let mut trades = Vec::new();

        let mut capital = self.initial_capital;
        let mut position: f64 = 0.0;
        let mut entry_price: f64 = 0.0;
        
        let mut max_equity = capital;
        let mut mdd = 0.0_f64;

        for i in 0..n {
            let signal = signals[i];
            let price = prices[i];

            // Update equity curve based on MTM (Mark-To-Market)
            let current_equity = capital + position * (price - entry_price);
            equity_curve.push(current_equity);
            
            // Track Drawdown
            if current_equity > max_equity {
                max_equity = current_equity;
            }
            let dd = (current_equity - max_equity) / max_equity;
            if dd < mdd {
                mdd = dd;
            }

            // Signal transition logic
            if signal != 0.0 {
                // If we are flat, enter position
                if position == 0.0 {
                    let qty = (current_equity * 0.95) / price; // 95% allocation
                    let trade_value = qty * price;
                    let fee = trade_value * self.commission_pct + trade_value * self.slippage_pct;
                    
                    capital -= fee;
                    position = if signal > 0.0 { qty } else { -qty };
                    entry_price = price;
                    
                    trades.push(Trade {
                        index: i,
                        price,
                        qty: position.abs(),
                        side: if position > 0.0 { "BUY".to_string() } else { "SELL".to_string() },
                        pnl: 0.0,
                    });
                } 
                // If we have position and signal flips, reverse position
                else if (position > 0.0 && signal < 0.0) || (position < 0.0 && signal > 0.0) {
                    // Close current
                    let pnl = position * (price - entry_price);
                    let close_value = position.abs() * price;
                    let close_fee = close_value * self.commission_pct + close_value * self.slippage_pct;
                    
                    capital += pnl - close_fee;
                    
                    trades.push(Trade {
                        index: i,
                        price,
                        qty: position.abs(),
                        side: if position > 0.0 { "SELL_CLOSE".to_string() } else { "BUY_CLOSE".to_string() },
                        pnl,
                    });
                    
                    // Open new
                    let new_equity = capital;
                    let qty = (new_equity * 0.95) / price;
                    let open_value = qty * price;
                    let open_fee = open_value * self.commission_pct + open_value * self.slippage_pct;
                    
                    capital -= open_fee;
                    position = if signal > 0.0 { qty } else { -qty };
                    entry_price = price;
                    
                    trades.push(Trade {
                        index: i,
                        price,
                        qty: position.abs(),
                        side: if position > 0.0 { "BUY".to_string() } else { "SELL".to_string() },
                        pnl: 0.0,
                    });
                }
            } else if signal == 0.0 && position != 0.0 {
                // Flatten position
                let pnl = position * (price - entry_price);
                let close_value = position.abs() * price;
                let close_fee = close_value * self.commission_pct + close_value * self.slippage_pct;
                
                capital += pnl - close_fee;
                
                trades.push(Trade {
                    index: i,
                    price,
                    qty: position.abs(),
                    side: if position > 0.0 { "SELL_CLOSE".to_string() } else { "BUY_CLOSE".to_string() },
                    pnl,
                });
                
                position = 0.0;
                entry_price = 0.0;
            }
        }

        let final_equity = *equity_curve.last().unwrap_or(&self.initial_capital);
        let total_return = (final_equity - self.initial_capital) / self.initial_capital;
        
        // Very basic Sharpe estimate from returns curve
        let sharpe = crate::metrics::sharpe_ratio(equity_curve.clone(), 0.0, 252.0);

        Ok(BacktestResult {
            sharpe,
            mdd,
            total_return,
            equity_curve,
            trades,
        })
    }
}

#[pyclass]
pub struct EventDrivenBacktest {
    capital: f64,
    position: f64,
    entry_price: f64,
    commission_pct: f64,
    slippage_pct: f64,
}

#[pymethods]
impl EventDrivenBacktest {
    #[new]
    pub fn new(initial_capital: f64, commission_pct: f64, slippage_pct: f64) -> Self {
        EventDrivenBacktest {
            capital: initial_capital,
            position: 0.0,
            entry_price: 0.0,
            commission_pct,
            slippage_pct,
        }
    }

    /// Process a single tick event
    pub fn on_tick(&mut self, price: f64, signal: f64) -> PyResult<Option<Trade>> {
        if signal == 0.0 && self.position == 0.0 {
            return Ok(None);
        }

        let mut trade = None;

        if signal != 0.0 {
            if self.position == 0.0 {
                let qty = (self.capital * 0.95) / price;
                let trade_value = qty * price;
                let fee = trade_value * self.commission_pct + trade_value * self.slippage_pct;
                
                self.capital -= fee;
                self.position = if signal > 0.0 { qty } else { -qty };
                self.entry_price = price;
                
                trade = Some(Trade {
                    index: 0, // In an event-driven setup, caller should track time/index
                    price,
                    qty: self.position.abs(),
                    side: if self.position > 0.0 { "BUY".to_string() } else { "SELL".to_string() },
                    pnl: 0.0,
                });
            } else if (self.position > 0.0 && signal < 0.0) || (self.position < 0.0 && signal > 0.0) {
                // Close current
                let pnl = self.position * (price - self.entry_price);
                let close_value = self.position.abs() * price;
                let close_fee = close_value * self.commission_pct + close_value * self.slippage_pct;
                
                self.capital += pnl - close_fee;
                
                // Open new
                let new_equity = self.capital;
                let qty = (new_equity * 0.95) / price;
                let open_value = qty * price;
                let open_fee = open_value * self.commission_pct + open_value * self.slippage_pct;
                
                self.capital -= open_fee;
                self.position = if signal > 0.0 { qty } else { -qty };
                self.entry_price = price;
                
                trade = Some(Trade {
                    index: 0,
                    price,
                    qty: self.position.abs(),
                    side: if self.position > 0.0 { "REVERSE_BUY".to_string() } else { "REVERSE_SELL".to_string() },
                    pnl,
                });
            }
        } else if signal == 0.0 && self.position != 0.0 {
            let pnl = self.position * (price - self.entry_price);
            let close_value = self.position.abs() * price;
            let close_fee = close_value * self.commission_pct + close_value * self.slippage_pct;
            
            self.capital += pnl - close_fee;
            
            trade = Some(Trade {
                index: 0,
                price,
                qty: self.position.abs(),
                side: if self.position > 0.0 { "SELL_CLOSE".to_string() } else { "BUY_CLOSE".to_string() },
                pnl,
            });
            
            self.position = 0.0;
            self.entry_price = 0.0;
        }

        Ok(trade)
    }

    pub fn get_equity(&self, current_price: f64) -> f64 {
        self.capital + self.position * (current_price - self.entry_price)
    }
}
