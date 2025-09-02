"""
AnalyticaCore AI - Advanced Forecasting Engine
Following project coding instructions and AI/ML best practices
Implements Prophet, XGBoost, and ensemble forecasting methods
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import logging
import warnings
warnings.filterwarnings('ignore')

# Configure logging following coding instructions
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import ML libraries with fallbacks
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    logger.warning("Prophet not available. Using sklearn-based forecasting.")
    PROPHET_AVAILABLE = False

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    logger.warning("XGBoost not available. Using sklearn-based forecasting.")
    XGBOOST_AVAILABLE = False

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class AdvancedForecastingEngine:
    """
    Advanced forecasting engine for AnalyticaCore AI
    Following AI/ML best practices and SME business context
    """
    
    def __init__(self):
        """Initialize advanced forecasting engine"""
        self.logger = logging.getLogger(__name__)
        self.models = {}
        self.scalers = {}
        self.feature_columns = []
        self.target_column = None
        
        logger.info("Advanced forecasting engine initialized")
    
    def prepare_time_series_features(self, df: pd.DataFrame, date_col: str, target_col: str) -> pd.DataFrame:
        """
        Prepare time series features for forecasting
        Following feature engineering best practices
        
        Args:
            df: Input dataframe
            date_col: Name of date column
            target_col: Name of target column
            
        Returns:
            DataFrame with engineered features
        """
        try:
            # Ensure datetime format
            forecast_df = df.copy()
            forecast_df[date_col] = pd.to_datetime(forecast_df[date_col])
            forecast_df = forecast_df.sort_values(date_col)
            
            # Basic time features
            forecast_df['year'] = forecast_df[date_col].dt.year
            forecast_df['month'] = forecast_df[date_col].dt.month
            forecast_df['day'] = forecast_df[date_col].dt.day
            forecast_df['dayofweek'] = forecast_df[date_col].dt.dayofweek
            forecast_df['dayofyear'] = forecast_df[date_col].dt.dayofyear
            forecast_df['quarter'] = forecast_df[date_col].dt.quarter
            forecast_df['week'] = forecast_df[date_col].dt.isocalendar().week
            
            # Cyclical features following ML best practices
            forecast_df['month_sin'] = np.sin(2 * np.pi * forecast_df['month'] / 12)
            forecast_df['month_cos'] = np.cos(2 * np.pi * forecast_df['month'] / 12)
            forecast_df['day_sin'] = np.sin(2 * np.pi * forecast_df['dayofweek'] / 7)
            forecast_df['day_cos'] = np.cos(2 * np.pi * forecast_df['dayofweek'] / 7)
            
            # Lag features
            for lag in [1, 7, 30]:
                if len(forecast_df) > lag:
                    forecast_df[f'{target_col}_lag_{lag}'] = forecast_df[target_col].shift(lag)
            
            # Rolling statistics
            for window in [7, 14, 30]:
                if len(forecast_df) > window:
                    forecast_df[f'{target_col}_ma_{window}'] = forecast_df[target_col].rolling(
                        window=window, min_periods=1
                    ).mean()
                    forecast_df[f'{target_col}_std_{window}'] = forecast_df[target_col].rolling(
                        window=window, min_periods=1
                    ).std()
            
            # Trend features
            forecast_df['trend'] = range(len(forecast_df))
            
            # Fill NaN values
            forecast_df = forecast_df.fillna(method='bfill').fillna(method='ffill')
            
            logger.info(f"Time series features prepared: {forecast_df.shape}")
            return forecast_df
            
        except Exception as e:
            logger.error(f"Error preparing time series features: {str(e)}")
            raise
    
    def train_prophet_model(self, df: pd.DataFrame, date_col: str, target_col: str) -> Dict[str, Any]:
        """
        Train Prophet model for time series forecasting
        Following Prophet best practices
        """
        if not PROPHET_AVAILABLE:
            return {"error": "Prophet not available"}
            
        try:
            # Prepare data for Prophet
            prophet_df = df[[date_col, target_col]].copy()
            prophet_df.columns = ['ds', 'y']
            prophet_df = prophet_df.sort_values('ds')
            
            # Initialize Prophet model with business-appropriate settings
            model = Prophet(
                daily_seasonality=True,
                weekly_seasonality=True,
                yearly_seasonality=True,
                changepoint_prior_scale=0.05,  # Conservative approach for SME data
                seasonality_prior_scale=10.0,
                holidays_prior_scale=10.0,
                changepoint_range=0.8,
                interval_width=0.80
            )
            
            # Fit model
            model.fit(prophet_df)
            
            # Store model
            self.models['prophet'] = model
            
            # Generate predictions for validation
            train_size = int(len(prophet_df) * 0.8)
            train_data = prophet_df[:train_size]
            test_data = prophet_df[train_size:]
            
            if len(test_data) > 0:
                # Predict on test data
                test_forecast = model.predict(test_data[['ds']])
                
                # Calculate performance metrics
                mae = mean_absolute_error(test_data['y'], test_forecast['yhat'])
                mse = mean_squared_error(test_data['y'], test_forecast['yhat'])
                r2 = r2_score(test_data['y'], test_forecast['yhat'])
                
                performance = {
                    'mae': mae,
                    'mse': mse,
                    'rmse': np.sqrt(mse),
                    'r2_score': r2,
                    'mape': np.mean(np.abs((test_data['y'] - test_forecast['yhat']) / test_data['y'])) * 100
                }
            else:
                performance = {'mae': 0, 'mse': 0, 'rmse': 0, 'r2_score': 0, 'mape': 0}
            
            logger.info("Prophet model trained successfully")
            return {
                'model': model,
                'performance': performance,
                'model_type': 'prophet'
            }
            
        except Exception as e:
            logger.error(f"Error training Prophet model: {str(e)}")
            return {"error": f"Prophet training error: {str(e)}"}
    
    def train_xgboost_model(self, df: pd.DataFrame, date_col: str, target_col: str) -> Dict[str, Any]:
        """
        Train XGBoost model for forecasting
        Following XGBoost best practices
        """
        if not XGBOOST_AVAILABLE:
            return {"error": "XGBoost not available"}
            
        try:
            # Prepare features
            feature_df = self.prepare_time_series_features(df, date_col, target_col)
            
            # Select feature columns
            exclude_cols = [date_col, target_col]
            feature_cols = [col for col in feature_df.columns if col not in exclude_cols]
            
            X = feature_df[feature_cols]
            y = feature_df[target_col]
            
            # Train/test split
            split_idx = int(len(X) * 0.8)
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train XGBoost model
            model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                eval_metric='mae'
            )
            
            model.fit(X_train_scaled, y_train)
            
            # Store model and scaler
            self.models['xgboost'] = model
            self.scalers['xgboost'] = scaler
            self.feature_columns = feature_cols
            
            # Evaluate model
            if len(X_test) > 0:
                y_pred = model.predict(X_test_scaled)
                
                performance = {
                    'mae': mean_absolute_error(y_test, y_pred),
                    'mse': mean_squared_error(y_test, y_pred),
                    'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                    'r2_score': r2_score(y_test, y_pred),
                    'mape': np.mean(np.abs((y_test - y_pred) / y_test)) * 100
                }
            else:
                performance = {'mae': 0, 'mse': 0, 'rmse': 0, 'r2_score': 0, 'mape': 0}
            
            logger.info("XGBoost model trained successfully")
            return {
                'model': model,
                'scaler': scaler,
                'feature_columns': feature_cols,
                'performance': performance,
                'model_type': 'xgboost'
            }
            
        except Exception as e:
            logger.error(f"Error training XGBoost model: {str(e)}")
            return {"error": f"XGBoost training error: {str(e)}"}
    
    def train_ensemble_model(self, df: pd.DataFrame, date_col: str, target_col: str) -> Dict[str, Any]:
        """
        Train ensemble model combining multiple approaches
        Following ensemble learning best practices
        """
        try:
            models_trained = []
            performances = []
            
            # Train Random Forest (always available)
            rf_result = self.train_random_forest_model(df, date_col, target_col)
            if 'error' not in rf_result:
                models_trained.append(rf_result)
                performances.append(rf_result['performance'])
            
            # Train Prophet if available
            if PROPHET_AVAILABLE:
                prophet_result = self.train_prophet_model(df, date_col, target_col)
                if 'error' not in prophet_result:
                    models_trained.append(prophet_result)
                    performances.append(prophet_result['performance'])
            
            # Train XGBoost if available
            if XGBOOST_AVAILABLE:
                xgb_result = self.train_xgboost_model(df, date_col, target_col)
                if 'error' not in xgb_result:
                    models_trained.append(xgb_result)
                    performances.append(xgb_result['performance'])
            
            if not models_trained:
                return {"error": "No models could be trained"}
            
            # Calculate ensemble weights based on performance
            weights = []
            for perf in performances:
                r2 = perf.get('r2_score', 0)
                weight = max(0.1, r2)  # Minimum weight of 0.1
                weights.append(weight)
            
            # Normalize weights
            total_weight = sum(weights)
            weights = [w / total_weight for w in weights]
            
            # Store ensemble information
            ensemble_info = {
                'models': models_trained,
                'weights': weights,
                'model_types': [m['model_type'] for m in models_trained],
                'avg_performance': {
                    'mae': np.average([p['mae'] for p in performances], weights=weights),
                    'r2_score': np.average([p['r2_score'] for p in performances], weights=weights)
                }
            }
            
            logger.info(f"Ensemble model trained with {len(models_trained)} models")
            return ensemble_info
            
        except Exception as e:
            logger.error(f"Error training ensemble model: {str(e)}")
            return {"error": f"Ensemble training error: {str(e)}"}
    
    def train_random_forest_model(self, df: pd.DataFrame, date_col: str, target_col: str) -> Dict[str, Any]:
        """
        Train Random Forest model (fallback option)
        Following sklearn best practices
        """
        try:
            # Prepare features
            feature_df = self.prepare_time_series_features(df, date_col, target_col)
            
            # Select feature columns
            exclude_cols = [date_col, target_col]
            feature_cols = [col for col in feature_df.columns if col not in exclude_cols]
            
            X = feature_df[feature_cols]
            y = feature_df[target_col]
            
            # Train/test split
            split_idx = int(len(X) * 0.8)
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]
            
            # Train Random Forest
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            )
            
            model.fit(X_train, y_train)
            
            # Store model
            self.models['random_forest'] = model
            self.feature_columns = feature_cols
            
            # Evaluate model
            if len(X_test) > 0:
                y_pred = model.predict(X_test)
                
                performance = {
                    'mae': mean_absolute_error(y_test, y_pred),
                    'mse': mean_squared_error(y_test, y_pred),
                    'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
                    'r2_score': r2_score(y_test, y_pred),
                    'mape': np.mean(np.abs((y_test - y_pred) / y_test)) * 100
                }
            else:
                performance = {'mae': 0, 'mse': 0, 'rmse': 0, 'r2_score': 0, 'mape': 0}
            
            logger.info("Random Forest model trained successfully")
            return {
                'model': model,
                'feature_columns': feature_cols,
                'performance': performance,
                'model_type': 'random_forest'
            }
            
        except Exception as e:
            logger.error(f"Error training Random Forest model: {str(e)}")
            return {"error": f"Random Forest training error: {str(e)}"}
    
    def generate_forecast(
        self, 
        df: pd.DataFrame, 
        date_col: str, 
        target_col: str, 
        periods: int = 30,
        model_type: str = 'auto'
    ) -> Dict[str, Any]:
        """
        Generate forecast using specified or best available model
        Following forecasting best practices
        
        Args:
            df: Historical data
            date_col: Date column name
            target_col: Target variable name
            periods: Number of periods to forecast
            model_type: 'auto', 'prophet', 'xgboost', 'random_forest', or 'ensemble'
            
        Returns:
            Dictionary with forecast results and visualizations
        """
        try:
            logger.info(f"Generating {periods}-period forecast using {model_type} model")
            
            # Determine best model if auto
            if model_type == 'auto':
                if PROPHET_AVAILABLE and XGBOOST_AVAILABLE:
                    model_type = 'ensemble'
                elif PROPHET_AVAILABLE:
                    model_type = 'prophet'
                elif XGBOOST_AVAILABLE:
                    model_type = 'xgboost'
                else:
                    model_type = 'random_forest'
            
            # Train model and generate forecast
            if model_type == 'prophet' and PROPHET_AVAILABLE:
                return self._forecast_with_prophet(df, date_col, target_col, periods)
            elif model_type == 'xgboost' and XGBOOST_AVAILABLE:
                return self._forecast_with_xgboost(df, date_col, target_col, periods)
            elif model_type == 'ensemble':
                return self._forecast_with_ensemble(df, date_col, target_col, periods)
            else:
                return self._forecast_with_random_forest(df, date_col, target_col, periods)
                
        except Exception as e:
            logger.error(f"Error generating forecast: {str(e)}")
            return {"error": f"Forecast generation error: {str(e)}"}
    
    def _forecast_with_prophet(
        self, 
        df: pd.DataFrame, 
        date_col: str, 
        target_col: str, 
        periods: int
    ) -> Dict[str, Any]:
        """Generate forecast using Prophet model"""
        try:
            # Train model
            model_result = self.train_prophet_model(df, date_col, target_col)
            if 'error' in model_result:
                return model_result
            
            model = model_result['model']
            
            # Create future dataframe
            future = model.make_future_dataframe(periods=periods)
            
            # Generate forecast
            forecast = model.predict(future)
            
            # Extract results
            historical_dates = df[date_col].tolist()
            historical_values = df[target_col].tolist()
            
            future_dates = forecast['ds'].tail(periods).tolist()
            future_values = forecast['yhat'].tail(periods).tolist()
            future_lower = forecast['yhat_lower'].tail(periods).tolist()
            future_upper = forecast['yhat_upper'].tail(periods).tolist()
            
            # Create visualization
            fig = self._create_forecast_visualization(
                historical_dates, historical_values,
                future_dates, future_values,
                future_lower, future_upper,
                "Prophet Forecast"
            )
            
            # Calculate insights
            current_avg = np.mean(historical_values[-30:]) if len(historical_values) >= 30 else np.mean(historical_values)
            forecast_avg = np.mean(future_values)
            growth_prediction = ((forecast_avg - current_avg) / current_avg) * 100
            
            return {
                "model_performance": model_result['performance'],
                "forecast_chart": fig,
                "insights": {
                    "growth_prediction": growth_prediction,
                    "forecast_avg": forecast_avg,
                    "current_avg": current_avg,
                    "confidence": "High" if model_result['performance']['r2_score'] > 0.8 else "Medium",
                    "model_used": "Prophet"
                },
                "future_dates": future_dates,
                "future_values": future_values,
                "confidence_intervals": {
                    "lower": future_lower,
                    "upper": future_upper
                }
            }
            
        except Exception as e:
            logger.error(f"Error in Prophet forecasting: {str(e)}")
            return {"error": f"Prophet forecasting error: {str(e)}"}
    
    def _forecast_with_xgboost(
        self, 
        df: pd.DataFrame, 
        date_col: str, 
        target_col: str, 
        periods: int
    ) -> Dict[str, Any]:
        """Generate forecast using XGBoost model"""
        try:
            # Train model
            model_result = self.train_xgboost_model(df, date_col, target_col)
            if 'error' in model_result:
                return model_result
            
            model = model_result['model']
            scaler = model_result['scaler']
            feature_cols = model_result['feature_columns']
            
            # Prepare historical data with features
            feature_df = self.prepare_time_series_features(df, date_col, target_col)
            
            # Generate future dates
            last_date = pd.to_datetime(df[date_col].max())
            future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=periods, freq='D')
            
            # Generate future features
            future_data = []
            current_df = feature_df.copy()
            
            for i, future_date in enumerate(future_dates):
                # Create a row for the future date
                future_row = pd.Series(index=current_df.columns, dtype=float)
                future_row[date_col] = future_date
                
                # Add time-based features
                future_row['year'] = future_date.year
                future_row['month'] = future_date.month
                future_row['day'] = future_date.day
                future_row['dayofweek'] = future_date.dayofweek
                future_row['dayofyear'] = future_date.dayofyear
                future_row['quarter'] = future_date.quarter
                future_row['week'] = future_date.isocalendar().week
                
                # Cyclical features
                future_row['month_sin'] = np.sin(2 * np.pi * future_date.month / 12)
                future_row['month_cos'] = np.cos(2 * np.pi * future_date.month / 12)
                future_row['day_sin'] = np.sin(2 * np.pi * future_date.dayofweek / 7)
                future_row['day_cos'] = np.cos(2 * np.pi * future_date.dayofweek / 7)
                
                # Trend feature
                future_row['trend'] = len(current_df) + i
                
                # Use recent values for lag and moving average features
                recent_values = current_df[target_col].tail(30).values
                if len(recent_values) > 0:
                    recent_avg = np.mean(recent_values)
                    for lag in [1, 7, 30]:
                        future_row[f'{target_col}_lag_{lag}'] = recent_avg
                    for window in [7, 14, 30]:
                        future_row[f'{target_col}_ma_{window}'] = recent_avg
                        future_row[f'{target_col}_std_{window}'] = np.std(recent_values) if len(recent_values) > 1 else 0
                
                future_data.append(future_row)
            
            # Convert to dataframe and get features
            future_df = pd.DataFrame(future_data)
            X_future = future_df[feature_cols].fillna(0)
            X_future_scaled = scaler.transform(X_future)
            
            # Generate predictions
            future_values = model.predict(X_future_scaled)
            
            # Create visualization
            historical_dates = df[date_col].tolist()
            historical_values = df[target_col].tolist()
            
            fig = self._create_forecast_visualization(
                historical_dates, historical_values,
                future_dates.tolist(), future_values.tolist(),
                None, None,  # No confidence intervals for XGBoost
                "XGBoost Forecast"
            )
            
            # Calculate insights
            current_avg = np.mean(historical_values[-30:]) if len(historical_values) >= 30 else np.mean(historical_values)
            forecast_avg = np.mean(future_values)
            growth_prediction = ((forecast_avg - current_avg) / current_avg) * 100
            
            return {
                "model_performance": model_result['performance'],
                "forecast_chart": fig,
                "insights": {
                    "growth_prediction": growth_prediction,
                    "forecast_avg": forecast_avg,
                    "current_avg": current_avg,
                    "confidence": "High" if model_result['performance']['r2_score'] > 0.8 else "Medium",
                    "model_used": "XGBoost"
                },
                "future_dates": future_dates.tolist(),
                "future_values": future_values.tolist()
            }
            
        except Exception as e:
            logger.error(f"Error in XGBoost forecasting: {str(e)}")
            return {"error": f"XGBoost forecasting error: {str(e)}"}
    
    def _forecast_with_random_forest(
        self, 
        df: pd.DataFrame, 
        date_col: str, 
        target_col: str, 
        periods: int
    ) -> Dict[str, Any]:
        """Generate forecast using Random Forest model (fallback)"""
        try:
            # Train model
            model_result = self.train_random_forest_model(df, date_col, target_col)
            if 'error' in model_result:
                return model_result
            
            model = model_result['model']
            feature_cols = model_result['feature_columns']
            
            # Prepare features and generate predictions similar to XGBoost
            feature_df = self.prepare_time_series_features(df, date_col, target_col)
            
            # Generate future dates
            last_date = pd.to_datetime(df[date_col].max())
            future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=periods, freq='D')
            
            # Simple future feature generation
            future_data = []
            for i, future_date in enumerate(future_dates):
                future_row = pd.Series(index=feature_df.columns, dtype=float)
                future_row[date_col] = future_date
                
                # Basic time features
                future_row['year'] = future_date.year
                future_row['month'] = future_date.month
                future_row['day'] = future_date.day
                future_row['dayofweek'] = future_date.dayofweek
                future_row['dayofyear'] = future_date.dayofyear
                future_row['quarter'] = future_date.quarter
                future_row['week'] = future_date.isocalendar().week
                
                # Cyclical features
                future_row['month_sin'] = np.sin(2 * np.pi * future_date.month / 12)
                future_row['month_cos'] = np.cos(2 * np.pi * future_date.month / 12)
                future_row['day_sin'] = np.sin(2 * np.pi * future_date.dayofweek / 7)
                future_row['day_cos'] = np.cos(2 * np.pi * future_date.dayofweek / 7)
                
                # Trend
                future_row['trend'] = len(feature_df) + i
                
                # Use recent averages for lag/MA features
                recent_avg = feature_df[target_col].tail(30).mean()
                for col in feature_cols:
                    if col not in future_row or pd.isna(future_row[col]):
                        if 'lag' in col or 'ma' in col or 'std' in col:
                            future_row[col] = recent_avg if 'std' not in col else feature_df[col].tail(30).mean()
                
                future_data.append(future_row)
            
            # Make predictions
            future_df = pd.DataFrame(future_data)
            X_future = future_df[feature_cols].fillna(0)
            future_values = model.predict(X_future)
            
            # Create visualization
            historical_dates = df[date_col].tolist()
            historical_values = df[target_col].tolist()
            
            fig = self._create_forecast_visualization(
                historical_dates, historical_values,
                future_dates.tolist(), future_values.tolist(),
                None, None,
                "Random Forest Forecast"
            )
            
            # Calculate insights
            current_avg = np.mean(historical_values[-30:]) if len(historical_values) >= 30 else np.mean(historical_values)
            forecast_avg = np.mean(future_values)
            growth_prediction = ((forecast_avg - current_avg) / current_avg) * 100
            
            return {
                "model_performance": model_result['performance'],
                "forecast_chart": fig,
                "insights": {
                    "growth_prediction": growth_prediction,
                    "forecast_avg": forecast_avg,
                    "current_avg": current_avg,
                    "confidence": "Medium" if model_result['performance']['r2_score'] > 0.6 else "Low",
                    "model_used": "Random Forest"
                },
                "future_dates": future_dates.tolist(),
                "future_values": future_values.tolist()
            }
            
        except Exception as e:
            logger.error(f"Error in Random Forest forecasting: {str(e)}")
            return {"error": f"Random Forest forecasting error: {str(e)}"}
    
    def _forecast_with_ensemble(
        self, 
        df: pd.DataFrame, 
        date_col: str, 
        target_col: str, 
        periods: int
    ) -> Dict[str, Any]:
        """Generate forecast using ensemble of models"""
        try:
            # Train ensemble
            ensemble_result = self.train_ensemble_model(df, date_col, target_col)
            if 'error' in ensemble_result:
                return ensemble_result
            
            # Generate individual forecasts
            individual_forecasts = []
            models = ensemble_result['models']
            weights = ensemble_result['weights']
            
            for model_info in models:
                model_type = model_info['model_type']
                
                if model_type == 'prophet':
                    forecast = self._forecast_with_prophet(df, date_col, target_col, periods)
                elif model_type == 'xgboost':
                    forecast = self._forecast_with_xgboost(df, date_col, target_col, periods)
                else:  # random_forest
                    forecast = self._forecast_with_random_forest(df, date_col, target_col, periods)
                
                if 'error' not in forecast:
                    individual_forecasts.append(forecast)
            
            if not individual_forecasts:
                return {"error": "No individual forecasts available for ensemble"}
            
            # Combine forecasts using weights
            ensemble_values = np.zeros(periods)
            for i, forecast in enumerate(individual_forecasts):
                weight = weights[i] if i < len(weights) else 1.0 / len(individual_forecasts)
                ensemble_values += np.array(forecast['future_values']) * weight
            
            # Use dates from first forecast
            future_dates = individual_forecasts[0]['future_dates']
            
            # Create visualization
            historical_dates = df[date_col].tolist()
            historical_values = df[target_col].tolist()
            
            fig = self._create_forecast_visualization(
                historical_dates, historical_values,
                future_dates, ensemble_values.tolist(),
                None, None,
                "Ensemble Forecast"
            )
            
            # Calculate insights
            current_avg = np.mean(historical_values[-30:]) if len(historical_values) >= 30 else np.mean(historical_values)
            forecast_avg = np.mean(ensemble_values)
            growth_prediction = ((forecast_avg - current_avg) / current_avg) * 100
            
            return {
                "model_performance": ensemble_result['avg_performance'],
                "forecast_chart": fig,
                "insights": {
                    "growth_prediction": growth_prediction,
                    "forecast_avg": forecast_avg,
                    "current_avg": current_avg,
                    "confidence": "High",
                    "model_used": f"Ensemble ({len(individual_forecasts)} models)"
                },
                "future_dates": future_dates,
                "future_values": ensemble_values.tolist(),
                "individual_forecasts": individual_forecasts
            }
            
        except Exception as e:
            logger.error(f"Error in ensemble forecasting: {str(e)}")
            return {"error": f"Ensemble forecasting error: {str(e)}"}
    
    def _create_forecast_visualization(
        self,
        historical_dates: List,
        historical_values: List,
        future_dates: List,
        future_values: List,
        lower_bound: Optional[List] = None,
        upper_bound: Optional[List] = None,
        title: str = "Forecast"
    ) -> go.Figure:
        """Create forecast visualization using Plotly"""
        try:
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=historical_dates,
                y=historical_values,
                mode='lines',
                name='Historical Data',
                line=dict(color='#667eea', width=2)
            ))
            
            # Future predictions
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=future_values,
                mode='lines',
                name='Forecast',
                line=dict(color='#f093fb', width=2, dash='dash')
            ))
            
            # Confidence intervals if available
            if lower_bound and upper_bound:
                fig.add_trace(go.Scatter(
                    x=future_dates,
                    y=upper_bound,
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False,
                    name='Upper Bound'
                ))
                
                fig.add_trace(go.Scatter(
                    x=future_dates,
                    y=lower_bound,
                    mode='lines',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor='rgba(240, 147, 251, 0.2)',
                    name='Confidence Interval',
                    showlegend=True
                ))
            
            fig.update_layout(
                title=title,
                xaxis_title="Date",
                yaxis_title="Value",
                template="plotly_white",
                height=500,
                hovermode='x unified'
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating forecast visualization: {str(e)}")
            # Return empty figure as fallback
            return go.Figure()