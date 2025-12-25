import pandas as pd
import numpy as np
import json
from sklearn.metrics import mean_squared_error, r2_score
import os

def generate_insights():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(base_dir, 'models')
        results_path = os.path.join(models_dir, 'test_results.csv')
        
        if not os.path.exists(results_path):
            print(f"Test results not found at {results_path}. Run train_model.py first.")
            return

        df = pd.read_csv(results_path)
        
        y_true = df['Actual_Price']
        y_pred = df['Predicted_Price']
        
        
        mse = mean_squared_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        
        
        prev_actual = y_true.shift(1)
        
        valid_idx = prev_actual.notna()
        
        actual_move = (y_true[valid_idx] - prev_actual[valid_idx]) > 0
        pred_move = (y_pred[valid_idx] - prev_actual[valid_idx]) > 0
        
        dir_acc = np.mean(actual_move == pred_move) * 100
        
        
        coef_df = pd.read_csv(os.path.join(models_dir, 'coefficients.csv'))
        
        
        insights = []
        
        
        lag_coef = coef_df.loc[coef_df['Feature'] == 'Data_Lag1', 'Coefficient'].values[0]
        diff_coef = coef_df.loc[coef_df['Feature'] == 'Data_Diff', 'Coefficient'].values[0]
        
        insights.append(f"Model explains {r2*100:.1f}% of the variance in stock prices.")
        
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
            "directional_accuracy": dir_acc
        }
        
        output = {
            "metrics": metrics,
            "insights": insights,
            "coefficients": coef_df.to_dict(orient='records')
        }
        
        output_path = os.path.join(models_dir, 'evaluation.json')
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=4)
            
        print(f"Evaluation complete. Saved to {output_path}")
        print(json.dumps(output, indent=2))
        
    except Exception as e:
        print(f"Error in evaluation: {e}")

if __name__ == "__main__":
    generate_insights()
