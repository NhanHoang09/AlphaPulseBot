"""
AI Prediction Commands
Commands cho dự báo giá với AI
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from .base_commands import BaseCommands

class PredictionCommands(BaseCommands):
    """AI Prediction Commands"""
    
    async def predict_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /predict command - AI prediction"""
        if not context.args:
            await update.message.reply_text(
                "🔮 **AI Prediction**\n\n"
                "Sử dụng: `/predict <symbol> [model_type]`\n"
                "Ví dụ:\n"
                "• `/predict VNM` - Dự báo với LSTM\n"
                "• `/predict VNM ensemble` - Dự báo với Ensemble\n"
                "• `/predict AAPL lstm` - Dự báo cổ phiếu Mỹ",
                parse_mode=ParseMode.MARKDOWN
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
                "🤖 **AI Model Training**\n\n"
                "Sử dụng: `/train <symbol> [model_type]`\n"
                "Ví dụ:\n"
                "• `/train VNM` - Train LSTM cho VNM\n"
                "• `/train VNM ensemble` - Train Ensemble cho VNM\n"
                "• `/train AAPL lstm` - Train LSTM cho AAPL",
                parse_mode=ParseMode.MARKDOWN
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
                "📊 **Model Status**\n\n"
                "Sử dụng: `/model_status <symbol> [model_type]`\n"
                "Ví dụ:\n"
                "• `/model_status VNM` - Kiểm tra tất cả models\n"
                "• `/model_status VNM lstm` - Kiểm tra LSTM model",
                parse_mode=ParseMode.MARKDOWN
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
🔮 **AI Prediction - {symbol}**

💰 **Giá hiện tại:** {current_price:,.2f}
🎯 **Giá dự báo:** {predicted_price:,.2f}
📈 **Thay đổi:** {change_percent:+.2f}%

🤖 **Model:** {prediction['model_type'].upper()}
📊 **Độ tin cậy:** {prediction['confidence']:.1%}
📅 **Ngày dự báo:** {prediction['prediction_date'].strftime('%Y-%m-%d %H:%M')}

💡 **Khuyến nghị:** {'🟢 MUA' if change_percent > 2 else '🔴 BÁN' if change_percent < -2 else '🟡 GIỮ'}
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi dự báo {symbol}: {str(e)}")
    
    async def train_model(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str, model_type: str = 'lstm'):
        """Train AI model for a symbol"""
        try:
            # Get data based on market
            if symbol.endswith('.VN') or len(symbol) <= 3:  # VN market
                data = self.vn_collector.get_vn_stock_data_yahoo(symbol, period="2y")
            else:  # US market
                data = self.us_collector.get_stock_data(symbol, period="2y")
            
            if data.empty:
                await update.message.reply_text(f"❌ Không thể lấy dữ liệu cho {symbol}")
                return
            
            # Add technical indicators
            data_with_indicators = self.analyzer.add_all_indicators(data)
            
            # Train model
            if model_type == 'lstm':
                result = self.predictor.train_lstm_model(data_with_indicators, symbol, epochs=50)  # Reduced for Telegram
            else:  # ensemble
                result = self.predictor.train_ensemble_model(data_with_indicators, symbol)
            
            if 'error' in result:
                await update.message.reply_text(f"❌ Lỗi training: {result['error']}")
                return
            
            # Format training result message
            if model_type == 'lstm':
                message = f"""
🤖 **LSTM Model Training Complete - {symbol}**

✅ **Status:** Training thành công
📊 **Model Type:** LSTM
📈 **Performance:**
• MSE: {result.get('mse', 'N/A'):.4f}
• MAE: {result.get('mae', 'N/A'):.4f}
• R²: {result.get('r2', 'N/A'):.4f}

💾 **Model saved:** {result.get('model_path', 'N/A')}
"""
            else:
                message = f"""
🤖 **Ensemble Model Training Complete - {symbol}**

✅ **Status:** Training thành công
📊 **Model Type:** Ensemble
🏆 **Best Model:** {result.get('best_model', 'N/A')}

📈 **Performance:**
"""
                for model_name, metrics in result.get('results', {}).items():
                    message += f"• {model_name}: MSE={metrics.get('mse', 'N/A'):.4f}\n"
                
                message += f"\n💾 **Model saved:** {result.get('model_path', 'N/A')}"
            
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi training model cho {symbol}: {str(e)}")
    
    async def check_model_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str, model_type: str = 'all'):
        """Check model status for a symbol"""
        try:
            if model_type == 'all':
                # Check both models
                lstm_status = self.predictor.get_model_performance(symbol, 'lstm')
                ensemble_status = self.predictor.get_model_performance(symbol, 'ensemble')
                
                message = f"""
📊 **Model Status - {symbol}**

🤖 **LSTM Model:**
• Status: {lstm_status.get('status', 'Unknown')}
• File: {lstm_status.get('file_path', 'Not found')}

🏆 **Ensemble Model:**
• Status: {ensemble_status.get('status', 'Unknown')}
• File: {ensemble_status.get('file_path', 'Not found')}

💡 **Commands:**
• `/train {symbol} lstm` - Train LSTM
• `/train {symbol} ensemble` - Train Ensemble
• `/predict {symbol} lstm` - Predict with LSTM
• `/predict {symbol} ensemble` - Predict with Ensemble
"""
            else:
                # Check specific model
                status = self.predictor.get_model_performance(symbol, model_type)
                
                message = f"""
📊 **Model Status - {symbol} ({model_type.upper()})**

• **Status:** {status.get('status', 'Unknown')}
• **File:** {status.get('file_path', 'Not found')}
• **Loaded at:** {status.get('loaded_at', 'N/A')}

💡 **Commands:**
• `/train {symbol} {model_type}` - Train model
• `/predict {symbol} {model_type}` - Predict
"""
            
            await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Lỗi khi kiểm tra model status: {str(e)}")
