use pyo3::prelude::*;

#[pyfunction]
pub fn momentum_signal(prices: Vec<f64>, lookback: usize) -> Vec<f64> {
    let n = prices.len();
    let mut signals = vec![f64::NAN; n];
    
    if n <= lookback || lookback == 0 {
        return signals;
    }
    
    for i in lookback..n {
        let current = prices[i];
        let past = prices[i - lookback];
        
        if past != 0.0 {
            signals[i] = (current - past) / past;
        } else {
            signals[i] = 0.0;
        }
    }
    
    signals
}

#[pyfunction]
pub fn cross_sectional_rank(matrix: Vec<Vec<f64>>) -> Vec<Vec<f64>> {
    if matrix.is_empty() {
        return Vec::new();
    }
    
    let n_rows = matrix.len();
    let n_cols = matrix[0].len();
    let mut ranked = vec![vec![0.0; n_cols]; n_rows];
    
    for i in 0..n_rows {
        let mut row_with_idx: Vec<(usize, f64)> = matrix[i]
            .iter()
            .enumerate()
            .map(|(idx, &val)| (idx, val))
            .collect();
            
        // Sort ignoring NaNs for simplicity, placing them at the end
        row_with_idx.sort_by(|a, b| {
            if a.1.is_nan() && b.1.is_nan() {
                std::cmp::Ordering::Equal
            } else if a.1.is_nan() {
                std::cmp::Ordering::Greater
            } else if b.1.is_nan() {
                std::cmp::Ordering::Less
            } else {
                a.1.partial_cmp(&b.1).unwrap()
            }
        });
        
        let valid_count = row_with_idx.iter().filter(|(_, v)| !v.is_nan()).count();
        if valid_count > 1 {
            for (rank, &(idx, val)) in row_with_idx.iter().enumerate() {
                if !val.is_nan() {
                    // Min-max scaling to [-1.0, 1.0]
                    ranked[i][idx] = (rank as f64 / (valid_count - 1) as f64) * 2.0 - 1.0;
                } else {
                    ranked[i][idx] = f64::NAN;
                }
            }
        }
    }
    
    ranked
}
