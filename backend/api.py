from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import json
import os
import joblib

app = FastAPI(title="Lagged Price Forecast API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Lagged Price Forecast API is running"}

@app.get("/metrics")
def get_metrics():
    """Returns model evaluation metrics and insights."""
    try:
        eval_path = os.path.join(MODELS_DIR, "evaluation.json")
        if not os.path.exists(eval_path):
            raise HTTPException(status_code=404, detail="Metrics not found. Model might not be trained.")
        
        with open(eval_path, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predictions")
def get_predictions():
    """Returns actual vs predicted prices from the test set."""
    try:
        results_path = os.path.join(MODELS_DIR, "test_results.csv")
        if not os.path.exists(results_path):
            raise HTTPException(status_code=404, detail="Predictions not found.")
            
        df = pd.read_csv(results_path)
        
        df = df.sort_values("Date")
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def get_history():
    """Returns full historical data (Data vs Price) for visualization."""
    try:
        
        from preprocessing import load_and_process_data
        df = load_and_process_data()
        
        return df[['Date', 'Price', 'Data']].to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
