"""
Detailed Report Generator
Tạo báo cáo chi tiết cho từng mã cổ phiếu theo format dễ đọc
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List

class DetailedReportGenerator:
    """Class để tạo báo cáo chi tiết cho từng mã cổ phiếu"""
    
    def __init__(self):
        self.report_content = []
        self.timestamp = None
        self.report_file_path = None
        
    def start_report(self, timestamp: str = None):
        """Bắt đầu tạo report mới"""
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.timestamp = timestamp
        self.report_content = []
        
        # Tạo header
        header = f"""# Báo Cáo Chi Tiết Training LSTM Models
**Ngày:** {datetime.now().strftime('%d/%m/%Y')}  
**Thời gian:** {datetime.now().strftime('%H:%M:%S')}  
**Timestamp:** {timestamp}

## 📊 Kết Quả Training Chi Tiết

"""
        self.report_content.append(header)
        
        # Tạo file path
        os.makedirs("results", exist_ok=True)
        self.report_file_path = f"results/detailed_training_report_{timestamp}.md"
        print(f"📄 Detailed report will be saved to: {self.report_file_path}")
        
    def add_stock_result(self, result: Dict[str, Any]):
        """Thêm kết quả của một mã cổ phiếu vào report"""
        symbol = result.get('symbol', 'UNKNOWN')
        sector = result.get('sector', 'UNKNOWN')
        status = result.get('status', 'unknown')
        
        # Tạo entry cho mã cổ phiếu
        entry = f"### {symbol} - {sector}\n"
        
        if status == 'success':
            # Lấy thông tin performance
            mse = result.get('mse', 'N/A')
            mae = result.get('mae', 'N/A')
            r2 = result.get('r2', 'N/A')
            training_time = result.get('training_time', 0)
            data_points = result.get('data_points', 0)
            
            # Format performance metrics
            if isinstance(mse, (int, float)):
                mse_str = f"{mse:.4f}"
            else:
                mse_str = str(mse)
                
            if isinstance(mae, (int, float)):
                mae_str = f"{mae:.4f}"
            else:
                mae_str = str(mae)
                
            if isinstance(r2, (int, float)):
                r2_str = f"{r2:.4f}"
            else:
                r2_str = str(r2)
            
            entry += f"""📊 **Model Type:** LSTM
📈 **Performance:**
• MSE: {mse_str}
• MAE: {mae_str}
• R²: {r2_str}
⏱️ **Training Time:** {training_time:.2f}s
📊 **Data Points:** {data_points}
✅ **Status:** Thành công

"""
        else:
            # Trường hợp thất bại
            error = result.get('error', 'Unknown error')
            training_time = result.get('training_time', 0)
            
            entry += f"""📊 **Model Type:** LSTM
❌ **Status:** Thất bại
⏱️ **Training Time:** {training_time:.2f}s
🚨 **Error:** {error}

"""
        
        self.report_content.append(entry)
        
        # Lưu report ngay lập tức sau mỗi mã
        self._save_report()
        
    def add_summary(self, summary: Dict[str, Any]):
        """Thêm phần tổng kết vào report"""
        summary_section = f"""
---

## 📋 Tổng Kết

### Thống Kê Chung
- **Tổng số mã cổ phiếu:** {summary.get('total_symbols', 0)}
- **Training thành công:** {summary.get('successful', 0)} ({summary.get('success_rate', 0)*100:.2f}%)
- **Training thất bại:** {summary.get('failed', 0)} ({(1-summary.get('success_rate', 0))*100:.2f}%)
- **R² trung bình:** {summary.get('avg_r2', 0):.4f}
- **R² tốt nhất:** {summary.get('max_r2', 0):.4f}
- **R² tệ nhất:** {summary.get('min_r2', 0):.4f}
- **Thời gian training trung bình:** {summary.get('avg_training_time', 0):.2f}s

### Top 5 Models Hiệu Quả Nhất
"""
        
        # Thêm top performers
        top_performers = summary.get('top_performers', [])
        for i, performer in enumerate(top_performers[:5], 1):
            symbol = performer.get('symbol', 'N/A')
            sector = performer.get('sector', 'N/A')
            r2 = performer.get('r2', 0)
            mse = performer.get('mse', 0)
            
            summary_section += f"{i}. **{symbol}** ({sector}) - R²: **{r2:.4f}**, MSE: {mse:.4f}\n"
        
        summary_section += f"""
### Phân Tích Theo Ngành
"""
        
        # Thêm sector analysis
        sector_analysis = summary.get('sector_analysis', {})
        for sector, data in sector_analysis.items():
            total = data.get('total_symbols', 0)
            successful = data.get('successful', 0)
            success_rate = data.get('success_rate', 0)
            avg_r2 = data.get('avg_r2', 0)
            best_symbol = data.get('best_symbol', 'N/A')
            
            summary_section += f"- **{sector}:** {successful}/{total} thành công ({success_rate*100:.0f}%), R² TB: {avg_r2:.4f}, Tốt nhất: {best_symbol}\n"
        
        summary_section += f"""
---
*Báo cáo được tạo tự động bởi AlphaPulseBot Training System*
*File: {self.report_file_path}*
"""
        
        self.report_content.append(summary_section)
        self._save_report()
        
    def _save_report(self):
        """Lưu report vào file"""
        if self.report_file_path:
            try:
                with open(self.report_file_path, 'w', encoding='utf-8') as f:
                    f.write(''.join(self.report_content))
                print(f"💾 Report saved: {self.report_file_path}")
            except Exception as e:
                print(f"❌ Error saving report: {str(e)}")
                print(f"📁 Current directory: {os.getcwd()}")
                print(f"📄 Report path: {self.report_file_path}")
                
    def get_report_path(self) -> str:
        """Trả về đường dẫn file report"""
        return self.report_file_path
        
    def create_console_report(self, result: Dict[str, Any]) -> str:
        """Tạo report cho console output"""
        symbol = result.get('symbol', 'UNKNOWN')
        sector = result.get('sector', 'UNKNOWN')
        status = result.get('status', 'unknown')
        
        if status == 'success':
            mse = result.get('mse', 'N/A')
            mae = result.get('mae', 'N/A')
            r2 = result.get('r2', 'N/A')
            
            if isinstance(mse, (int, float)):
                mse_str = f"{mse:.4f}"
            else:
                mse_str = str(mse)
                
            if isinstance(mae, (int, float)):
                mae_str = f"{mae:.4f}"
            else:
                mae_str = str(mae)
                
            if isinstance(r2, (int, float)):
                r2_str = f"{r2:.4f}"
            else:
                r2_str = str(r2)
            
            return f"{symbol} - 📊 Model Type: LSTM\n📈 Performance:\n• MSE: {mse_str}\n• MAE: {mae_str}\n• R²: {r2_str}"
        else:
            error = result.get('error', 'Unknown error')
            return f"{symbol} - ❌ Training Failed\n🚨 Error: {error}"
