# ============================================
# 📦 E-commerce Dashboard Project (Streamlit)
# ============================================

import pandas as pd
import streamlit as st
import plotly.express as px

# ---------------------------
# Step 1: Load dataset from CSV
# ---------------------------
csv_path = r"C:\Users\shanmugapriya\Downloads\Data analysis dashboard\E-commerce Dataset.csv"

df = pd.read_csv(csv_path)

# ---------------------------
# Step 2: Data Preprocessing
# ---------------------------
# Convert date columns
if "Order Date" in df.columns:
    df['Order Date'] = pd.to_datetime(df['Order Date'], errors="coerce")

# Create new features
if "Order Date" in df.columns:
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month
    df['YearMonth'] = df['Order Date'].dt.to_period('M')

# Handle missing values
df = df.dropna()

# Feature Engineering: Profit Margin (if Sales & Profit exist)
if "Profit" in df.columns and "Sales" in df.columns:
    df['Profit Margin %'] = (df['Profit'] / df['Sales']) * 100

# ---------------------------
# Step 3: Streamlit Dashboard UI
# ---------------------------
st.set_page_config(page_title="E-commerce Dashboard", layout="wide")
st.title("📊 E-commerce Data Analysis Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
if "Region" in df.columns:
    region = st.sidebar.multiselect("Select Region", df['Region'].unique())
    if region:
        df = df[df['Region'].isin(region)]

if "Category" in df.columns:
    category = st.sidebar.multiselect("Select Category", df['Category'].unique())
    if category:
        df = df[df['Category'].isin(category)]

# ---------------------------
# Step 4: KPIs
# ---------------------------
total_sales = df['Sales'].sum() if "Sales" in df.columns else 0
total_profit = df['Profit'].sum() if "Profit" in df.columns else 0
num_orders = df['Order ID'].nunique() if "Order ID" in df.columns else len(df)
avg_order_value = total_sales / num_orders if num_orders > 0 else 0

# Show metrics
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("💰 Total Sales", f"${total_sales:,.0f}")
kpi2.metric("📈 Total Profit", f"${total_profit:,.0f}")
kpi3.metric("🛒 Total Orders", num_orders)
kpi4.metric("📦 Avg Order Value", f"${avg_order_value:,.2f}")

st.markdown("---")

# ---------------------------
# Step 5: Charts
# ---------------------------

# 1. Sales Trend Over Time
sales_trend = df.groupby('YearMonth').agg(Total_Sales=('Sales', 'sum')).reset_index()
fig1 = px.line(sales_trend, x='YearMonth', y='Total_Sales', title='Sales Trend Over Time')
st.plotly_chart(fig1, use_container_width=True)

# 2. Sales by Category
if "Category" in df.columns:
    sales_category = df.groupby('Category').agg(Total_Sales=('Sales', 'sum')).reset_index()
    fig2 = px.bar(sales_category, x='Category', y='Total_Sales', title='Sales by Category')
    st.plotly_chart(fig2, use_container_width=True)

# 3. Sales by Region
if "Region" in df.columns:
    sales_region = df.groupby('Region').agg(Total_Sales=('Sales', 'sum')).reset_index()
    fig3 = px.choropleth(sales_region, locations='Region', locationmode='country names',
                        color='Total_Sales', title='Sales by Region')
    st.plotly_chart(fig3, use_container_width=True)

# 4. Top 10 Products by Sales
top_products = df.groupby('Product ID').agg(Total_Sales=('Sales', 'sum')).reset_index()
top_products = top_products.sort_values(by='Total_Sales', ascending=False).head(10)
fig4 = px.bar(top_products, x='Product ID', y='Total_Sales', title='Top 10 Products by Sales')
st.plotly_chart(fig4, use_container_width=True)

# 5. Monthly Sales Heatmap
monthly_sales = df.groupby(['Year', 'Month']).agg(Total_Sales=('Sales', 'sum')).reset_index()
fig5 = px.imshow(monthly_sales.pivot_table(index='Month', columns='Year', values='Total_Sales'),
                title='Monthly Sales Heatmap')
st.plotly_chart(fig5, use_container_width=True)

# ---------------------------
# Step 6: Data Download
# ---------------------------
st.markdown("---")
st.header("Download Processed Data")

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name='processed_ecommerce_data.csv',
    mime='text/csv',
)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by [Your Name]")

# ---------------------------
# README
# ---------------------------
"""
# E-commerce Dashboard Project

This project analyzes e-commerce sales data to provide insights into sales performance, 
profitability, and order trends. The dashboard allows users to filter data by region and category, 
and view key performance indicators (KPIs) and charts such as sales trend over time, sales by category, 
sales by region, top 10 products by sales, and a monthly sales heatmap.

## Files Included
- `E-commerce Dataset.csv`: The raw e-commerce sales data.
- `app.py`: The Streamlit application file for the dashboard.
- `requirements.txt`: The Python dependencies required to run the app.

## Instructions
1. Install the required packages using `pip install -r requirements.txt`
2. Run the Streamlit app with `streamlit run app.py`
3. Open the app in your web browser at `http://localhost:8501`

## Author
[Your Name]
"""
