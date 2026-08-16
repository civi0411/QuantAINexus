use pyo3::prelude::*;

mod fracdiff;
mod cpcv;
mod backtest;
mod orderbook;
mod risk;
mod metrics;
mod data;
mod signal;
mod regime;

#[cfg(feature = "talib")]
mod ffi;

/// A Python module implemented in Rust.
#[pymodule]
fn quantainexus_native(_py: Python, m: &PyModule) -> PyResult<()> {
    // T1: Research & ML
    m.add_class::<fracdiff::FractionalDiff>()?;
    m.add_class::<cpcv::CombinatorialPurgedCV>()?;
    
    // T2: Backtest & Metrics
    m.add_class::<backtest::FastBacktest>()?;
    m.add_class::<backtest::EventDrivenBacktest>()?;
    m.add_class::<backtest::BacktestResult>()?;
    m.add_class::<backtest::Trade>()?;
    m.add_class::<regime::HMMRegimeDetector>()?;
    m.add_function(wrap_pyfunction!(metrics::sharpe_ratio, m)?)?;
    m.add_function(wrap_pyfunction!(metrics::max_drawdown, m)?)?;
    
    // T3: Order & Risk
    m.add_class::<orderbook::OrderbookMatcher>()?;
    m.add_class::<orderbook::Fill>()?;
    m.add_class::<risk::RiskGate>()?;
    
    // T4: Data & Signal
    m.add_function(wrap_pyfunction!(data::rolling_mean, m)?)?;
    m.add_function(wrap_pyfunction!(data::rolling_std, m)?)?;
    m.add_function(wrap_pyfunction!(data::vwap, m)?)?;
    m.add_function(wrap_pyfunction!(signal::momentum_signal, m)?)?;
    m.add_function(wrap_pyfunction!(signal::cross_sectional_rank, m)?)?;
    
    // T5: FFI (Optional)
    #[cfg(feature = "talib")]
    {
        m.add_function(wrap_pyfunction!(ffi::talib::rsi, m)?)?;
        m.add_function(wrap_pyfunction!(ffi::talib::macd, m)?)?;
    }
    
    Ok(())
}
