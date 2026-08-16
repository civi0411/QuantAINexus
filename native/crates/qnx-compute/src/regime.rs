use pyo3::prelude::*;
use std::f64::NEG_INFINITY;

#[pyclass]
pub struct HMMRegimeDetector {
    n_states: usize,
    transitions: Vec<Vec<f64>>, // Log probabilities
    means: Vec<f64>,
    vars: Vec<f64>,
}

#[pymethods]
impl HMMRegimeDetector {
    #[new]
    pub fn new(n_states: usize, trans_mat: Vec<Vec<f64>>, means: Vec<f64>, vars: Vec<f64>) -> PyResult<Self> {
        // Convert transition probabilities to log scale
        let mut transitions = vec![vec![0.0; n_states]; n_states];
        for i in 0..n_states {
            for j in 0..n_states {
                transitions[i][j] = if trans_mat[i][j] > 0.0 { trans_mat[i][j].ln() } else { NEG_INFINITY };
            }
        }
        
        Ok(HMMRegimeDetector {
            n_states,
            transitions,
            means,
            vars,
        })
    }

    /// Run Viterbi algorithm to detect regimes
    pub fn detect(&self, obs: Vec<f64>) -> PyResult<Vec<usize>> {
        let n_obs = obs.len();
        if n_obs == 0 {
            return Ok(Vec::new());
        }

        // dp[t][j] stores the max log prob of sequence ending at state j at time t
        let mut dp = vec![vec![NEG_INFINITY; self.n_states]; n_obs];
        // backptr[t][j] stores the state at time t-1 that maximizes dp[t][j]
        let mut backptr = vec![vec![0; self.n_states]; n_obs];

        // Initialization at t=0
        for j in 0..self.n_states {
            let log_pi = -(self.n_states as f64).ln(); // Assume uniform initial distribution
            dp[0][j] = log_pi + self.log_gaussian_pdf(obs[0], self.means[j], self.vars[j]);
        }

        // Recursion
        for t in 1..n_obs {
            for j in 0..self.n_states {
                let mut max_log_prob = NEG_INFINITY;
                let mut best_prev_state = 0;

                for i in 0..self.n_states {
                    let prob = dp[t - 1][i] + self.transitions[i][j];
                    if prob > max_log_prob {
                        max_log_prob = prob;
                        best_prev_state = i;
                    }
                }

                dp[t][j] = max_log_prob + self.log_gaussian_pdf(obs[t], self.means[j], self.vars[j]);
                backptr[t][j] = best_prev_state;
            }
        }

        // Termination
        let mut best_final_state = 0;
        let mut max_final_prob = NEG_INFINITY;
        for j in 0..self.n_states {
            if dp[n_obs - 1][j] > max_final_prob {
                max_final_prob = dp[n_obs - 1][j];
                best_final_state = j;
            }
        }

        // Backtracking
        let mut path = vec![0; n_obs];
        path[n_obs - 1] = best_final_state;
        for t in (1..n_obs).rev() {
            path[t - 1] = backptr[t][path[t]];
        }

        Ok(path)
    }
}

impl HMMRegimeDetector {
    fn log_gaussian_pdf(&self, x: f64, mean: f64, var: f64) -> f64 {
        if var <= 0.0 {
            return NEG_INFINITY;
        }
        let std = var.sqrt();
        let diff = x - mean;
        -0.5 * (diff / std).powi(2) - (std * (2.0 * std::f64::consts::PI).sqrt()).ln()
    }
}
