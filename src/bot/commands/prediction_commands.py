"""
AI Prediction Commands
Commands cho dự báo giá với AI
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base_commands import BaseCommands

# Setup logging
logging.basicConfig(level=logging.INFO)

class PredictionCommands(BaseCommands):
    """AI Prediction Commands"""
    
    async def predict_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /predict command - AI prediction"""
        if not context.args:
            await update.message.reply_text(
                "🔮 <b>AI Prediction</b>\n\n"
                "Sử dụng: <code>/predict &lt;symbol&gt; [model_type]</code>\n"
                "Ví dụ:\n"
                "• <code>/predict VNM</code> - Dự báo với LSTM\n"
                "• <code>/predict VNM ensemble</code> - Dự báo với Ensemble\n"
                "• <code>/predict AAPL lstm</code> - Dự báo cổ phiếu Mỹ",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        model_type = context.args[1].lower() if len(context.args) > 1 else 'lstm'
        
        if model_type not in ['lstm', 'ensemble']:
            await update.message.reply_text("❌ Model type phải là 'lstm' hoặc 'ensemble'")
            return
        
        await update.message.reply_text(f"🔮 Đang dự báo {symbol} với {model_type.upper()} model...")
        await self.predict_stock(update, context, symbol, model_type)
    
    async def train_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /train command - Train AI models"""
        if not context.args:
            await update.message.reply_text(
                "🤖 <b>AI Model Training</b>\n\n"
                "Sử dụng: <code>/train &lt;symbol&gt; [model_type]</code>\n"
                "Ví dụ:\n"
                "• <code>/train VNM</code> - Train LSTM cho VNM\n"
                "• <code>/train VNM ensemble</code> - Train Ensemble cho VNM\n"
                "• <code>/train AAPL lstm</code> - Train LSTM cho AAPL",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        model_type = context.args[1].lower() if len(context.args) > 1 else 'lstm'
        
        if model_type not in ['lstm', 'ensemble']:
            await update.message.reply_text("❌ Model type phải là 'lstm' hoặc 'ensemble'")
            return
        
        await update.message.reply_text(f"🤖 Đang training {model_type.upper()} model cho {symbol}...")
        await self.train_model(update, context, symbol, model_type)
    
    async def model_status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /model_status command - Check model status"""
        if not context.args:
            await update.message.reply_text(
                "📊 <b>Model Status</b>\n\n"
                "Sử dụng: <code>/model_status &lt;symbol&gt; [model_type]</code>\n"
                "Ví dụ:\n"
                "• <code>/model_status VNM</code> - Kiểm tra tất cả models\n"
                "• <code>/model_status VNM lstm</code> - Kiểm tra LSTM model",
                parse_mode=ParseMode.HTML
            )
            return
        
        symbol = context.args[0].upper()
        model_type = context.args[1].lower() if len(context.args) > 1 else 'all'
        
        await update.message.reply_text(f"📊 Đang kiểm tra model status cho {symbol}...")
        await self.check_model_status(update, context, symbol, model_type)
    
    async def predict_stock(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str, model_type: str = 'lstm'):
        """Predict stock price using AI models"""
        try:
            # Get data based on market
            if symbol.endswith('.VN') or len(symbol) <= 3:  # VN market
                data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period="6mo")
            else:  # US market
                data = self.us_collector.get_stock_data(symbol, period="6mo")
            
            if data.empty:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            # Get prediction
            prediction = self.predictor.predict(data, symbol, model_type)
            
            if 'error' in prediction:
                await update.message.reply_text(f"❌ Lỗi dự báo: {prediction['error']}")
                return
            
            # Format prediction message
            current_price = prediction['current_price']
            predicted_price = prediction['predicted_price']
            change_percent = ((predicted_price - current_price) / current_price) * 100
            
            message = f"""
🔮 <b>AI Prediction - {symbol}</b>

💰 <b>Giá hiện tại:</b> {current_price:,.2f}
🎯 <b>Giá dự báo:</b> {predicted_price:,.2f}
📈 <b>Thay đổi:</b> {change_percent:+.2f}%

🤖 <b>Model:</b> {prediction['model_type'].upper()}
📊 <b>Độ tin cậy:</b> {prediction['confidence']:.1%}
📅 <b>Ngày dự báo:</b> {prediction['prediction_date'].strftime('%Y-%m-%d %H:%M')}

💡 <b>Khuyến nghị:</b> {'🟢 MUA' if change_percent > 2 else '🔴 BÁN' if change_percent < -2 else '🟡 GIỮ'}
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi dự báo {symbol}: {str(e)}")
    
    async def train_model(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str, model_type: str = 'lstm'):
        """Train AI model for a symbol"""
        try:
            logging.info(f"Starting training for {symbol} with {model_type} model")
            
            # Get data based on market
            if symbol.endswith('.VN') or len(symbol) <= 3:  # VN market
                logging.info(f"Using VN collector for {symbol}")
                data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period="2y")
                logging.info(f"VN collector result: {data.shape if not data.empty else 'Empty'}")
            else:  # US market
                logging.info(f"Using US collector for {symbol}")
                data = self.us_collector.get_stock_data(symbol, period="2y")
                logging.info(f"US collector result: {data.shape if not data.empty else 'Empty'}")
            
            logging.info(f"Data collected for {symbol}: {data.shape}")
            
            if data.empty:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            # Add technical indicators
            data_with_indicators = self.analyzer.add_all_indicators(data)
            logging.info(f"Technical indicators added: {data_with_indicators.shape}")
            
            # Train model
            if model_type == 'lstm':
                logging.info(f"Training LSTM model for {symbol}")
                result = self.predictor.train_lstm_model(data_with_indicators, symbol, 
                                                       lookback=30, epochs=100, batch_size=16)  # Cải thiện cho R²
            else:  # ensemble
                logging.info(f"Training Ensemble model for {symbol}")
                result = self.predictor.train_ensemble_model(data_with_indicators, symbol)
            
            logging.info(f"Training result: {result}")
            
            if 'error' in result:
                await update.message.reply_text(f"❌ Lỗi training: {result['error']}")
                return
            
            # Format training result message
            if model_type == 'lstm':
                # Escape special characters in file path
                model_path = result.get('model_path', 'N/A')
                if model_path != 'N/A':
                    model_path = model_path.replace('_', '\\_').replace('-', '\\-').replace('.', '\\.')
                
                message = f"""
🤖 <b>LSTM Model Training Complete - {symbol}</b>

✅ <b>Status:</b> Training thành công
📊 <b>Model Type:</b> LSTM
📈 <b>Performance:</b>
&#8226; MSE: {result.get('mse', 'N/A'):.4f}
&#8226; MAE: {result.get('mae', 'N/A'):.4f}
&#8226; R²: {result.get('r2', 'N/A'):.4f}

💾 <b>Model saved:</b> <code>{model_path}</code>
"""
            else:
                # Escape special characters in file path
                model_path = result.get('model_path', 'N/A')
                if model_path != 'N/A':
                    model_path = model_path.replace('_', '\\_').replace('-', '\\-').replace('.', '\\.')
                
                message = f"""
🤖 <b>Ensemble Model Training Complete - {symbol}</b>

✅ <b>Status:</b> Training thành công
📊 <b>Model Type:</b> Ensemble
🏆 <b>Best Model:</b> {result.get('best_model', 'N/A')}

📈 <b>Performance:</b>
"""
                for model_name, metrics in result.get('results', {}).items():
                    message += f"&#8226; {model_name}: MSE={metrics.get('mse', 'N/A'):.4f}\n"
                
                message += f"\n💾 <b>Model saved:</b> <code>{model_path}</code>"
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi training model cho {symbol}: {str(e)}")
    
    async def check_model_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str, model_type: str = 'all'):
        """Check model status for a symbol"""
        try:
            if model_type == 'all':
                # Check both models
                lstm_status = self.predictor.get_model_performance(symbol, 'lstm')
                ensemble_status = self.predictor.get_model_performance(symbol, 'ensemble')
                
                # Get file paths
                lstm_file = lstm_status.get('file_path', 'Not found')
                ensemble_file = ensemble_status.get('file_path', 'Not found')
                
                message = f"""
📊 <b>Model Status - {symbol}</b>

🤖 <b>LSTM Model:</b>
&#8226; Status: {lstm_status.get('status', 'Unknown')}
&#8226; File: <code>{lstm_file}</code>

🏆 <b>Ensemble Model:</b>
&#8226; Status: {ensemble_status.get('status', 'Unknown')}
&#8226; File: <code>{ensemble_file}</code>

💡 <b>Commands:</b>
&#8226; <code>/train {symbol} lstm</code> - Train LSTM
&#8226; <code>/train {symbol} ensemble</code> - Train Ensemble
&#8226; <code>/predict {symbol} lstm</code> - Predict with LSTM
&#8226; <code>/predict {symbol} ensemble</code> - Predict with Ensemble
"""
            else:
                # Check specific model
                status = self.predictor.get_model_performance(symbol, model_type)
                
                # Get file path
                file_path = status.get('file_path', 'Not found')
                
                message = f"""
📊 <b>Model Status - {symbol} ({model_type.upper()})</b>

&#8226; <b>Status:</b> {status.get('status', 'Unknown')}
&#8226; <b>File:</b> <code>{file_path}</code>
&#8226; <b>Loaded at:</b> {status.get('loaded_at', 'N/A')}

💡 <b>Commands:</b>
&#8226; <code>/train {symbol} {model_type}</code> - Train model
&#8226; <code>/predict {symbol} {model_type}</code> - Predict
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi kiểm tra model status: {str(e)}")
