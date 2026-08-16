use pyo3::prelude::*;
use wide::f64x4;

/// Calculates the Sharpe ratio using SIMD for high performance.
#[pyfunction]
pub fn sharpe_ratio(returns: Vec<f64>, risk_free: f64, annualization: f64) -> f64 {
    let excess: Vec<f64> = returns.iter().map(|&r| r - risk_free).collect();
    let mean = simd_mean(&excess);
    let std = simd_std(&excess, mean);
    
    if std == 0.0 {
        return 0.0;
    }
    
    (mean / std) * annualization.sqrt()
}

/// Calculates Maximum Drawdown
#[pyfunction]
pub fn max_drawdown(equity_curve: Vec<f64>) -> f64 {
    let mut peak = f64::NEG_INFINITY;
    let mut mdd = 0.0_f64;
    
    for &val in equity_curve.iter() {
        if val > peak {
            peak = val;
        }
        let dd = (val - peak) / peak;
        if dd < mdd {
            mdd = dd;
        }
    }
    
    mdd
}

// Internal SIMD helpers
fn simd_mean(data: &[f64]) -> f64 {
    let n = data.len();
    if n == 0 { return 0.0; }
    
    let chunks = data.chunks_exact(4);
    let remainder = chunks.remainder();
    
    let sum_simd = chunks.fold(f64x4::ZERO, |acc, chunk| {
        acc + f64x4::new([chunk[0], chunk[1], chunk[2], chunk[3]])
    });
    
    let mut sum = sum_simd.to_array().iter().sum::<f64>();
    for &val in remainder {
        sum += val;
    }
    
    sum / (n as f64)
}

fn simd_std(data: &[f64], mean: f64) -> f64 {
    let n = data.len();
    if n < 2 { return 0.0; }
    
    let chunks = data.chunks_exact(4);
    let remainder = chunks.remainder();
    let mean_simd = f64x4::splat(mean);
    
    let sum_sq_simd = chunks.fold(f64x4::ZERO, |acc, chunk| {
        let val = f64x4::new([chunk[0], chunk[1], chunk[2], chunk[3]]);
        let diff = val - mean_simd;
        acc + diff * diff
    });
    
    let mut sum_sq = sum_sq_simd.to_array().iter().sum::<f64>();
    for &val in remainder {
        let diff = val - mean;
        sum_sq += diff * diff;
    }
    
    (sum_sq / ((n - 1) as f64)).sqrt()
}
