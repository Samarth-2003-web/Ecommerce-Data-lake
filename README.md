# E-Commerce Data Lake Project

A data pipeline and analytics dashboard for e-commerce data.

## Project Structure

```
ecommerce-data-lake/
├── data/
│   ├── bronze/          # Raw data
│   ├── silver/          # Cleaned data
│   └── gold/            # Dimensional model
├── etl/
│   ├── etl_explore.py   # Data cleaning pipeline
│   └── etl_dimensions.py # Dimension table creation
└── dashboard/
    ├── app.py           # Flask dashboard
    └── templates/
        └── dashboard.html
```

## Features

- **Data Pipeline**: Bronze → Silver → Gold layer architecture
- **ETL Processing**: Data cleaning and transformation
- **Dimensional Modeling**: Fact and dimension tables
- **Interactive Dashboard**: Flask web app with Plotly visualizations
  - Daily revenue trends (last 10 days)
  - Top 10 products by quantity
  - Revenue distribution by location

## Setup

1. Install dependencies:
```bash
pip install pandas flask plotly openpyxl pyarrow
```

2. Run the ETL pipeline:
```bash
python etl/etl_explore.py
python etl/etl_dimensions.py
```

3. Start the dashboard:
```bash
cd dashboard
python app.py
```

4. Open http://127.0.0.1:5000 in your browser

## Technologies

- Python
- Pandas
- Flask
- Plotly
- Parquet
