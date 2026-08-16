from enum import Enum, auto

class TaskType(Enum):
    """Mục đích của pipeline — quyết định validation rules + output format."""
    FORECASTING = auto()        # Time-series prediction → IC, RMSE
    TRADING = auto()            # Signal → Order → PnL → Sharpe, MDD
    PORTFOLIO = auto()          # Multi-asset allocation → Risk-adjusted return
    RESEARCH = auto()           # Factor mining, model selection
    FACTOR_MINING = auto()      # Autonomous factor generation (RD-Agent style)
    PRETRAIN = auto()           # Foundation model pretraining
    FINE_TUNE = auto()          # LLM/DL fine-tuning (SFT, DPO, GRPO)
    BACKTEST = auto()           # Historical simulation
    PAPER_TRADING = auto()      # Live data, mock execution
    LIVE_TRADING = auto()       # Real money
