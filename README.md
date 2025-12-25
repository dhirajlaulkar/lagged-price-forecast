# Lagged Price Forecast

**Project Objective**: Build an end-to-end Python + Next.js project that predicts stock prices using lagged (previous-day) data changes.

## 📌 Project Overview
This application predicts the daily `StockPrice` based on the previous day's `Data` metric. It implements a Linear Regression model trained on historical data, adhering to strict constraints:
- **Primary Influence**: Stock price movement is influenced only by the previous day’s change in data.
- **Model**: Linear Regression (no deep learning).
- **Tech Stack**: FastAPI (Backend) + Next.js (Frontend).

## 🧠 Data & Methodology
### Data Preprocessing
- **Source**: `Data.csv` (Independent) and `StockPrice.csv` (Dependent).
- **Alignment**: Datasets are merged on `Date` and sorted ascending.
- **Missing Values**: Handled via **Forward Fill** (`ffill`) to propagate last known values.
- **Feature Engineering**:
    - `Data_Lag1`: Value of Data at $t-1$.
    - `Data_Diff`: Day-over-day change ($Data_{t-1} - Data_{t-2}$).
    - `Data_Pct_Change`: Percentage change relative to $t-2$.
- **Target**: `Price` at $t$.

### Model
- **Algorithm**: Linear Regression (`sklearn`).
- **Split**: Time-based split (80% Train, 20% Test) to prevent data leakage.
- **Scaling**: Features are normalized using `StandardScaler`.

## 🚀 Usage

### Prerequisites
- Python 3.9+
- Node.js 18+

### 1. Backend Setup
Navigate to the root directory:
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run Training Pipeline (Preprocessing -> Train -> Evaluate)
python backend/train_model.py
python backend/evaluate.py

# Start API Server
python backend/api.py
```
*API will run at `http://localhost:8000`*

### 2. Frontend Setup
Navigate to `frontend/`:
```bash
cd frontend
npm install
npm run dev
```
*Dashboard will run at `http://localhost:3000`*

## 📊 Dashboard Features
- **Price Forecast**: Line chart comparing Actual vs Predicted stock prices on the test set.
- **Metrics**: Real-time display of $R^2$ Score, MSE, and Directional Accuracy.
- **Insights**: AI-generated textual explanations of model findings and coefficient impact.

## 📁 Repository Structure
```
lagged-price-forecast/
├── backend/
│   ├── data/               # Data files (symlinked or loaded from root)
│   ├── models/             # Saved models and evaluation JSON
│   ├── api.py             # FastAPI application
│   ├── preprocessing.py   # Data pipeline
│   ├── train_model.py     # Training script
│   ├── evaluate.py        # Evaluation script
│   └── requirements.txt
├── frontend/
│   ├── app/               # Next.js App Router pages
│   ├── components/        # Reusable UI components
│   └── ...
└── README.md
```

