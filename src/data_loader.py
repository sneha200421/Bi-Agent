import pandas as pd
from typing import Tuple, Dict, Any

def load_and_merge_data(customers_path: str, orders_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Loads customers and orders datasets, performs data cleaning,
    merges them on customer_id, and extracts dataset metadata.
    """
    try:
        customers_df = pd.read_csv(customers_path)
        orders_df = pd.read_csv(orders_path)
        
        # Strip column whitespace
        customers_df.columns = customers_df.columns.str.strip()
        orders_df.columns = orders_df.columns.str.strip()
        
        # Merge on customer_id
        df = pd.merge(orders_df, customers_df, on='customer_id', how='left')
        
        # Date transformations
        if 'order_date' in df.columns:
            df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        if 'customer_signup_date' in df.columns:
            df['customer_signup_date'] = pd.to_datetime(df['customer_signup_date'], errors='coerce')
            
        # Clean numerical fields
        if 'discount_percentage' in df.columns:
            df['discount_percentage'] = df['discount_percentage'].fillna(0)
            
        # Extract schema information for the LLM context
        schema_info = {
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "sample_rows": df.head(3).to_dict(orient="records"),
            "total_records": len(df)
        }
        
        return df, schema_info

    except Exception as e:
        raise RuntimeError(f"Error loading datasets: {str(e)}")

def generate_sample_datasets():
    """Generates synthetic datasets if no CSVs are provided."""
    import numpy as np
    
    np.random.seed(42)
    n_customers = 100
    n_orders = 500
    
    customers_data = {
        'customer_id': [f'CUST_{i:03d}' for i in range(1, n_customers + 1)],
        'customer_signup_date': pd.date_range(start='2023-01-01', periods=n_customers, freq='D').strftime('%Y-%m-%d'),
        'gender': np.random.choice(['Male', 'Female'], n_customers),
        'age': np.random.randint(18, 65, n_customers),
        'age_group': np.random.choice(['18-25', '26-35', '36-50', '50+'], n_customers),
        'state': np.random.choice(['Maharashtra', 'Karnataka', 'Delhi', 'Tamil Nadu'], n_customers),
        'city': np.random.choice(['Mumbai', 'Bengaluru', 'New Delhi', 'Chennai'], n_customers),
        'pincode_prefix': np.random.choice([400, 560, 110, 600], n_customers),
        'customer_segment': np.random.choice(['VIP', 'Regular', 'New'], n_customers),
        'preferred_device': np.random.choice(['Mobile', 'Desktop', 'Tablet'], n_customers)
    }
    
    orders_data = {
        'order_id': [f'ORD_{i:04d}' for i in range(1, n_orders + 1)],
        'customer_id': np.random.choice(customers_data['customer_id'], n_orders),
        'order_date': pd.date_range(start='2024-01-01', periods=n_orders, freq='H').strftime('%Y-%m-%d'),
        'order_time': '12:00:00',
        'order_status': np.random.choice(['Delivered', 'Cancelled', 'Returned'], n_orders, p=[0.8, 0.1, 0.1]),
        'shipping_method': np.random.choice(['Express', 'Standard'], n_orders),
        'delivery_city': np.random.choice(['Mumbai', 'Bengaluru', 'New Delhi', 'Chennai'], n_orders),
        'delivery_state': np.random.choice(['Maharashtra', 'Karnataka', 'Delhi', 'Tamil Nadu'], n_orders),
        'coupon_code': np.random.choice(['SAVE10', 'WELCOME20', None], n_orders, p=[0.3, 0.2, 0.5]),
        'discount_percentage': np.random.choice([10, 20, 0], n_orders, p=[0.3, 0.2, 0.5])
    }
    
    pd.DataFrame(customers_data).to_csv('data/customers.csv', index=False)
    pd.DataFrame(orders_data).to_csv('data/orders.csv', index=False)
    print("Sample datasets created in data/ directory.")

if __name__ == "__main__":
    generate_sample_datasets()