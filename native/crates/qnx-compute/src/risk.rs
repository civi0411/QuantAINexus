use pyo3::prelude::*;
use statrs::distribution::{Normal, ContinuousCDF};

#[pyclass]
pub struct RiskGate {
    max_drawdown: f64,
    max_position_pct: f64,
}

#[pymethods]
impl RiskGate {
    #[new]
    pub fn new(max_drawdown: f64, max_position_pct: f64) -> Self {
        RiskGate {
            max_drawdown,
            max_position_pct,
        }
    }
    
    /// Calculate Parametric Value at Risk (VaR)
    #[staticmethod]
    pub fn parametric_var(returns: Vec<f64>, confidence: f64) -> PyResult<f64> {
        if returns.is_empty() {
            return Ok(0.0);
        }
        
        let mean = returns.iter().sum::<f64>() / (returns.len() as f64);
        let variance = returns.iter().map(|&r| (r - mean).powi(2)).sum::<f64>() / (returns.len() as f64);
        let std_dev = variance.sqrt();
        
        if std_dev == 0.0 {
            return Ok(0.0);
        }
        
        let normal = match Normal::new(mean, std_dev) {
            Ok(n) => n,
            Err(_) => return Ok(0.0),
        };
        
        // For 95% confidence, we look at the 5th percentile (1.0 - 0.95 = 0.05)
        let alpha = 1.0 - confidence;
        let var = -normal.inverse_cdf(alpha);
        
        Ok(var)
    }
    
    /// Calculate Historical Value at Risk (VaR)
    #[staticmethod]
    pub fn historical_var(mut returns: Vec<f64>, confidence: f64) -> PyResult<f64> {
        if returns.is_empty() {
            return Ok(0.0);
        }
        
        // Sort in ascending order
        returns.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
        
        let alpha = 1.0 - confidence;
        let index = ((returns.len() as f64) * alpha).floor() as usize;
        
        let idx = if index >= returns.len() {
            returns.len() - 1
        } else {
            index
        };
        
        Ok(-returns[idx]) // Return as a positive loss value
    }
}
