use pyo3::prelude::*;
use ndarray::Array1;
use ndarray_stats::QuantileExt;

#[pyfunction]
pub fn rolling_mean(data: Vec<f64>, window: usize) -> Vec<f64> {
    let n = data.len();
    let mut out = vec![f64::NAN; n];
    
    if n < window || window == 0 {
        return out;
    }
    
    let mut sum: f64 = data[0..window].iter().sum();
    out[window - 1] = sum / (window as f64);
    
    for i in window..n {
        sum += data[i] - data[i - window];
        out[i] = sum / (window as f64);
    }
    
    out
}

#[pyfunction]
pub fn rolling_std(data: Vec<f64>, window: usize) -> Vec<f64> {
    let n = data.len();
    let mut out = vec![f64::NAN; n];
    
    if n < window || window < 2 {
        return out;
    }
    
    for i in (window - 1)..n {
        let slice = &data[(i + 1 - window)..(i + 1)];
        let mean = slice.iter().sum::<f64>() / (window as f64);
        let variance = slice.iter().map(|&x| (x - mean).powi(2)).sum::<f64>() / ((window - 1) as f64);
        out[i] = variance.sqrt();
    }
    
    out
}

#[pyfunction]
pub fn vwap(prices: Vec<f64>, volumes: Vec<f64>) -> f64 {
    let n = prices.len();
    if n == 0 || n != volumes.len() {
        return f64::NAN;
    }
    
    let mut sum_pv = 0.0;
    let mut sum_v = 0.0;
    
    for i in 0..n {
        sum_pv += prices[i] * volumes[i];
        sum_v += volumes[i];
    }
    
    if sum_v == 0.0 { f64::NAN } else { sum_pv / sum_v }
}
