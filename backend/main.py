"""
FastAPI Backend for AI Company Data Analyzer
Provides REST API endpoints for data analysis and ML operations
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from pydantic import BaseModel
from typing import List, Dict, Any
import io
import json
import warnings
warnings.filterwarnings('ignore')

# Initialize FastAPI app
app = FastAPI(
    title="AI Company Data Analyzer API",
    description="REST API for automated company data analysis using AI/ML",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class ForecastRequest(BaseModel):
    date_column: str
    value_column: str
    periods: int = 90

class SegmentationRequest(BaseModel):
    features: List[str]
    n_clusters: int = 4

class AnomalyRequest(BaseModel):
    column: str

# Global data storage (in production, use proper database)
data_store = {}

@app.get("/")
async def root():
    return {"message": "AI Company Data Analyzer API", "version": "1.0.0"}

@app.post("/upload")
async def upload_data(file: UploadFile = File(...)):
    """Upload and process company dataset"""
    try:
        # Read uploaded file
        content = await file.read()
        
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Store data (use session ID in production)
        data_id = "default"
        data_store[data_id] = df
        
        # Generate data summary
        summary = {
            "rows": len(df),
            "columns": len(df.columns),
            "numeric_columns": len(df.select_dtypes(include=[np.number]).columns),
            "missing_values": int(df.isnull().sum().sum()),
            "column_info": [
                {
                    "name": col,
                    "type": str(df[col].dtype),
                    "missing": int(df[col].isnull().sum()),
                    "unique": int(df[col].nunique())
                }
                for col in df.columns
            ]
        }
        
        return {"message": "Data uploaded successfully", "summary": summary}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/forecast")
async def generate_forecast(request: ForecastRequest):
    """Generate sales/revenue forecast using Prophet"""
    try:
        data_id = "default"
        if data_id not in data_store:
            raise HTTPException(status_code=404, detail="No data found. Please upload data first.")
        
        df = data_store[data_id]
        
        # Prepare data for Prophet
        forecast_df = df[[request.date_column, request.value_column]].copy()
        forecast_df.columns = ['ds', 'y']
        forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
        forecast_df = forecast_df.dropna()
        
        # Create and fit Prophet model
        model = Prophet(
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=True
        )
        model.fit(forecast_df)
        
        # Make future predictions
        future = model.make_future_dataframe(periods=request.periods)
        forecast = model.predict(future)
        
        # Calculate insights
        last_actual = forecast_df['y'].iloc[-1]
        next_month_forecast = forecast[forecast['ds'] > forecast_df['ds'].max()]['yhat'].iloc[:30].mean()
        growth_rate = ((next_month_forecast - last_actual) / last_actual) * 100
        
        # Prepare response
        response = {
            "historical_data": {
                "dates": forecast_df['ds'].dt.strftime('%Y-%m-%d').tolist(),
                "values": forecast_df['y'].tolist()
            },
            "forecast_data": {
                "dates": forecast['ds'].dt.strftime('%Y-%m-%d').tolist(),
                "predicted": forecast['yhat'].tolist(),
                "upper_bound": forecast['yhat_upper'].tolist(),
                "lower_bound": forecast['yhat_lower'].tolist()
            },
            "insights": {
                "current_value": float(last_actual),
                "next_month_forecast": float(next_month_forecast),
                "growth_rate": float(growth_rate),
                "trend": "growth" if growth_rate > 5 else "decline" if growth_rate < -5 else "stable"
            }
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating forecast: {str(e)}")

@app.post("/segmentation")
async def customer_segmentation(request: SegmentationRequest):
    """Perform customer segmentation using K-means clustering"""
    try:
        data_id = "default"
        if data_id not in data_store:
            raise HTTPException(status_code=404, detail="No data found. Please upload data first.")
        
        df = data_store[data_id]
        
        # Prepare data
        cluster_data = df[request.features].dropna()
        
        # Standardize features
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(cluster_data)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=request.n_clusters, random_state=42)
        clusters = kmeans.fit_predict(scaled_data)
        
        # Add cluster labels
        cluster_data['segment'] = clusters
        
        # Generate segment analysis
        segments = []
        for i in range(request.n_clusters):
            segment_data = cluster_data[cluster_data['segment'] == i]
            segment_info = {
                "segment_id": i + 1,
                "size": len(segment_data),
                "percentage": len(segment_data) / len(cluster_data) * 100,
                "characteristics": {}
            }
            
            # Calculate segment characteristics
            for feature in request.features:
                avg_value = segment_data[feature].mean()
                overall_avg = cluster_data[feature].mean()
                segment_info["characteristics"][feature] = {
                    "average": float(avg_value),
                    "relative_to_overall": "high" if avg_value > overall_avg * 1.1 else "low" if avg_value < overall_avg * 0.9 else "average"
                }
            
            segments.append(segment_info)
        
        # Prepare visualization data
        visualization_data = {
            "x_values": cluster_data[request.features[0]].tolist(),
            "y_values": cluster_data[request.features[1]].tolist() if len(request.features) > 1 else [],
            "segments": cluster_data['segment'].tolist()
        }
        
        return {
            "segments": segments,
            "visualization": visualization_data,
            "total_customers": len(cluster_data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing segmentation: {str(e)}")

@app.post("/anomaly-detection")
async def detect_anomalies(request: AnomalyRequest):
    """Detect anomalies in the specified column using IQR method"""
    try:
        data_id = "default"
        if data_id not in data_store:
            raise HTTPException(status_code=404, detail="No data found. Please upload data first.")
        
        df = data_store[data_id]
        data_series = df[request.column].dropna()
        
        # Calculate IQR-based thresholds
        Q1 = data_series.quantile(0.25)
        Q3 = data_series.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Identify anomalies
        anomalies = data_series[(data_series < lower_bound) | (data_series > upper_bound)]
        
        # Prepare response
        response = {
            "total_data_points": len(data_series),
            "anomalies_found": len(anomalies),
            "anomaly_rate": len(anomalies) / len(data_series) * 100,
            "thresholds": {
                "lower_bound": float(lower_bound),
                "upper_bound": float(upper_bound)
            },
            "anomalies": [
                {
                    "index": int(idx),
                    "value": float(val),
                    "type": "high" if val > upper_bound else "low"
                }
                for idx, val in anomalies.items()
            ],
            "visualization": {
                "indices": data_series.index.tolist(),
                "values": data_series.tolist(),
                "anomaly_indices": anomalies.index.tolist(),
                "anomaly_values": anomalies.tolist()
            }
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting anomalies: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
