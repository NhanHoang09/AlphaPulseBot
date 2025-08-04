"""
Prediction Models Module
Machine Learning models cho dự báo xu hướng thị trường
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Conv1D, MaxPooling1D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
import joblib
import logging
from typing import Dict, List, Tuple, Optional, Any
import os
from datetime import datetime

class PredictionModels:
    """Class quản lý các mô hình dự báo"""
    
    def __init__(self, model_save_path: str = "models/"):
        self.logger = logging.getLogger(__name__)
        self.model_save_path = model_save_path
        self.scaler = StandardScaler()
        self.models = {}
        
        # Tạo thư mục lưu models
        os.makedirs(model_save_path, exist_ok=True)
    
    def prepare_data(self, data: pd.DataFrame, target_col: str = 'Close', 
                    lookback: int = 60, prediction_horizon: int = 1) -> Tuple[np.ndarray, np.ndarray]:
        """
        Chuẩn bị dữ liệu cho training
        
        Args:
            data: DataFrame với dữ liệu
            target_col: Cột target
            lookback: Số ngày nhìn lại
            prediction_horizon: Số ngày dự báo trước
        
        Returns:
            X, y arrays cho training
        """
        # Chọn features
        feature_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Returns', 'Volatility']
        available_cols = [col for col in feature_cols if col in data.columns]
        
        if len(available_cols) < 3:
            available_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            available_cols = [col for col in available_cols if col in data.columns]
        
        # Tạo sequences
        X, y = [], []
        
        for i in range(lookback, len(data) - prediction_horizon + 1):
            X.append(data[available_cols].iloc[i-lookback:i].values)
            y.append(data[target_col].iloc[i:i+prediction_horizon].values)
        
        return np.array(X), np.array(y)
    
    def build_lstm_model(self, input_shape: Tuple[int, int], output_size: int = 1) -> tf.keras.Model:
        """
        Xây dựng mô hình LSTM
        
        Args:
            input_shape: Shape của input (timesteps, features)
            output_size: Số output cần dự báo
        
        Returns:
            LSTM model
        """
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(output_size)
        ])
        
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
        return model
    
    def build_cnn_lstm_model(self, input_shape: Tuple[int, int], output_size: int = 1) -> tf.keras.Model:
        """
        Xây dựng mô hình CNN-LSTM hybrid
        
        Args:
            input_shape: Shape của input
            output_size: Số output cần dự báo
        
        Returns:
            CNN-LSTM model
        """
        model = Sequential([
            Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=input_shape),
            MaxPooling1D(pool_size=2),
            Conv1D(filters=32, kernel_size=3, activation='relu'),
            MaxPooling1D(pool_size=2),
            LSTM(50, return_sequences=True),
            Dropout(0.2),
            LSTM(25, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(output_size)
        ])
        
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
        return model
    
    def train_lstm_model(self, data: pd.DataFrame, symbol: str, 
                        lookback: int = 60, prediction_horizon: int = 1,
                        epochs: int = 100, batch_size: int = 32) -> Dict[str, Any]:
        """
        Training mô hình LSTM
        
        Args:
            data: Dữ liệu training
            symbol: Mã symbol
            lookback: Số ngày nhìn lại
            prediction_horizon: Số ngày dự báo trước
            epochs: Số epochs training
            batch_size: Batch size
        
        Returns:
            Dictionary với thông tin training
        """
        try:
            # Chuẩn bị dữ liệu
            X, y = self.prepare_data(data, lookback=lookback, prediction_horizon=prediction_horizon)
            
            if len(X) < 100:
                return {"error": "Không đủ dữ liệu để training"}
            
            # Split data
            split_idx = int(0.8 * len(X))
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]
            
            # Scale data
            X_train_scaled = self.scaler.fit_transform(X_train.reshape(-1, X_train.shape[-1])).reshape(X_train.shape)
            X_test_scaled = self.scaler.transform(X_test.reshape(-1, X_test.shape[-1])).reshape(X_test.shape)
            
            # Build model
            model = self.build_lstm_model((X_train.shape[1], X_train.shape[2]), y_train.shape[1])
            
            # Callbacks
            early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
            
            # Training
            history = model.fit(
                X_train_scaled, y_train,
                validation_data=(X_test_scaled, y_test),
                epochs=epochs,
                batch_size=batch_size,
                callbacks=[early_stopping],
                verbose=1
            )
            
            # Evaluation
            y_pred = model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Save model
            model_path = os.path.join(self.model_save_path, f"lstm_{symbol}.h5")
            model.save(model_path)
            
            # Save scaler
            scaler_path = os.path.join(self.model_save_path, f"scaler_{symbol}.pkl")
            joblib.dump(self.scaler, scaler_path)
            
            self.models[f"lstm_{symbol}"] = {
                'model': model,
                'scaler': self.scaler,
                'lookback': lookback,
                'prediction_horizon': prediction_horizon
            }
            
            return {
                'model_type': 'LSTM',
                'symbol': symbol,
                'mse': mse,
                'mae': mae,
                'r2': r2,
                'model_path': model_path,
                'scaler_path': scaler_path,
                'history': history.history
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi khi training LSTM model cho {symbol}: {str(e)}")
            return {"error": str(e)}
    
    def train_ensemble_model(self, data: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """
        Training ensemble model với Random Forest và Gradient Boosting
        
        Args:
            data: Dữ liệu training
            symbol: Mã symbol
        
        Returns:
            Dictionary với thông tin training
        """
        try:
            # Chuẩn bị features
            feature_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Returns', 'Volatility']
            available_cols = [col for col in feature_cols if col in data.columns]
            
            if len(available_cols) < 3:
                available_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
                available_cols = [col for col in available_cols if col in data.columns]
            
            # Tạo lag features
            df = data[available_cols].copy()
            for col in available_cols:
                for lag in [1, 2, 3, 5, 10]:
                    df[f'{col}_lag_{lag}'] = df[col].shift(lag)
            
            # Tạo target (giá ngày mai)
            df['target'] = df['Close'].shift(-1)
            
            # Drop NaN
            df = df.dropna()
            
            if len(df) < 100:
                return {"error": "Không đủ dữ liệu để training"}
            
            # Prepare X, y
            feature_cols = [col for col in df.columns if col != 'target']
            X = df[feature_cols]
            y = df['target']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train models
            models = {
                'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
                'gradient_boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
                'svr': SVR(kernel='rbf'),
                'ridge': Ridge(alpha=1.0)
            }
            
            results = {}
            
            for name, model in models.items():
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
                
                results[name] = {
                    'mse': mean_squared_error(y_test, y_pred),
                    'mae': mean_absolute_error(y_test, y_pred),
                    'r2': r2_score(y_test, y_pred),
                    'model': model
                }
            
            # Save best model
            best_model_name = min(results.keys(), key=lambda x: results[x]['mse'])
            best_model = results[best_model_name]['model']
            
            model_path = os.path.join(self.model_save_path, f"ensemble_{symbol}.pkl")
            joblib.dump(best_model, model_path)
            
            scaler_path = os.path.join(self.model_save_path, f"ensemble_scaler_{symbol}.pkl")
            joblib.dump(self.scaler, scaler_path)
            
            self.models[f"ensemble_{symbol}"] = {
                'model': best_model,
                'scaler': self.scaler,
                'feature_cols': feature_cols
            }
            
            return {
                'model_type': 'Ensemble',
                'symbol': symbol,
                'best_model': best_model_name,
                'results': results,
                'model_path': model_path,
                'scaler_path': scaler_path
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi khi training ensemble model cho {symbol}: {str(e)}")
            return {"error": str(e)}
    
    def predict(self, data: pd.DataFrame, symbol: str, model_type: str = 'lstm') -> Dict[str, Any]:
        """
        Dự báo giá tương lai
        
        Args:
            data: Dữ liệu hiện tại
            symbol: Mã symbol
            model_type: Loại model ('lstm' hoặc 'ensemble')
        
        Returns:
            Dictionary với kết quả dự báo
        """
        try:
            model_key = f"{model_type}_{symbol}"
            
            if model_key not in self.models:
                # Load model từ file
                if model_type == 'lstm':
                    model_path = os.path.join(self.model_save_path, f"lstm_{symbol}.h5")
                    scaler_path = os.path.join(self.model_save_path, f"scaler_{symbol}.pkl")
                    
                    if not os.path.exists(model_path):
                        return {"error": f"Model {model_key} chưa được training"}
                    
                    model = tf.keras.models.load_model(model_path)
                    scaler = joblib.load(scaler_path)
                    
                    # Chuẩn bị dữ liệu cho prediction
                    lookback = 60  # Default
                    X, _ = self.prepare_data(data, lookback=lookback, prediction_horizon=1)
                    
                    if len(X) == 0:
                        return {"error": "Không đủ dữ liệu để dự báo"}
                    
                    X_scaled = scaler.transform(X[-1].reshape(-1, X.shape[-1])).reshape(1, X.shape[1], X.shape[2])
                    prediction = model.predict(X_scaled)
                    
                else:  # ensemble
                    model_path = os.path.join(self.model_save_path, f"ensemble_{symbol}.pkl")
                    scaler_path = os.path.join(self.model_save_path, f"ensemble_scaler_{symbol}.pkl")
                    
                    if not os.path.exists(model_path):
                        return {"error": f"Model {model_key} chưa được training"}
                    
                    model = joblib.load(model_path)
                    scaler = joblib.load(scaler_path)
                    
                    # Chuẩn bị features
                    feature_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Returns', 'Volatility']
                    available_cols = [col for col in feature_cols if col in data.columns]
                    
                    if len(available_cols) < 3:
                        available_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
                        available_cols = [col for col in available_cols if col in data.columns]
                    
                    # Tạo lag features
                    df = data[available_cols].copy()
                    for col in available_cols:
                        for lag in [1, 2, 3, 5, 10]:
                            df[f'{col}_lag_{lag}'] = df[col].shift(lag)
                    
                    df = df.dropna()
                    
                    if len(df) == 0:
                        return {"error": "Không đủ dữ liệu để dự báo"}
                    
                    X = df.iloc[-1:][[col for col in df.columns if 'lag' in col or col in available_cols]]
                    X_scaled = scaler.transform(X)
                    prediction = model.predict(X_scaled)
                
                return {
                    'symbol': symbol,
                    'model_type': model_type,
                    'current_price': data['Close'].iloc[-1],
                    'predicted_price': prediction[0][0] if model_type == 'lstm' else prediction[0],
                    'prediction_date': datetime.now(),
                    'confidence': 0.8  # Placeholder
                }
            
            else:
                # Use loaded model
                model_info = self.models[model_key]
                # Implementation similar to above
                pass
                
        except Exception as e:
            self.logger.error(f"Lỗi khi dự báo cho {symbol}: {str(e)}")
            return {"error": str(e)}
    
    def get_model_performance(self, symbol: str, model_type: str = 'lstm') -> Dict[str, Any]:
        """
        Lấy thông tin performance của model
        
        Args:
            symbol: Mã symbol
            model_type: Loại model
        
        Returns:
            Dictionary với thông tin performance
        """
        model_key = f"{model_type}_{symbol}"
        
        if model_key in self.models:
            return {
                'symbol': symbol,
                'model_type': model_type,
                'status': 'loaded',
                'loaded_at': datetime.now()
            }
        else:
            model_path = os.path.join(self.model_save_path, f"{model_type}_{symbol}.h5")
            if os.path.exists(model_path):
                return {
                    'symbol': symbol,
                    'model_type': model_type,
                    'status': 'saved',
                    'file_path': model_path
                }
            else:
                return {
                    'symbol': symbol,
                    'model_type': model_type,
                    'status': 'not_found'
                }

# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Test prediction models
    from src.data.data_collector import DataCollector
    from src.analysis.technical_analysis import TechnicalAnalyzer
    
    collector = DataCollector()
    analyzer = TechnicalAnalyzer()
    predictor = PredictionModels()
    
    # Lấy và phân tích dữ liệu
    data = collector.get_stock_data("AAPL", period="2y")
    if not data.empty:
        data_with_indicators = analyzer.add_all_indicators(data)
        
        # Training LSTM model
        lstm_result = predictor.train_lstm_model(data_with_indicators, "AAPL")
        print("LSTM Training Result:", lstm_result)
        
        # Training Ensemble model
        ensemble_result = predictor.train_ensemble_model(data_with_indicators, "AAPL")
        print("Ensemble Training Result:", ensemble_result)
        
        # Prediction
        prediction = predictor.predict(data_with_indicators, "AAPL", "lstm")
        print("Prediction:", prediction) 