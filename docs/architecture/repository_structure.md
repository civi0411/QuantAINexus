# QuantAINexus — Repository Structure

Tài liệu này định nghĩa cấu trúc thư mục hoàn chỉnh (Complete Directory Tree) của Framework QuantAINexus. Cấu trúc này được thiết kế để phân tách rõ ràng giữa Core System (Rust), Control Plane (Python), Data Pipeline, và Agentic System. Tất cả các file chi tiết đều được liệt kê trực tiếp trên sơ đồ cây này.

```text
QuantAINexus/
├── docs/                           # Tài liệu hệ thống (MkDocs)
│   ├── architecture/               # Các bản thiết kế hệ thống (ADR, cấu trúc)
│   ├── api/                        # API References tự sinh từ code
│   └── tutorials/                  # Hướng dẫn sử dụng (Jupyter Notebooks)
│
├── native/                         # Tầng Core Engine hiệu năng cao (Rust)
│   ├── Cargo.toml                  # Workspace Rust Cargo
│   └── crates/
│       ├── qnx-core/               # Cấu trúc cơ bản (Order, Trade, Hashing)
│       │   ├── Cargo.toml
│       │   └── src/lib.rs
│       ├── qnx-arrow/              # Cầu nối Zero-copy memory giữa Polars và Rust
│       │   ├── Cargo.toml
│       │   └── src/lib.rs
│       ├── qnx-compute/            # Thuật toán Data processing, SIMD
│       │   ├── Cargo.toml
│       │   └── src/lib.rs
│       ├── qnx-quant/              # Toán học tài chính (Pricing, Stochastic, Risk)
│       │   ├── Cargo.toml
│       │   └── src/lib.rs
│       ├── qnx-signal/             # Các chỉ báo (Technical, Alpha158)
│       │   ├── Cargo.toml
│       │   └── src/lib.rs
│       ├── qnx-backtest/           # Lõi Matching Engine và Event Queue
│       │   ├── Cargo.toml
│       │   └── src/lib.rs
│       └── qnx-py/                 # PyO3 bindings (wrap tất cả thành quantainexus._native)
│           ├── Cargo.toml
│           └── src/lib.rs
│
├── src/quantainexus/               # Tầng Control Plane (Python)
│   ├── __init__.py
│   ├── py.typed                    # Khai báo type hints
│   │
│   ├── _kernel/                    # Xương sống của hệ thống
│   │   ├── __init__.py
│   │   ├── domain/                 # Các dataclass nền tảng
│   │   │   ├── __init__.py
│   │   │   ├── order.py            # Dataclass Order (Limit, Market, Stop)
│   │   │   ├── signal.py           # Dataclass Signal từ model
│   │   │   ├── trade.py            # Khớp lệnh (Fill)
│   │   │   └── asset.py            # Đặc tả mã tài sản
│   │   ├── contracts/              # Interfaces (Protocol) bắt buộc các module khác kế thừa
│   │   │   ├── __init__.py
│   │   │   ├── agent.py            # Base Protocol cho AI Agent
│   │   │   ├── backtest_engine.py  # Base Protocol cho Backtest
│   │   │   ├── evaluator.py        # Base Protocol chấm điểm mô hình
│   │   │   ├── exec_algo.py        # Base Protocol thuật toán execution
│   │   │   ├── factor.py           # Base Protocol cho Factor (Alpha)
│   │   │   ├── labeler.py          # Base Protocol gán nhãn
│   │   │   ├── method.py           # Base Protocol cho thuật toán chính (fit/predict)
│   │   │   ├── optimizer.py        # Base Protocol tối ưu danh mục
│   │   │   ├── processor.py        # Base Protocol xử lý data
│   │   │   └── trainer.py          # Base Protocol quản lý training
│   │   ├── registry/               # Trạm trung chuyển (Plugin Registry Manager)
│   │   │   ├── __init__.py
│   │   │   └── registry.py         # Decorators @register, quản lý namespace
│   │   ├── dag/                    # Cấu trúc đồ thị chạy luồng (Directed Acyclic Graph)
│   │   │   └── __init__.py
│   │   ├── task/                   # Khai báo các loại Task nội bộ
│   │   │   └── __init__.py
│   │   ├── governance/             # Quản trị rủi ro và giới hạn cấp Kernel (Hard limits)
│   │   │   └── __init__.py
│   │   ├── runner.py               # Engine chạy DAG và Task
│   │   └── exceptions.py           # Custom Exceptions (DataMissingError...)
│   │
│   ├── interfaces/                 # Giao diện cho Platform Layer
│   │   ├── __init__.py
│   │   └── qnx.py                  # API Facade (run_backtest, train_model...)
│   │
│   ├── data/                       # Tầng Chuẩn bị dữ liệu (The Fuel)
│   │   ├── __init__.py
│   │   ├── market/                 # Kết nối dữ liệu giá
│   │   │   ├── __init__.py
│   │   │   ├── yahoo.py            # Lấy data OHLCV từ Yahoo Finance
│   │   │   └── binance.py          # Lấy orderbook/ohlcv từ Binance
│   │   ├── alternative/            # Dữ liệu thay thế
│   │   │   ├── __init__.py
│   │   │   ├── macro.py            # Dữ liệu vĩ mô (lạm phát, lãi suất)
│   │   │   └── esg/
│   │   │       └── __init__.py     # Điểm số ESG
│   │   ├── fundamental/            # Dữ liệu cơ bản
│   │   │   └── __init__.py         # Báo cáo tài chính, PE, PB
│   │   ├── synthetic/              # Tạo dữ liệu giả lập
│   │   │   └── __init__.py         # Sinh data bằng GAN/Diffusion để test
│   │   ├── pit/                    # Point-In-Time Data
│   │   │   └── __init__.py         # Xử lý data có mốc thời gian thực, chống look-ahead
│   │   ├── _schema/                # Định nghĩa Schema cho Dataset
│   │   │   └── __init__.py         # Pydantic/Pandera schema cho validation
│   │   ├── processor/              # Xử lý dữ liệu
│   │   │   ├── __init__.py
│   │   │   ├── cleaner.py          # Xử lý null, drop, fill-forward
│   │   │   ├── normalizer.py       # Z-score, MinMax
│   │   │   └── outlier.py          # Xử lý nhiễu (Winsorize)
│   │   ├── label/                  # Thuật toán gán nhãn
│   │   │   ├── __init__.py
│   │   │   ├── fixed_horizon.py    # Gán nhãn n-ngày tiếp theo
│   │   │   └── triple_barrier.py   # Phương pháp 3 rào cản (Lopez de Prado)
│   │   └── fusion/                 # Feature Store & Data join logic
│   │       ├── __init__.py
│   │       └── feature_store.py    # Tránh look-ahead bias khi join data
│   │
│   ├── methods/                    # Tầng Trí tuệ (The Brains - All in One)
│   │   ├── __init__.py
│   │   ├── _blocks/                # Các khối neural/logic block tái sử dụng (Attention, CNN block...)
│   │   │   └── __init__.py
│   │   ├── _bridges/               # Cầu nối wrap các thư viện ngoài (PyTorch Lightning, HuggingFace...)
│   │   │   └── __init__.py
│   │   ├── factors/                # Các nhân tố Quant
│   │   │   ├── __init__.py
│   │   │   ├── _base.py            # BaseFactor
│   │   │   ├── alpha158.py         # 158 yếu tố Alpha kinh điển
│   │   │   ├── technical.py        # Kỹ thuật (RSI, MACD)
│   │   │   ├── fundamental/
│   │   │   │   └── __init__.py
│   │   │   ├── cross_sectional/
│   │   │   │   ├── __init__.py
│   │   │   │   └── rank.py         # Phép toán Rank cắt ngang
│   │   │   └── combination/
│   │   │       └── __init__.py
│   │   ├── quant/                  # Toán học lượng tử
│   │   │   ├── __init__.py
│   │   │   ├── _base.py            # Base QuantModel
│   │   │   ├── stochastic/
│   │   │   │   ├── __init__.py
│   │   │   │   └── gbm.py          # Geometric Brownian Motion
│   │   │   ├── pricing/
│   │   │   │   ├── __init__.py
│   │   │   │   └── black_scholes.py
│   │   │   ├── risk/
│   │   │   │   └── __init__.py
│   │   │   ├── volatility/
│   │   │   │   └── __init__.py
│   │   │   ├── econometrics/
│   │   │   │   └── __init__.py
│   │   │   └── fixed_income/
│   │   │       └── __init__.py
│   │   ├── ml/                     # Machine Learning
│   │   │   ├── __init__.py
│   │   │   └── tree.py             # LightGBM, XGBoost
│   │   ├── dl/                     # Deep Learning
│   │   │   ├── __init__.py
│   │   │   └── time_series.py      # PyTorch Transformers, LSTM
│   │   ├── ts/                     # Thuật toán phân tích chuỗi thời gian truyền thống (ARIMA, GARCH)
│   │   │   └── __init__.py
│   │   ├── causal/                 # Mô hình Causal Inference (suy luận nhân quả)
│   │   │   └── __init__.py
│   │   ├── rl/                     # Reinforcement Learning
│   │   │   ├── __init__.py
│   │   │   └── env.py              # OpenAI Gymnasium Trading Env
│   │   └── llm/                    # Large Language Models
│   │       ├── __init__.py
│   │       └── rag/                # RAG pipeline
│   │           ├── __init__.py
│   │           ├── chunker.py      # Băm tài liệu
│   │           ├── embedder.py     # SentenceTransformer
│   │           ├── vectorstore.py  # Faiss / Chroma
│   │           ├── retriever.py    # Lấy thông tin
│   │           ├── reranker.py     # Cross-Encoder xếp hạng
│   │           └── generator.py    # Sinh câu trả lời (OpenAI)
│   │
│   ├── training/                   # Tầng Huấn luyện
│   │   ├── __init__.py
│   │   ├── base.py                 # BaseTrainer class quản lý Model & DataLoader
│   │   ├── loops/                  # Vòng lặp train
│   │   │   ├── __init__.py
│   │   │   ├── supervised.py       # Vòng lặp ML/DL cơ bản
│   │   │   ├── rl_loop.py          # Cập nhật Policy PPO
│   │   │   ├── finetune.py         # SFT cho LLM
│   │   │   ├── dpo.py              # Căn chỉnh DPO
│   │   │   ├── grpo.py             # Căn chỉnh GRPO
│   │   │   └── pretrain.py         # Pretrain từ đầu
│   │   ├── callbacks/              # Hook sự kiện
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── checkpoint.py       # Lưu model weights
│   │   │   ├── early_stopping.py   # Dừng sớm tránh Overfit
│   │   │   ├── wandb_logger.py     # Log Weights&Biases
│   │   │   └── guardian.py         # Kích hoạt an toàn
│   │   ├── loss/                   # Hàm Loss
│   │   │   ├── __init__.py
│   │   │   ├── financial.py        # Sharpe Loss, IC Loss
│   │   │   ├── ranking.py          # ListNet, RankNet
│   │   │   ├── reward.py           # Loss cho RL
│   │   │   └── standard.py         # MSE, Huber
│   │   ├── optim/                  # Trình tối ưu
│   │   │   ├── __init__.py
│   │   │   └── factory.py          # Tạo Adam, SGD, AdamW
│   │   └── sched/                  # Lịch trình học
│   │       ├── __init__.py
│   │       └── factory.py          # Tạo CosineAnnealing, StepLR
│   │
│   ├── evaluate/                   # Tầng Đánh giá & Giả lập
│   │   ├── __init__.py
│   │   ├── backtest/               # Backtest Engines
│   │   │   ├── __init__.py
│   │   │   ├── engine.py           # Base BacktestEngine
│   │   │   ├── vectorized.py       # Backtest ma trận siêu tốc (Polars)
│   │   │   ├── event_driven.py     # Backtest theo chuỗi sự kiện (Tick-by-tick)
│   │   │   ├── walk_forward.py     # Sliding window optimizer
│   │   │   └── simulation.py       # Slippage & Commission models
│   │   ├── metrics/                # Các hệ đo lường hiệu suất
│   │   │   ├── __init__.py
│   │   │   ├── registry.py         # Đăng ký metric vào thư viện
│   │   │   ├── forecasting.py      # IC, ICIR, MSE
│   │   │   ├── trading.py          # WinRate, PnL
│   │   │   ├── portfolio.py        # Sharpe, Sortino, Calmar
│   │   │   ├── risk.py             # Max Drawdown, VaR, CVaR
│   │   │   ├── statistical.py      # P-value, T-stat
│   │   │   └── llm.py              # Đo lường riêng cho LLM output
│   │   ├── explainability/         # XAI (Explainable AI)
│   │   │   └── __init__.py         # SHAP, LIME (giải thích mô hình)
│   │   └── report/                 # Tạo báo cáo (PDF, HTML)
│   │       └── __init__.py         # Sinh Quant Tear Sheet
│   │
│   ├── portfolio/                  # Tầng Quản lý Danh mục
│   │   ├── __init__.py
│   │   ├── rebalancer.py           # Logic tái cân bằng định kỳ
│   │   ├── optimizer/              # Tối ưu hoá
│   │   │   ├── __init__.py
│   │   │   ├── mvo.py              # Mean-Variance của Markowitz
│   │   │   └── hrp.py              # Hierarchical Risk Parity
│   │   ├── allocators/             # Phân bổ vốn
│   │   │   ├── __init__.py
│   │   │   └── equal_weight.py     # Chia tỷ trọng đều
│   │   └── risk/                   # Mô hình rủi ro
│   │       ├── __init__.py
│   │       └── barra.py            # Mô hình rủi ro đa nhân tố (Barra)
│   │
│   ├── execution/                  # Tầng Khớp lệnh
│   │   ├── __init__.py
│   │   ├── algos/                  # Thuật toán execution
│   │   │   ├── __init__.py
│   │   │   ├── twap.py             # Băm lệnh theo thời gian (TWAP)
│   │   │   ├── vwap.py             # Băm lệnh theo khối lượng (VWAP)
│   │   │   ├── pov.py              # Tỷ lệ phần trăm thanh khoản (POV)
│   │   │   ├── iceberg.py          # Lệnh ẩn
│   │   │   └── market_impact.py    # Đo lường tác động giá
│   │   ├── models/                 # Mô hình phụ trợ thực thi
│   │   │   └── __init__.py         # Slippage/Delay models
│   │   ├── environments/           # Môi trường chạy Live
│   │   │   └── __init__.py         # Config paper/live trading
│   │   ├── routing/                # Định tuyến lệnh tới sàn
│   │   │   └── __init__.py
│   │   └── venues/                 # Cổng kết nối sàn (Binance, IBKR, Mock)
│   │       └── __init__.py
│   │
│   ├── agents/                     # Tầng AI Tự chủ (The Autonomous Layer)
│   │   ├── __init__.py
│   │   ├── research/               # Chuyên viên nghiên cứu AI
│   │   │   └── __init__.py         # Tự động backtest và sinh chiến lược
│   │   ├── memory/                 # Bộ nhớ của AI
│   │   │   └── __init__.py         # Trí nhớ ngắn hạn, dài hạn (Vector/SQL)
│   │   ├── tools/                  # Công cụ cho Agent
│   │   │   └── __init__.py         # Trình duyệt web, Code interpreter
│   │   ├── topologies/             # Các mạng lưới Agents
│   │   │   └── __init__.py         # Swarm, Hierarchical, Sequential Network
│   │   ├── mcp/                    # Model Context Protocol
│   │   │   ├── __init__.py
│   │   │   ├── server.py           # MCP Server expose JSON tools
│   │   │   ├── tools.py            # Chuyển đổi hàm thành Agent Tool
│   │   │   └── transport.py        # Chuẩn giao tiếp
│   │   ├── a2a/                    # Agent-to-Agent Communication
│   │   │   ├── __init__.py
│   │   │   ├── card.py             # Namecard chứa capability của Agent
│   │   │   ├── task.py             # Đóng gói nhiệm vụ cho Agent khác
│   │   │   └── client.py           # Giao thức truyền tin P2P
│   │   ├── personas/               # Các chức danh AI (Prompt & Behavior)
│   │   │   └── __init__.py
│   │   └── _state/                 # Quản lý State Graph (LangGraph)
│   │       └── __init__.py
│   │
│   ├── observability/              # Tầng Theo dõi & Cảnh báo
│   │   ├── __init__.py
│   │   ├── logger.py               # Standard/JSON logging
│   │   ├── experiment.py           # Experiment Tracker (lưu model, config, artifacts)
│   │   ├── metrics_collector.py    # Ghi nhận CPU, RAM usage
│   │   ├── drift.py                # Phát hiện data drift
│   │   └── alert.py                # Cảnh báo rủi ro (Telegram, Slack)
│   │
│   └── storage/                    # Tầng Lưu trữ nội bộ
│       ├── __init__.py
│       ├── artifact_store/         # Lưu Model weights, Scalers
│       │   └── __init__.py
│       ├── metadata_store/         # Lưu JSON Logs của đợt chạy
│       │   └── __init__.py
│       ├── local_disk/             # Parquet/Arrow store
│       │   └── __init__.py
│       └── s3_connector.py         # Kết nối Cloud Storage
│
├── tests/                          # Tầng Kiểm thử (Pytest / Cargo test)
├── examples/                       # Các kịch bản chạy mẫu (Sample Scripts)
├── config/                         # Schema Validator (Pydantic) cho hệ thống Platform
├── pyproject.toml                  # Cấu hình dự án Python
└── requirements.txt                # Các thư viện phụ thuộc
```
