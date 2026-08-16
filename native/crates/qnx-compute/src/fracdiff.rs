use pyo3::prelude::*;

#[pyclass]
pub struct FractionalDiff {
    d: f64,
}

#[pymethods]
impl FractionalDiff {
    #[new]
    pub fn new(d: f64) -> Self {
        FractionalDiff { d }
    }

    /// Apply fractional differentiation using Fixed-Width Window (FFD)
    pub fn diff(&self, series: Vec<f64>) -> PyResult<Vec<f64>> {
        self.diff_with_threshold(series, 1e-5)
    }

    pub fn diff_with_threshold(&self, series: Vec<f64>, tau: f64) -> PyResult<Vec<f64>> {
        let w = self.get_weights_ffd(tau);
        let n = series.len();
        let w_len = w.len();
        
        let mut diff_series = vec![f64::NAN; n]; // NaN for elements before window is filled
        
        if n < w_len {
            return Ok(diff_series);
        }
        
        for i in (w_len - 1)..n {
            let mut sum = 0.0;
            for (k, &weight) in w.iter().enumerate() {
                sum += weight * series[i - k];
            }
            diff_series[i] = sum;
        }
        
        Ok(diff_series)
    }

    /// Process a panel of series in parallel
    pub fn diff_panel(&self, panel: Vec<Vec<f64>>, tau: Option<f64>) -> PyResult<Vec<Vec<f64>>> {
        let t = tau.unwrap_or(1e-5);
        let w = self.get_weights_ffd(t);
        let w_len = w.len();
        
        use rayon::prelude::*;
        let result: Vec<Vec<f64>> = panel.into_par_iter().map(|series| {
            let n = series.len();
            let mut diff_series = vec![f64::NAN; n];
            
            if n >= w_len {
                for i in (w_len - 1)..n {
                    let mut sum = 0.0;
                    for (k, &weight) in w.iter().enumerate() {
                        sum += weight * series[i - k];
                    }
                    diff_series[i] = sum;
                }
            }
            diff_series
        }).collect();
        
        Ok(result)
    }

    #[staticmethod]
    pub fn find_min_d(_series: Vec<f64>) -> PyResult<f64> {
        // Dummy grid search for minimum d that achieves stationarity
        Ok(0.35)
    }
}

impl FractionalDiff {
    fn get_weights_ffd(&self, tau: f64) -> Vec<f64> {
        let mut w = vec![1.0];
        let mut k = 1;
        
        loop {
            let next_w = -w[k - 1] * (self.d - (k as f64) + 1.0) / (k as f64);
            if next_w.abs() < tau {
                break;
            }
            w.push(next_w);
            k += 1;
        }
        
        w
    }
}
