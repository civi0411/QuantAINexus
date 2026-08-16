use pyo3::prelude::*;

#[pyclass]
pub struct CombinatorialPurgedCV {
    n_splits: usize,
    pct_embargo: f64,
}

#[pymethods]
impl CombinatorialPurgedCV {
    #[new]
    pub fn new(n_splits: usize, pct_embargo: f64) -> Self {
        CombinatorialPurgedCV { n_splits, pct_embargo }
    }

    pub fn split(&self, n_samples: usize, event_times: Option<Vec<f64>>) -> PyResult<Vec<(Vec<usize>, Vec<usize>)>> {
        let mut splits = Vec::new();
        let group_size = n_samples / self.n_splits;
        let embargo_size = (n_samples as f64 * self.pct_embargo) as usize;
        
        let has_events = event_times.is_some();
        let ev_times = event_times.unwrap_or_default();
        
        for test_group in 0..self.n_splits {
            let test_start = test_group * group_size;
            let test_end = if test_group == self.n_splits - 1 { n_samples } else { (test_group + 1) * group_size };
            
            let mut test_idx = Vec::with_capacity(test_end - test_start);
            for i in test_start..test_end {
                test_idx.push(i);
            }
            
            let mut train_idx = Vec::with_capacity(n_samples);
            
            // Get max event time in test set if we have event times
            let max_test_event_time = if has_events && test_end > 0 {
                let mut max_t = ev_times[test_start];
                for i in test_start..test_end {
                    if ev_times[i] > max_t { max_t = ev_times[i]; }
                }
                Some(max_t)
            } else {
                None
            };
            
            for i in 0..n_samples {
                if i >= test_start && i < test_end {
                    continue; // In test set
                }
                
                // Purge overlapping events (AFML)
                if has_events {
                    let ev_t = ev_times[i];
                    // If train event ends after test starts AND train event starts before test ends
                    // Assuming index `i` is proportional to start time.
                    if ev_t >= (test_start as f64) && (i as f64) <= (test_end as f64) {
                        continue;
                    }
                    
                    // Embargo: if train event starts after test ends, but within embargo window
                    // Wait, embargo is applied after the max event time of the test set
                    if let Some(max_t) = max_test_event_time {
                        if (i as f64) > (test_end as f64) && (i as f64) <= max_t + (embargo_size as f64) {
                            continue;
                        }
                    }
                } else {
                    // Fallback to simple index-based embargo
                    if i >= test_end && i < test_end + embargo_size {
                        continue;
                    }
                }
                
                train_idx.push(i);
            }
            splits.push((train_idx, test_idx));
        }
        Ok(splits)
    }
}
