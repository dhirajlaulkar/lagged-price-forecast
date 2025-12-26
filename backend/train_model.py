import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

import os
from preprocessing import load_and_process_data

def train():
    print("Loading data..")
    df = load_and_process_data()
    
    # Updated Features and Target
    features = ['Data_Lag1', 'Data_Diff']
    target = 'Price_Diff'
    
    X = df[features]
    y = df[target]
    
    split_idx = int(len(df) * 0.8)
    
    X_train = X.iloc[:split_idx]
    y_train = y.iloc[:split_idx]
    X_test = X.iloc[split_idx:]
    y_test = y.iloc[split_idx:]
    
    print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)
    
    y_pred_diff = model.predict(X_test_scaled)
    
    price_lag1_test = df.iloc[split_idx:]['Price_Lag1']
    y_pred_price = price_lag1_test + y_pred_diff
    y_actual_price = df.iloc[split_idx:]['Price']

    mse = mean_squared_error(y_actual_price, y_pred_price)
    r2 = r2_score(y_actual_price, y_pred_price)
    
    actual_diff = df.iloc[split_idx:]['Price_Diff']
    directional_accuracy = np.mean(np.sign(y_pred_diff) == np.sign(actual_diff)) * 100
    
    print(f"Model Trained. MSE: {mse:.4f}, R2: {r2:.4f}, Directional Acc: {directional_accuracy:.2f}%")
    
    # Save Evaluation Metrics
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    import json
    
    
    insights = []
    insights.append(f"Model explains {r2*100:.1f}% of the variance in stock prices.")
    

    lag_coef = model.coef_[0]
    diff_coef = model.coef_[1]
    
    if abs(diff_coef) > abs(lag_coef):
         insights.append("Day-to-day changes in data have a stronger impact than the raw value level.")
    else:
         insights.append("The raw level of the data is a stronger predictor than recent changes.")
         
    if diff_coef > 0:
        insights.append("Positive changes in the data signal correlate with higher stock prices (positive correlation).")
    else:
        insights.append("Positive changes in the data signal tend to pull the stock price down (negative correlation).")
        
    metrics = {
        "mse": mse,
        "r2": r2,
        "directional_accuracy": directional_accuracy
    }
    
    
    coef_list = []
    for feat, coef in zip(features, model.coef_):
        item = {"Feature": feat, "Coefficient": coef}
        if feat == 'Data_Lag1':
            item['Explanation'] = "Absolute Level (Gravity Effect) - Higher rates typically push prices down"
        elif feat == 'Data_Diff':
            item['Explanation'] = "Rate of Change (Momentum) - Immediate changes add pressure"
        coef_list.append(item)
            
    output = {
        "metrics": metrics,
        "insights": insights,
        "coefficients": coef_list
    }
    
    with open(os.path.join(models_dir, 'evaluation.json'), 'w') as f:
        json.dump(output, f, indent=4)

    test_results = X_test.copy()
    test_results['Actual_Price'] = y_actual_price
    test_results['Predicted_Price'] = y_pred_price
    test_results['Date'] = df.iloc[split_idx:]['Date']
    test_results.to_csv(os.path.join(models_dir, 'test_results.csv'), index=False)
    
    coef_df = pd.DataFrame({
        'Feature': features,
        'Coefficient': model.coef_
    })
    coef_df.to_csv(os.path.join(models_dir, 'coefficients.csv'), index=False)
    
    print(f"Artifacts saved to {models_dir}")

if __name__ == "__main__":
    train()
