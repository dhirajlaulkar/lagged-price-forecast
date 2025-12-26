import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from preprocessing import load_and_process_data

def generate_eda_plots():
    print("Generating EDA Plots...")
    
    # 1. Setup Directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    plots_dir = os.path.join(base_dir, 'plots')
    models_dir = os.path.join(base_dir, 'models')
    os.makedirs(plots_dir, exist_ok=True)
    
    # 2. Load Data
    df = load_and_process_data()
    
    # Load Test Results for Predicted vs Actual
    results_path = os.path.join(models_dir, 'test_results.csv')
    if os.path.exists(results_path):
        test_results = pd.read_csv(results_path)
    else:
        print("Warning: test_results.csv not found. Skipping Predicted vs Actual plot.")
        test_results = None

    # Set Style
    sns.set_theme(style="whitegrid")
    
    # --- PLOT 1: Actual vs Predicted Price (The "Hero" Chart) ---
    if test_results is not None:
        plt.figure(figsize=(12, 6))
        plt.plot(pd.to_datetime(test_results['Date']), test_results['Actual_Price'], label='Actual Price', color='black', linewidth=2)
        plt.plot(pd.to_datetime(test_results['Date']), test_results['Predicted_Price'], label='Predicted Price', color='red', linestyle='--', alpha=0.9)
        plt.title('Actual vs Predicted Stock Price (Test Set)', fontsize=16)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(plots_dir, '1_Actual_vs_Predicted.png'))
        plt.close()
        print("Saved: 1_Actual_vs_Predicted.png")

    # --- PLOT 2: Dual Axis - Price vs Data (Visualizing the Inverse Correlation) ---
    # Downsample for readability if needed, but let's take the last 500 points
    subset = df.iloc[-500:]
    
    fig, ax1 = plt.subplots(figsize=(12, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Date (Last 500 Days)')
    ax1.set_ylabel('Stock Price', color=color)
    ax1.plot(subset['Date'], subset['Price'], color=color, linewidth=2, label='Stock Price')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:orange'
    ax2.set_ylabel('Data (Yield/Rate)', color=color)  # we already handled the x-label with ax1
    ax2.plot(subset['Date'], subset['Data'], color=color, linestyle=':', linewidth=2, label='Data (Lagged Driver)')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Stock Price vs Data (Inverse Relationship)', fontsize=16)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(os.path.join(plots_dir, '2_Price_vs_Data_DualAxis.png'))
    plt.close()
    print("Saved: 2_Price_vs_Data_DualAxis.png")

    # --- PLOT 3: Scatter Plot - Data Level vs Price ---
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Data', y='Price', data=df, alpha=0.5, color='purple')
    plt.title('Correlation: Data Level vs Stock Price', fontsize=16)
    plt.xlabel('Data Value (Lagged)')
    plt.ylabel('Stock Price')
    
    # Add trendline
    z = np.polyfit(df['Data'], df['Price'], 1)
    p = np.poly1d(z)
    plt.plot(df['Data'], p(df['Data']), "r--", linewidth=2)
    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, '3_Scatter_Data_vs_Price.png'))
    plt.close()
    print("Saved: 3_Scatter_Data_vs_Price.png")

    # --- PLOT 4: Correlation Heatmap ---
    plt.figure(figsize=(8, 6))
    corr_matrix = df[['Price', 'Data_Lag1', 'Data_Diff', 'Price_Diff']].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Feature Correlation Matrix', fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, '4_Correlation_Heatmap.png'))
    plt.close()
    print("Saved: 4_Correlation_Heatmap.png")

    # --- STATISTICS OUTPUT ---
    print("\n--- Model Insights ---")
    
    # Calculate Correlation
    corr = df['Price'].corr(df['Data_Lag1'])
    print(f"Correlation between Price and Data_Lag1: {corr:.4f}")
    if corr < -0.5:
        print("Insight: Strong Negative Correlation. As Data increases, Price tends to decrease.")
    elif corr > 0.5:
        print("Insight: Strong Positive Correlation. As Data increases, Price tends to increase.")
        
    print("\nPlots have been saved to 'backend/plots/' directory.")

if __name__ == "__main__":
    generate_eda_plots()
