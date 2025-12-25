import pandas as pd
import numpy as np
import os

def load_and_process_data(data_path='../data/Data.csv', price_path='../data/StockPrice.csv'):
    """
    Loads data, aligns timestamps, handles missing values, and generates lagged features.
    
    Args:
        data_path: Path to independent variable CSV
        price_path: Path to target variable CSV
        
    Returns:
        df: Processed DataFrame with features and target
    """
   
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if data_path == '../data/Data.csv':
        data_path = os.path.join(base_dir, '../data/Data.csv')
    if price_path == '../data/StockPrice.csv':
        price_path = os.path.join(base_dir, '../data/StockPrice.csv')


    df_data = pd.read_csv(data_path, parse_dates=['Date'])
    df_price = pd.read_csv(price_path, parse_dates=['Date'])

    
    df_data = df_data.sort_values('Date').reset_index(drop=True)
    df_price = df_price.sort_values('Date').reset_index(drop=True)

    
    df = pd.merge(df_price, df_data, on='Date', how='inner')

    
    df = df.ffill()

    
  
    
                
    df['Data_Lag1'] = df['Data'].shift(1)
    
    
    df['Data_Lag2'] = df['Data'].shift(2)

    
    df['Data_Diff'] = df['Data_Lag1'] - df['Data_Lag2']

    
    df['Data_Pct_Change'] = (df['Data_Diff'] / df['Data_Lag2']) * 100

    
    df = df.dropna().reset_index(drop=True)

    return df

if __name__ == "__main__":
    # Test execution
    try:
        df = load_and_process_data()
        print("Data processed successfully.")
        print(f"Shape: {df.shape}")
        print("\nFirst 5 rows:")
        print(df.head())
        print("\nLast 5 rows:")
        print(df.tail())
        
        
        df.to_csv("debug_processed_data.csv", index=False)
        print("\nSaved debug_processed_data.csv")
    except Exception as e:
        print(f"Error during processing: {e}")
