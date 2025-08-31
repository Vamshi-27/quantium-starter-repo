# Pink Morsel Sales Dashboard

A data visualization dashboard for analyzing Soul Foods Pink Morsel sales data across different regions.

## Features

- Interactive sales visualization with regional filtering
- KPI metrics display (Total Sales, Average Daily Sales, Peak Sales)
- Price increase event marker (January 15, 2021)
- Modern dark theme interface

## Setup

1. Install dependencies:
   ```bash
   pip install pandas dash plotly
   ```

2. Run the dashboard:
   ```bash
   python app.py
   ```

3. Access the dashboard at `http://127.0.0.1:8050`

## Data Processing

The raw CSV files in the `data/` folder are processed by `process_sales_data.py` to create a formatted dataset containing only Pink Morsel sales with calculated revenue (quantity × price).

## Testing

Run tests to verify dashboard functionality:
```bash
pytest test_app.py -v
```

Tests verify:
- Header presence
- Chart visualization rendering
- Regional filter controls
- Interactive functionality
