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
from tensorflow.keras.layers import LSTM, Dense, Dropout, Conv1D, MaxPooling1D, BatchNormalization
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
        self.scaler = StandardScaler()  # Cho ensemble models
        self.lstm_scaler = StandardScaler()  # Cho LSTM features
        self.target_scaler = StandardScaler()  # Cho LSTM target
        self.models = {}
        
        # Tạo thư mục lưu models
        os.makedirs(model_save_path, exist_ok=True)
    
    def load_model_safely(self, model_path: str) -> tf.keras.Model:
        """
        Load Keras model with compatibility handling
        
        Args:
            model_path: Path to the model file
            
        Returns:
            Loaded Keras model
        """
        try:
            # First try loading with default settings
            return tf.keras.models.load_model(model_path)
        except Exception as e:
            self.logger.warning(f"Failed to load model with default settings: {e}")
            
            try:
                # Try loading without compilation
                model = tf.keras.models.load_model(model_path, compile=False)
                # Recompile with compatible settings
                model.compile(optimizer='adam', loss='mse', metrics=['mae'])
                self.logger.info("Model loaded and recompiled successfully")
                return model
            except Exception as e2:
                self.logger.error(f"Failed to load model even without compilation: {e2}")
                raise e2
    
    def prepare_data(self, data: pd.DataFrame, target_col: str = 'Close', 
                    lookback: int = 30, prediction_horizon: int = 1, symbol: str = '') -> Tuple[np.ndarray, np.ndarray]:
        """
        Chuẩn bị dữ liệu cho training với auto-detection adaptive features
        
        Args:
            data: DataFrame với dữ liệu
            target_col: Cột target
            lookback: Số ngày nhìn lại
            prediction_horizon: Số ngày dự báo trước
            symbol: Mã cổ phiếu để auto-detection
        
        Returns:
            X, y arrays cho training
        """
        # Chọn features cơ bản
        base_features = ['Open', 'High', 'Low', 'Close', 'Volume']
        available_base = [col for col in base_features if col in data.columns]
        
        if len(available_base) < 3:
            self.logger.error(f"Không đủ features cơ bản: {available_base}")
            return np.array([]), np.array([])
        
        # Tạo DataFrame mới chỉ với base features để tránh conflict
        data_enhanced = pd.DataFrame()
        for col in available_base + [target_col]:
            data_enhanced[col] = data[col].values
        
        # Reset index để tránh duplicate labels
        data_enhanced = data_enhanced.reset_index(drop=True)
        
        # Auto-detect stock characteristics
        if symbol:
            characteristics = self.analyze_stock_characteristics(data_enhanced, symbol)
            stock_type = characteristics.get('type', 'balanced')
            strategy = characteristics.get('strategy', 'mixed')
            volatility = characteristics.get('volatility', 0.2)
        else:
            stock_type = 'balanced'
            strategy = 'mixed'
            volatility = 0.2
        
        self.logger.info(f"Creating adaptive features for {symbol} - Type: {stock_type}, Strategy: {strategy}")
        
        # Thêm technical features cơ bản
        if 'Close' in data_enhanced.columns:
            # Price momentum features (cơ bản cho mọi cổ phiếu)
            data_enhanced['Price_Change'] = data_enhanced['Close'].pct_change()
            data_enhanced['Price_Change_2d'] = data_enhanced['Close'].pct_change(2)
            data_enhanced['Price_Change_5d'] = data_enhanced['Close'].pct_change(5)
            
            # Moving averages (cơ bản)
            data_enhanced['MA_5'] = data_enhanced['Close'].rolling(window=5).mean()
            data_enhanced['MA_10'] = data_enhanced['Close'].rolling(window=10).mean()
            data_enhanced['MA_20'] = data_enhanced['Close'].rolling(window=20).mean()
            
            # Price relative to moving averages
            data_enhanced['Price_vs_MA5'] = data_enhanced['Close'] / data_enhanced['MA_5']
            data_enhanced['Price_vs_MA10'] = data_enhanced['Close'] / data_enhanced['MA_10']
            data_enhanced['Price_vs_MA20'] = data_enhanced['Close'] / data_enhanced['MA_20']
            
            # Volatility features
            data_enhanced['Volatility_5d'] = data_enhanced['Price_Change'].rolling(window=5).std()
            data_enhanced['Volatility_10d'] = data_enhanced['Price_Change'].rolling(window=10).std()
            
            # RSI-like features
            data_enhanced['Gain'] = data_enhanced['Price_Change'].where(data_enhanced['Price_Change'] > 0, 0)
            data_enhanced['Loss'] = -data_enhanced['Price_Change'].where(data_enhanced['Price_Change'] < 0, 0)
            data_enhanced['Avg_Gain_14'] = data_enhanced['Gain'].rolling(window=14).mean()
            data_enhanced['Avg_Loss_14'] = data_enhanced['Loss'].rolling(window=14).mean()
            data_enhanced['RS_14'] = data_enhanced['Avg_Gain_14'] / data_enhanced['Avg_Loss_14']
            data_enhanced['RSI_14'] = 100 - (100 / (1 + data_enhanced['RS_14']))
            
            # Volume features
            if 'Volume' in data_enhanced.columns:
                data_enhanced['Volume_MA_5'] = data_enhanced['Volume'].rolling(window=5).mean()
                data_enhanced['Volume_Ratio'] = data_enhanced['Volume'] / data_enhanced['Volume_MA_5']
                data_enhanced['Volume_Change'] = data_enhanced['Volume'].pct_change()
            
            # Price range features
            data_enhanced['High_Low_Ratio'] = data_enhanced['High'] / data_enhanced['Low']
            data_enhanced['Close_Open_Ratio'] = data_enhanced['Close'] / data_enhanced['Open']
            
            # Trend features
            data_enhanced['Trend_5d'] = (data_enhanced['Close'] - data_enhanced['Close'].shift(5)) / data_enhanced['Close'].shift(5)
            data_enhanced['Trend_10d'] = (data_enhanced['Close'] - data_enhanced['Close'].shift(10)) / data_enhanced['Close'].shift(10)
            
            # Adaptive features dựa trên auto-detection
            if stock_type in ['conservative', 'blue_chip'] or strategy == 'fundamental':
                # Features cho cổ phiếu ổn định
                self.logger.info(f"Adding conservative features for {symbol}")
                data_enhanced['MA_50'] = data_enhanced['Close'].rolling(window=50).mean()
                data_enhanced['MA_100'] = data_enhanced['Close'].rolling(window=100).mean()
                data_enhanced['Price_vs_MA50'] = data_enhanced['Close'] / data_enhanced['MA_50']
                data_enhanced['Price_vs_MA100'] = data_enhanced['Close'] / data_enhanced['MA_100']
                data_enhanced['Volatility_20d'] = data_enhanced['Price_Change'].rolling(window=20).std()
                data_enhanced['Stability_Index'] = 1 / (1 + data_enhanced['Volatility_20d'])
                data_enhanced['Trend_20d'] = (data_enhanced['Close'] - data_enhanced['Close'].shift(20)) / data_enhanced['Close'].shift(20)
                
            elif stock_type in ['aggressive'] or strategy == 'short_term':
                # Features cho cổ phiếu biến động cao
                self.logger.info(f"Adding aggressive features for {symbol}")
                data_enhanced['MA_15'] = data_enhanced['Close'].rolling(window=15).mean()
                data_enhanced['Price_vs_MA15'] = data_enhanced['Close'] / data_enhanced['MA_15']
                data_enhanced['Volatility_3d'] = data_enhanced['Price_Change'].rolling(window=3).std()
                data_enhanced['Momentum_5d'] = data_enhanced['Close'] / data_enhanced['Close'].shift(5) - 1
                
            else:  # balanced hoặc mixed strategy
                # Features cân bằng
                self.logger.info(f"Adding balanced features for {symbol}")
                data_enhanced['MA_30'] = data_enhanced['Close'].rolling(window=30).mean()
                data_enhanced['Price_vs_MA30'] = data_enhanced['Close'] / data_enhanced['MA_30']
                data_enhanced['Momentum_10d'] = data_enhanced['Close'] / data_enhanced['Close'].shift(10) - 1
                data_enhanced['Volatility_15d'] = data_enhanced['Price_Change'].rolling(window=15).std()
        
        # Forward fill cho NaN values
        data_enhanced = data_enhanced.ffill()
        
        # Backward fill cho các giá trị còn lại
        data_enhanced = data_enhanced.bfill()
        
        # Drop rows còn NaN (nếu có)
        data_enhanced = data_enhanced.dropna()
        
        # Reset index sau khi dropna
        data_enhanced = data_enhanced.reset_index(drop=True)
        
        self.logger.info(f"Enhanced data shape: {data_enhanced.shape}")
        
        # Kiểm tra dữ liệu sau khi clean
        if len(data_enhanced) < lookback + prediction_horizon:
            self.logger.error(f"Không đủ dữ liệu: {len(data_enhanced)} < {lookback + prediction_horizon}")
            return np.array([]), np.array([])
        
        # Chọn tất cả features trừ target
        feature_cols = [col for col in data_enhanced.columns if col != target_col]
        
        # Tạo sequences
        X, y = [], []
        
        # Chuyển sang numpy arrays để tránh pandas indexing issues
        feature_data = data_enhanced[feature_cols].values
        target_data = data_enhanced[target_col].values
        
        for i in range(lookback, len(data_enhanced) - prediction_horizon + 1):
            X.append(feature_data[i-lookback:i])
            # Ensure target has correct shape
            target_sequence = target_data[i:i+prediction_horizon]
            if len(target_sequence.shape) == 1:
                target_sequence = target_sequence.reshape(-1, 1)
            y.append(target_sequence)
        
        X_array = np.array(X)
        y_array = np.array(y)
        
        self.logger.info(f"Enhanced sequences created - X: {X_array.shape}, y: {y_array.shape}")
        
        # Kiểm tra NaN trong arrays
        if np.isnan(X_array).any() or np.isnan(y_array).any():
            self.logger.warning(f"Phát hiện NaN trong dữ liệu sau khi clean")
            return np.array([]), np.array([])
        
        return X_array, y_array
    
    def build_lstm_model(self, input_shape: Tuple[int, int], output_size: int = 1, symbol: str = '', 
                        characteristics: Dict[str, Any] = None) -> tf.keras.Model:
        """
        Xây dựng mô hình LSTM adaptive dựa trên auto-detection
        
        Args:
            input_shape: Shape của input (timesteps, features)
            output_size: Số output cần dự báo
            symbol: Mã cổ phiếu
            characteristics: Đặc điểm cổ phiếu từ auto-detection
        
        Returns:
            LSTM model
        """
        model = Sequential()
        
        # Input layer với normalization
        model.add(tf.keras.layers.Input(shape=input_shape))
        
        # Auto-determine architecture based on characteristics
        if characteristics:
            stock_type = characteristics.get('type', 'balanced')
            strategy = characteristics.get('strategy', 'mixed')
            volatility = characteristics.get('volatility', 0.2)
        else:
            stock_type = 'balanced'
            strategy = 'mixed'
            volatility = 0.2
        
        self.logger.info(f"Building model for {symbol} - Type: {stock_type}, Strategy: {strategy}, Volatility: {volatility:.3f}")
        
        # Adaptive architecture dựa trên auto-detection
        if stock_type in ['conservative', 'blue_chip'] or strategy == 'fundamental':
            # Architecture cho cổ phiếu ổn định
            self.logger.info(f"Building conservative model for {symbol}")
            model.add(LSTM(32, return_sequences=True))
            model.add(BatchNormalization())
            model.add(Dropout(0.1))
            
            model.add(LSTM(16, return_sequences=False))
            model.add(BatchNormalization())
            model.add(Dropout(0.1))
            
            model.add(Dense(16, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.005)))
            model.add(BatchNormalization())
            model.add(Dropout(0.05))
            
        elif stock_type in ['aggressive'] or strategy == 'short_term' or volatility > 0.3:
            # Architecture cho cổ phiếu biến động cao
            self.logger.info(f"Building aggressive model for {symbol}")
            model.add(LSTM(128, return_sequences=True))
            model.add(BatchNormalization())
            model.add(Dropout(0.3))
            
            model.add(LSTM(64, return_sequences=True))
            model.add(BatchNormalization())
            model.add(Dropout(0.3))
            
            model.add(LSTM(32, return_sequences=False))
            model.add(BatchNormalization())
            model.add(Dropout(0.2))
            
            model.add(Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)))
            model.add(BatchNormalization())
            model.add(Dropout(0.2))
            
            model.add(Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)))
            model.add(BatchNormalization())
            model.add(Dropout(0.1))
            
        else:  # balanced hoặc mixed strategy
            # Architecture cân bằng
            self.logger.info(f"Building balanced model for {symbol}")
            model.add(LSTM(64, return_sequences=True))
            model.add(BatchNormalization())
            model.add(Dropout(0.2))
            
            model.add(LSTM(32, return_sequences=False))
            model.add(BatchNormalization())
            model.add(Dropout(0.2))
            
            model.add(Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)))
            model.add(BatchNormalization())
            model.add(Dropout(0.1))
            
            model.add(Dense(16, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)))
            model.add(BatchNormalization())
            model.add(Dropout(0.1))
        
        # Output layer
        model.add(Dense(output_size))
        
        # Adaptive learning rate based on volatility
        if volatility > 0.3:
            learning_rate = 0.0005  # Low learning rate for high volatility
        elif volatility < 0.15:
            learning_rate = 0.002   # Higher learning rate for low volatility
        else:
            learning_rate = 0.001   # Default learning rate
        
        # Compile với adaptive optimizer
        optimizer = Adam(learning_rate=learning_rate, clipnorm=1.0)
        model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])
        
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
        model = Sequential()
        model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=input_shape))
        model.add(MaxPooling1D(pool_size=2))
        model.add(Conv1D(filters=32, kernel_size=3, activation='relu'))
        model.add(MaxPooling1D(pool_size=2))
        model.add(LSTM(50, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(25, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(25))
        model.add(Dense(output_size))
        
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
        return model
    
    def train_lstm_model(self, data: pd.DataFrame, symbol: str, 
                        lookback: int = 30, prediction_horizon: int = 1,
                        epochs: int = 100, batch_size: int = 16) -> Dict[str, Any]:
        """
        Training mô hình LSTM với adaptive parameters dựa trên loại cổ phiếu
        
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
            # Kiểm tra dữ liệu đầu vào
            if data.empty:
                return {"error": "Dữ liệu trống"}
            
            # Auto-detect stock characteristics
            characteristics = self.analyze_stock_characteristics(data, symbol)
            stock_type = characteristics.get('type', 'balanced')
            strategy = characteristics.get('strategy', 'mixed')
            volatility = characteristics.get('volatility', 0.2)
            
            # Adaptive parameters dựa trên auto-detection
            if stock_type in ['conservative', 'blue_chip'] or strategy == 'fundamental':
                self.logger.info(f"Using conservative parameters for {symbol}")
                adaptive_epochs = 80
                adaptive_batch_size = 32
                adaptive_lookback = 40
            elif stock_type in ['aggressive'] or strategy == 'short_term' or volatility > 0.3:
                self.logger.info(f"Using aggressive parameters for {symbol}")
                adaptive_epochs = 150
                adaptive_batch_size = 8
                adaptive_lookback = 25
            else:  # balanced hoặc mixed strategy
                self.logger.info(f"Using balanced parameters for {symbol}")
                adaptive_epochs = 100
                adaptive_batch_size = 16
                adaptive_lookback = 30
            
            # Override với parameters được truyền vào nếu khác
            if epochs != 100:
                adaptive_epochs = epochs
            if batch_size != 16:
                adaptive_batch_size = batch_size
            if lookback != 30:
                adaptive_lookback = lookback
            
            self.logger.info(f"Adaptive parameters: epochs={adaptive_epochs}, batch_size={adaptive_batch_size}, lookback={adaptive_lookback}")
            
            # Chuẩn bị dữ liệu
            X, y = self.prepare_data(data, lookback=adaptive_lookback, prediction_horizon=prediction_horizon, symbol=symbol)
            
            if len(X) == 0 or len(y) == 0:
                return {"error": "Không thể chuẩn bị dữ liệu"}
            
            if len(X) < 100:
                return {"error": f"Không đủ dữ liệu để training. Cần ít nhất 100 samples, hiện có {len(X)}"}
            
            # Kiểm tra NaN trong X, y
            if np.isnan(X).any() or np.isnan(y).any():
                return {"error": "Dữ liệu chứa NaN"}
            
            self.logger.info(f"Data prepared - X: {X.shape}, y: {y.shape}")
            
            # Split data với tỷ lệ 80-20
            split_idx = int(0.8 * len(X))
            X_train, X_test = X[:split_idx], X[split_idx:]
            y_train, y_test = y[:split_idx], y[split_idx:]
            
            self.logger.info(f"Data split - Train: {X_train.shape}, Test: {X_test.shape}")
            
            # Scale data cho cả features và target
            try:
                # Scale features
                X_train_reshaped = X_train.reshape(-1, X_train.shape[-1])
                X_test_reshaped = X_test.reshape(-1, X_test.shape[-1])
                
                # Fit scaler trên training data
                X_train_scaled_reshaped = self.lstm_scaler.fit_transform(X_train_reshaped)
                X_test_scaled_reshaped = self.lstm_scaler.transform(X_test_reshaped)
                
                # Reshape lại về shape ban đầu
                X_train_scaled = X_train_scaled_reshaped.reshape(X_train.shape)
                X_test_scaled = X_test_scaled_reshaped.reshape(X_test.shape)
                
                # Scale target values
                y_train_reshaped = y_train.reshape(-1, y_train.shape[-1])
                y_test_reshaped = y_test.reshape(-1, y_test.shape[-1])
                
                y_train_scaled_reshaped = self.target_scaler.fit_transform(y_train_reshaped)
                y_test_scaled_reshaped = self.target_scaler.transform(y_test_reshaped)
                
                y_train_scaled = y_train_scaled_reshaped.reshape(y_train.shape)
                y_test_scaled = y_test_scaled_reshaped.reshape(y_test.shape)
                
                self.logger.info("Data scaling completed successfully")
                
            except Exception as scaling_error:
                self.logger.error(f"Lỗi trong scaling: {str(scaling_error)}")
                return {"error": f"Lỗi scaling: {str(scaling_error)}"}
            
            # Build model
            try:
                # Get the actual output size from the target data
                output_size = y_train.shape[-1] if len(y_train.shape) > 1 else 1
                model = self.build_lstm_model((X_train.shape[1], X_train.shape[2]), output_size, symbol=symbol, characteristics=characteristics)
                self.logger.info(f"Model built successfully with output_size: {output_size}")
            except Exception as model_error:
                self.logger.error(f"Lỗi trong model building: {str(model_error)}")
                return {"error": f"Lỗi model building: {str(model_error)}"}
            
            # Callbacks với patience cao hơn để tối ưu R²
            early_stopping = EarlyStopping(
                monitor='val_loss', 
                patience=20,  # Tăng patience để model có thời gian tối ưu
                restore_best_weights=True,
                min_delta=1e-5
            )
            
            # Reduce learning rate callback với patience cao hơn
            reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=10,  # Tăng patience
                min_lr=1e-7,  # Giảm min_lr
                verbose=1
            )
            
            # Thêm callback để monitor R²
            class R2Callback(tf.keras.callbacks.Callback):
                def __init__(self, validation_data):
                    super().__init__()
                    self.validation_data = validation_data
                    self.best_r2 = -float('inf')
                
                def on_epoch_end(self, epoch, logs=None):
                    # Tính R² cho validation data
                    X_val, y_val = self.validation_data
                    y_pred = self.model.predict(X_val, verbose=0)
                    
                    # Inverse transform nếu cần
                    if hasattr(self.model, 'target_scaler'):
                        y_pred_reshaped = y_pred.reshape(-1, y_pred.shape[-1])
                        y_pred_inverse = self.model.target_scaler.inverse_transform(y_pred_reshaped)
                        y_pred = y_pred_inverse.reshape(y_pred.shape)
                        
                        y_val_reshaped = y_val.reshape(-1, y_val.shape[-1])
                        y_val_inverse = self.model.target_scaler.inverse_transform(y_val_reshaped)
                        y_val_actual = y_val_inverse.reshape(y_val.shape)
                    else:
                        y_val_actual = y_val
                    
                    # Tính R²
                    y_val_flat = y_val_actual.flatten()
                    y_pred_flat = y_pred.flatten()
                    
                    min_length = min(len(y_val_flat), len(y_pred_flat))
                    y_val_flat = y_val_flat[:min_length]
                    y_pred_flat = y_pred_flat[:min_length]
                    
                    r2 = r2_score(y_val_flat, y_pred_flat)
                    
                    if r2 > self.best_r2:
                        self.best_r2 = r2
                    
                    logs['val_r2'] = r2
                    logs['best_r2'] = self.best_r2
                    
                    if epoch % 10 == 0:
                        self.logger.info(f"Epoch {epoch}: R² = {r2:.4f}, Best R² = {self.best_r2:.4f}")
            
            # Training
            try:
                self.logger.info(f"Starting training with epochs: {adaptive_epochs}, batch_size: {adaptive_batch_size}")
                
                # Đảm bảo batch_size không lớn hơn số lượng samples
                actual_batch_size = min(adaptive_batch_size, len(X_train_scaled))
                
                # Tạo R² callback
                r2_callback = R2Callback((X_test_scaled, y_test_scaled))
                r2_callback.logger = self.logger
                
                history = model.fit(
                    X_train_scaled, y_train_scaled,
                    validation_data=(X_test_scaled, y_test_scaled),
                    epochs=adaptive_epochs,
                    batch_size=actual_batch_size,
                    callbacks=[early_stopping, reduce_lr, r2_callback],
                    verbose=1
                )
                self.logger.info("Training completed successfully")
            except Exception as training_error:
                self.logger.error(f"Lỗi trong training: {str(training_error)}")
                return {"error": f"Lỗi training: {str(training_error)}"}
            
            # Evaluation với inverse transform
            try:
                # Predict
                y_pred_scaled = model.predict(X_test_scaled, batch_size=1, verbose=0)
                
                # Inverse transform predictions
                y_pred_reshaped = y_pred_scaled.reshape(-1, y_pred_scaled.shape[-1])
                y_pred_inverse = self.target_scaler.inverse_transform(y_pred_reshaped)
                y_pred = y_pred_inverse.reshape(y_pred_scaled.shape)
                
                # Inverse transform actual values
                y_test_reshaped = y_test_scaled.reshape(-1, y_test_scaled.shape[-1])
                y_test_inverse = self.target_scaler.inverse_transform(y_test_reshaped)
                y_test_actual = y_test_inverse.reshape(y_test_scaled.shape)
                
                # Flatten for evaluation - ensure same shape
                y_test_flat = y_test_actual.flatten()
                y_pred_flat = y_pred.flatten()
                
                # Ensure both arrays have the same length
                min_length = min(len(y_test_flat), len(y_pred_flat))
                y_test_flat = y_test_flat[:min_length]
                y_pred_flat = y_pred_flat[:min_length]
                
                # Calculate metrics
                mse = mean_squared_error(y_test_flat, y_pred_flat)
                mae = mean_absolute_error(y_test_flat, y_pred_flat)
                r2 = r2_score(y_test_flat, y_pred_flat)
                
                self.logger.info(f"Evaluation - MSE: {mse:.4f}, MAE: {mae:.4f}, R²: {r2:.4f}")
                
                # Kiểm tra chất lượng metrics
                if mse > 1e8 or r2 < -10:
                    self.logger.warning("Model performance is poor, consider retraining with different parameters")
                
            except Exception as eval_error:
                self.logger.error(f"Lỗi trong evaluation: {str(eval_error)}")
                return {"error": f"Lỗi evaluation: {str(eval_error)}"}
            
            # Save model without compilation to avoid metrics compatibility issues
            model_path = os.path.join(self.model_save_path, f"lstm_{symbol}.h5")
            # Save model architecture and weights without compilation
            model.save(model_path, include_optimizer=False)
            
            # Save scalers
            scaler_path = os.path.join(self.model_save_path, f"lstm_scaler_{symbol}.pkl")
            target_scaler_path = os.path.join(self.model_save_path, f"lstm_target_scaler_{symbol}.pkl")
            
            joblib.dump(self.lstm_scaler, scaler_path)
            joblib.dump(self.target_scaler, target_scaler_path)
            
            self.models[f"lstm_{symbol}"] = {
                'model': model,
                'scaler': self.lstm_scaler,
                'target_scaler': self.target_scaler,
                'lookback': adaptive_lookback,
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
                'target_scaler_path': target_scaler_path,
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
            
            self.logger.info(f"Ensemble - Original data shape: {df.shape}")
            
            # Reset index để tránh duplicate labels
            df = df.reset_index(drop=True)
            
            self.logger.info(f"Ensemble - After reset index: {df.shape}")
            
            for col in available_cols:
                for lag in [1, 2, 3, 5, 10]:
                    df[f'{col}_lag_{lag}'] = df[col].shift(lag)
            
            # Tạo target (giá ngày mai)
            df['target'] = df['Close'].shift(-1)
            
            # Drop NaN
            df = df.dropna()
            
            self.logger.info(f"Ensemble - After dropna: {df.shape}")
            
            # Reset index sau khi dropna
            df = df.reset_index(drop=True)
            
            self.logger.info(f"Ensemble - Final shape: {df.shape}")
            
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
                    scaler_path = os.path.join(self.model_save_path, f"lstm_scaler_{symbol}.pkl")
                    target_scaler_path = os.path.join(self.model_save_path, f"lstm_target_scaler_{symbol}.pkl")
                    
                    if not os.path.exists(model_path):
                        return {"error": f"Model {model_key} chưa được training"}
                    
                    # Load model safely with compatibility handling
                    try:
                        model = self.load_model_safely(model_path)
                    except Exception as load_error:
                        self.logger.error(f"Failed to load model: {load_error}")
                        return {"error": f"Không thể load model: {str(load_error)}"}
                    # Load scalers with error handling
                    try:
                        scaler = joblib.load(scaler_path)
                        target_scaler = joblib.load(target_scaler_path)
                    except Exception as scaler_error:
                        self.logger.error(f"Failed to load scalers: {scaler_error}")
                        return {"error": f"Không thể load scalers: {str(scaler_error)}"}
                    
                    # Chuẩn bị dữ liệu cho prediction
                    lookback = 60  # Default
                    X, _ = self.prepare_data(data, lookback=lookback, prediction_horizon=1, symbol=symbol)
                    
                    if len(X) == 0:
                        return {"error": "Không đủ dữ liệu để dự báo"}
                    
                    # Scale data cho prediction (giống như training)
                    X_reshaped = X[-1].reshape(-1, X.shape[-1])
                    X_scaled_reshaped = scaler.transform(X_reshaped)
                    X_scaled = X_scaled_reshaped.reshape(1, X.shape[1], X.shape[2])
                    
                    # Scale target for prediction
                    y_reshaped = np.array([[data['Close'].iloc[-1]]]) # Assuming current price is the target for prediction
                    y_scaled_reshaped = target_scaler.transform(y_reshaped)
                    y_scaled = y_scaled_reshaped.reshape(1, 1) # Reshape to (1, 1) for LSTM output
                    
                    prediction = model.predict(X_scaled)
                    prediction_inverse = target_scaler.inverse_transform(prediction)
                    prediction_value = prediction_inverse[0][0]
                
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
                    
                    # Reset index để tránh duplicate labels
                    df = df.reset_index(drop=True)
                    
                    for col in available_cols:
                        for lag in [1, 2, 3, 5, 10]:
                            df[f'{col}_lag_{lag}'] = df[col].shift(lag)
                    
                    df = df.dropna()
                    
                    # Reset index sau khi dropna
                    df = df.reset_index(drop=True)
                    
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
            if model_type == 'lstm':
                model_path = os.path.join(self.model_save_path, f"lstm_{symbol}.h5")
                scaler_path = os.path.join(self.model_save_path, f"lstm_scaler_{symbol}.pkl")
                target_scaler_path = os.path.join(self.model_save_path, f"lstm_target_scaler_{symbol}.pkl")
            else:  # ensemble
                model_path = os.path.join(self.model_save_path, f"ensemble_{symbol}.pkl")
                scaler_path = os.path.join(self.model_save_path, f"ensemble_scaler_{symbol}.pkl")
            
            if os.path.exists(model_path) and os.path.exists(scaler_path) and os.path.exists(target_scaler_path):
                return {
                    'symbol': symbol,
                    'model_type': model_type,
                    'status': 'saved',
                    'file_path': model_path,
                    'scaler_path': scaler_path,
                    'target_scaler_path': target_scaler_path
                }
            else:
                return {
                    'symbol': symbol,
                    'model_type': model_type,
                    'status': 'not_found',
                    'missing_files': {
                        'model': not os.path.exists(model_path),
                        'scaler': not os.path.exists(scaler_path),
                        'target_scaler': not os.path.exists(target_scaler_path)
                    }
                }

    def analyze_stock_characteristics(self, data: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """
        Phân tích đặc điểm cổ phiếu để tự động chọn strategy phù hợp
        
        Args:
            data: Dữ liệu cổ phiếu
            symbol: Mã cổ phiếu
        
        Returns:
            Dictionary với đặc điểm và strategy
        """
        try:
            if 'Close' not in data.columns:
                return {'type': 'unknown', 'volatility': 'medium', 'strategy': 'balanced'}
            
            # Tính toán các metrics
            returns = data['Close'].pct_change().dropna()
            
            # 1. Volatility analysis
            daily_volatility = returns.std()
            annualized_volatility = daily_volatility * np.sqrt(252)
            
            # 2. Price trend analysis
            price_range = (data['Close'].max() - data['Close'].min()) / data['Close'].min()
            
            # 3. Volume analysis
            if 'Volume' in data.columns:
                volume_volatility = data['Volume'].pct_change().std()
                avg_volume = data['Volume'].mean()
            else:
                volume_volatility = 0
                avg_volume = 0
            
            # 4. Price stability
            price_stability = 1 / (1 + daily_volatility)
            
            # 5. Trend strength
            ma_short = data['Close'].rolling(window=20).mean()
            ma_long = data['Close'].rolling(window=60).mean()
            trend_strength = abs((ma_short.iloc[-1] - ma_long.iloc[-1]) / ma_long.iloc[-1])
            
            # Auto-classify stock type
            if annualized_volatility < 0.15:  # Low volatility
                stock_type = 'conservative'
                strategy = 'long_term'
            elif annualized_volatility < 0.25:  # Medium volatility
                stock_type = 'balanced'
                strategy = 'mixed'
            else:  # High volatility
                stock_type = 'aggressive'
                strategy = 'short_term'
            
            # Special cases based on symbol patterns
            if symbol.upper() in ['VNM', 'FPT', 'TCB', 'VCB']:
                stock_type = 'blue_chip'
                strategy = 'fundamental'
            elif symbol.upper() in ['ACB', 'TCB', 'VCB', 'BID', 'MBB']:
                stock_type = 'banking'
                strategy = 'technical'
            
            characteristics = {
                'symbol': symbol,
                'type': stock_type,
                'strategy': strategy,
                'volatility': annualized_volatility,
                'price_range': price_range,
                'volume_volatility': volume_volatility,
                'price_stability': price_stability,
                'trend_strength': trend_strength,
                'daily_volatility': daily_volatility
            }
            
            self.logger.info(f"Stock analysis for {symbol}: {stock_type} type, {strategy} strategy, "
                           f"volatility={annualized_volatility:.3f}, stability={price_stability:.3f}")
            
            return characteristics
            
        except Exception as e:
            self.logger.error(f"Error analyzing stock characteristics: {str(e)}")
            return {'type': 'unknown', 'volatility': 'medium', 'strategy': 'balanced'}

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