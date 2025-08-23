# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive Chan (缠论) trading framework implementing technical analysis based on the Chinese Chan theory. The framework supports:

- **Multi-level Chen Theory Analysis**: K-line combination, fractal identification, stroke calculation, segment identification, center calculation, and buy/sell points
- **Multiple Data Sources**: Baostock, CSV, CCXT (cryptocurrency), with extensible API
- **Trading Strategy Support**: Basic morphological buy/sell points + custom strategy framework
- **Machine Learning Integration**: Feature extraction, model training, and AutoML
- **Visualization**: Static and animated plotting with matplotlib
- **Real-time Trading**: Futu trading engine with simulation and live trading
- **Database Integration**: MySQL/SQLite for trade tracking and backtesting

## Architecture

### Core Components Hierarchy

```
CChan (Main Class)
├── KLine Analysis
│   ├── CKLine (Combined K-lines)
│   └── CKLine_Unit (Single K-line)
├── Pattern Recognition
│   ├── Bi (Strokes)
│   ├── Seg (Segments)  
│   └── ZS (Centers)
├── Buy/Sell Points
│   ├── BS_Point (Basic Points)
│   └── Custom Strategy Points
└── Analysis
    ├── Math modules (MACD, RSI, BOLL, etc.)
    └── Feature Extraction
```

### Key Classes & Components

- **CChan**: Main orchestrator, manages all levels and calculations
- **CKLine_List**: Manages K-line data for specific timeframes
- **CKLine_Unit**: Individual K-line data with OHLCV
- **CBi**: Represents a "stroke" in Chinese axis theory
- **CSeg**: Represents a "segment" in Chinese axis theory  
- **CZS**: Represents a "center" or consolidation area
- **CBS_Point**: Buy/sell point calculation based on patterns
- **CPlotDriver**: Visualization engine for static plots
- **CAnimateDriver**: Animated replay visualization

## Setup & Development

### Installation Requirements

- Python 3.11+ (required for performance)
- Dependencies: baostock, matplotlib, numpy, pandas, requests

### Common Commands

#### Basic Usage
```python
# Basic analysis
from Chan import CChan
from ChanConfig import CChanConfig
from Common.CEnum import KL_TYPE, DATA_SRC, AUTYPE

config = CChanConfig({
    "bi_strict": True,
    "trigger_step": False,
    "bs_type": "1,2,3a,3b,1p,2s",
    "plot_warning": True
})

chan = CChan(
    code="sz.000001",
    begin_time="2018-01-01",
    data_src=DATA_SRC.BAO_STOCK,
    lv_list=[KL_TYPE.K_DAY],
    config=config,
    autype=AUTYPE.QFQ
)

# Access results
bsp_points = chan[0].bs_point_lst.getSortedBspList()
stroke_list = chan[0].bi_list
```

#### Development Tasks

**Install Dependencies**
```bash
pip install -r Script/requirements.txt
```

**Run Basic Demo**
```bash
python main.py
```

**For Tests/Validation**
- The codebase appears to be research-focused without formal tests
- Use the demo files in Debug/ directory for basic validation
- Check quick_guide.md for detailed usage patterns

**Code Style**
- Use PascalCase for classes: CKLine_Unit, CChanConfig, CBS_Point
- Use lowercase_underscore for methods and variables
- Configuration is done via dictionaries to CChanConfig
- Error handling via CChanException custom exceptions

### Key Configuration Patterns

**Timeframe Types**: KL_TYPE.K_DAY, KL_TYPE.K_60M, KL_TYPE.K_30M, etc.
**Data Sources**: DATA_SRC.BAO_STOCK, DATA_SRC.CCXT, DATA_SRC.CSV
**Pric Adjustments**: AUTYPE.QFQ (forward), AUTYPE.HFQ (backward), AUTYPE.NONE

#### Adding Custom Data Source
1. Extend `CCommonStockAPI` in DataAPI/
2. Implement `get_kl_data()` method yielding CKLine_Unit objects
3. Register in CChan.GetStockAPI() method

### File Structure Patterns

- **DataAPI/**: Stock data sources (inherited from CCommonStockApi)
- **KLine/**: K-line data structures and processing
- **Bi/**: Stroke (bi) calculations and logic
- **Seg/**: Segment calculations with multiple algorithms
- **ZS/**: Center (zhongshu) calculations
- **BuySellPoint/**: Buy/sell point detection
- **Math/**: Technical indicators (MACD, RSI, BOLL, etc.)
- **Plot/**: Visualization engines
- **Debug/**: Demo and strategy examples

### Performance Considerations

- The codebase is designed for batch processing large datasets
- Heavy use of caching and optimization for full market analysis
- Minimum Python 3.11 required for 16% performance improvement
- Core calculations implemented in pure Python with NumPy optimizations

### Extension Points

**Custom Strategy Development**:
- Extend CStrategy class for custom buy/sell points
- Implement try_open/try_close methods
- Configure via CChanConfig.cbsp_strategy

**Custom Technical Indicators**:
- Add to Math/ directory following CMACD pattern
- Register in CChanConfig.GetMetricModel()

**Custom Visualization**:
- Extend CPlotDriver or CAnimateDriver
- Configure plotting via plot_config and plot_para dictionaries

### Common Pitfalls

1. **Data Consistency**: Framework enforces K-line alignment between levels
2. **Memory Usage**: Large datasets can consume significant RAM
3. **Edge Cases**: Holiday gaps and trading suspension create edge cases handled via CChanException
4. **Reproducibility**: Use CChan.toJson() for serialization

### Debugging Dev Workflow

1. Start with main.py as reference implementation
2. Use CChanConfig with print_warning=True for debugging
3. Access intermediate calculations via CChan[KL_TYPE] properties
4. For visual debugging: set trigger_step=True and use CAnimateDriver