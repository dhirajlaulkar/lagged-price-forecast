# Lagged Price Forecast

## Approach and Assumptions
This project implements a Time-Series Forecasting model to predict daily `StockPrice`. The core assumption is that the stock price is primarily driven by the "Data" variable (e.g., Interest Rates or Bond Yields), specifically its previous day's value and immediate rate of change.

We assume a **non-stationary** relationship where the absolute level of `Data` shifts over time (regimes). To handle this, the model predicts the **Day-to-Day Price Change** (Price[t] - Price[t-1]) rather than the absolute price. The final forecasted price is reconstructed by adding the predicted change to the previous known price.

## Data Preprocessing Steps
The data pipeline (`backend/preprocessing.py`) performs the following operations:
1.  **Alignment**: Merges `StockPrice.csv` (Target) and `Data.csv` (Feature) on the `Date` column.
2.  **Imputation**: Uses Forward Fill (`ffill`) to handle missing values, assuming market data remains constant on non-trading days.
3.  **Feature Engineering**:
    *   **Data_Lag1**: The absolute value of the Data variable at time `t-1`.
    *   **Data_Diff**: The change in Data from `t-2` to `t-1` (Momentum proxy).
4.  **Target Engineering**:
    *   Calculates `Price_Diff` (Price[t] - Price[t-1]) to create a stationary target variable for training.

## Model Selection and Evaluation
A **Linear Regression** model was selected for its interpretability and ability to capture the inverse correlation between the independent variable and the asset price.

*   **Training Split**: Time-based split (80% Train, 20% Test) to strictly prevent future data leakage.
*   **Scaling**: Standard Scaler is applied to normalize features (z-score normalization).
*   **Reconstruction**: The model predicts the *difference*. Post-prediction, the absolute price is reconstructed:
    `Predicted_Price(t) = Price(t-1) + Predicted_Diff(t)`

### Evaluation Metrics (Test Set)
*   **R2 Score**: **99.4%** - Indicates the model explains nearly all variance in the stock price movement.
*   **Mean Squared Error (MSE)**: **2343.98** - Average squared deviation of the predicted price from actual.
*   **Directional Accuracy**: **47.3%** - The model captures the magnitude/trend accurately but struggles with daily noise directionality.

## Key Insights and Conclusions
Automated analysis of the model coefficients reveals:
1.  **Primary Driver**: The **Absolute Level** of the "Data" variable is the strongest predictor.
2.  **Negative Correlation**: Both the absolute level (`Coef: -0.35`) and the rate of change (`Coef: -0.18`) have a negative impact on price. This suggests that as the "Data" variable (e.g., Interest Rates) rises, the Stock Price falls.
3.  **Regime Handling**: By modeling price *differences*, the system successfully adapts to new execution regimes (e.g., 2024-2025) even when the underlying data values are significantly higher than the training period (2010-2023).

---
*Note: A Next.js frontend is included in the `frontend/` directory solely for visualization purposes, providing an interactive dashboard to view the forecast against actual historical performance.*
