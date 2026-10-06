import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from src.data_loader import load_and_merge_data, generate_sample_datasets
from src.agent import BIAgent

# Page Config
st.set_page_config(
    page_title="AI Business Intelligence Agent",
    page_icon="📊",
    layout="wide"
)

load_dotenv()

# Sidebar: Configuration & Data Source Selection
st.sidebar.title(" Configuration")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

st.sidebar.markdown("---")
st.sidebar.subheader(" Data Source")
data_source = st.sidebar.radio("Select Dataset:", ["Use Sample Data", "Upload Custom CSVs"])

# Ensure sample files exist if option selected
if data_source == "Use Sample Data":
    if not os.path.exists("data/customers.csv") or not os.path.exists("data/orders.csv"):
        os.makedirs("data", exist_ok=True)
        generate_sample_datasets()
    customers_path = "data/customers.csv"
    orders_path = "data/orders.csv"

elif data_source == "Upload Custom CSVs":
    cust_file = st.sidebar.file_uploader("Upload Customers CSV", type=["csv"])
    ord_file = st.sidebar.file_uploader("Upload Orders CSV", type=["csv"])
    
    if cust_file and ord_file:
        os.makedirs("data", exist_ok=True)
        customers_path = "data/uploaded_customers.csv"
        orders_path = "data/uploaded_orders.csv"
        with open(customers_path, "wb") as f:
            f.write(cust_file.getbuffer())
        with open(orders_path, "wb") as f:
            f.write(ord_file.getbuffer())
    else:
        st.info("Please upload both `customers.csv` and `orders.csv` in the sidebar to proceed.")
        st.stop()

# Load Data
@st.cache_data
def get_data(c_path, o_path):
    return load_and_merge_data(c_path, o_path)

try:
    df, schema_info = get_data(customers_path, orders_path)
except Exception as e:
    st.error(f"Failed to load dataset: {e}")
    st.stop()

# Header
st.title(" AI-Powered Business Intelligence Agent")
st.caption("Ask natural language business questions to run automated calculations, charts, and recommendations.")

# Executive KPI Summary Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Customers", f"{df['customer_id'].nunique():,}")
with col2:
    st.metric("Total Orders", f"{len(df):,}")
with col3:
    completed = df[df['order_status'] == 'Delivered'] if 'order_status' in df.columns else df
    st.metric("Delivered Orders", f"{len(completed):,}")
with col4:
    unique_cities = df['delivery_city'].nunique() if 'delivery_city' in df.columns else df['city'].nunique()
    st.metric("Active Cities", f"{unique_cities}")

st.markdown("---")

# Main Query Interface
st.subheader(" Ask a Business Question")

sample_questions = [
    "Which city generates the highest number of orders?",
    "What is the distribution of orders by order status?",
    "What percentage of customers belong to each age group?",
    "Which preferred device drives the most orders?"
]

selected_sample = st.selectbox("Or choose an example query:", [""] + sample_questions)
user_query = st.text_input("Enter your business question:", value=selected_sample if selected_sample else "")

if st.button("Analyze Data", type="primary"):
    if not api_key:
        st.error("Please provide a valid Gemini API Key in `.env` or sidebar.")
        st.stop()
        
    if not user_query.strip():
        st.warning("Please enter a question to analyze.")
        st.stop()

    with st.spinner("Analyzing dataset, generating Python code, and calculating metrics..."):
        try:
            agent = BIAgent(api_key=api_key)
            response = agent.run_pipeline(user_query, df, schema_info)
            
            if not response["success"]:
                st.error("Execution error encountered while executing generated analysis code.")
                st.error(response["error"])
                with st.expander(" View Generated Code"):
                    st.code(response["code"], language="python")
            else:
                # 1. Direct Narrative & Recommendations
                st.markdown("###  Business Insights & Recommendations")
                st.markdown(response["insights"])
                
                # 2. Render Chart if generated
                if response["fig"] is not None:
                    st.markdown("###  Visual Analysis")
                    st.plotly_chart(response["fig"], use_container_width=True)
                
                # 3. Calculated Data Table
                if response["result"] is not None:
                    st.markdown("###  Calculated Dataset")
                    st.dataframe(response["result"], use_container_width=True)

                # 4. Debugging & Code Inspection
                with st.expander(" View Execution Logic (Generated Python Code)"):
                    st.code(response["code"], language="python")
                    
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Footer / Dataset Preview
with st.expander(" View Raw Merged Dataset Schema"):
    st.write(f"Total Rows: {schema_info['total_records']}")
    st.dataframe(df.head(10), use_container_width=True)