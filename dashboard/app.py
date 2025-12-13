from flask import Flask, render_template, request
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import json

app = Flask(__name__)

# Set up paths to data
base_dir = Path(__file__).resolve().parents[1]
gold_dir = base_dir / "data" / "gold"

# -----------------------------
# Helper functions
# -----------------------------

def get_daily_revenue(days=10):
    orders = pd.read_csv(gold_dir / "fact_orders.csv")
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    daily = orders.groupby(orders['order_date'].dt.date)['total_amount'].sum().sort_index()
    # Get last N days
    daily = daily.tail(days)
    return daily

def get_top_products():
    orders = pd.read_csv(gold_dir / "fact_orders.csv")
    top = orders.groupby("product_id")['quantity'].sum().sort_values(ascending=False).head(10)
    return top

def get_revenue_by_location():
    orders = pd.read_csv(gold_dir / "fact_orders.csv")
    rev = orders.groupby("location")['total_amount'].sum().sort_values(ascending=False)
    return rev

# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def dashboard():
    # Get the number of days from query parameter, default to 10
    days = request.args.get('days', default=10, type=int)
    
    daily_revenue = get_daily_revenue(days)
    top_products = get_top_products()
    revenue_by_location = get_revenue_by_location()
    
    # Create plots
    # Daily Revenue Line Chart
    fig_revenue = px.line(
        x=daily_revenue.index, 
        y=daily_revenue.values,
        labels={'x': 'Date', 'y': 'Revenue (₹)'},
        title=f'Daily Revenue (Last {days} Days)'
    )
    fig_revenue.update_traces(line_color='#667eea', line_width=3)
    revenue_graph = fig_revenue.to_json()
    
    # Top Products Bar Chart
    fig_products = px.bar(
        x=top_products.index,
        y=top_products.values,
        labels={'x': 'Product ID', 'y': 'Quantity Sold'},
        title='Top 10 Products by Quantity'
    )
    fig_products.update_traces(marker_color='#2196F3')
    products_graph = fig_products.to_json()
    
    # Revenue by Location Pie Chart
    fig_location = px.pie(
        values=revenue_by_location.values,
        names=revenue_by_location.index,
        title='Revenue Distribution by Location'
    )
    location_graph = fig_location.to_json()

    return render_template("dashboard.html",
                           daily_revenue=daily_revenue.to_dict(),
                           top_products=top_products.to_dict(),
                           revenue_by_location=revenue_by_location.to_dict(),
                           revenue_graph=revenue_graph,
                           products_graph=products_graph,
                           location_graph=location_graph,
                           selected_days=days)

if __name__ == "__main__":
    app.run(debug=True)
