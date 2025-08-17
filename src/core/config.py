"""
Configuration Manager
Quản lý cấu hình cho trading bot
"""

import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import time

class ConfigManager:
    """Configuration manager cho trading bot"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        load_dotenv()  # Load environment variables
        
        # Default configuration
        self.default_config = {
            "bot": {
                "name": "AlphaPulse Trading Bot",
                "version": "2.0.0",
                "debug": False
            },
            "trading": {
                "default_period": "6mo",
                "default_market": "US",
                "risk_thresholds": {
                    "high_volatility": 0.3,
                    "max_drawdown": -0.2,
                    "min_sharpe": 0.5
                }
            },
            "markets": {
                "vn": {
                    "name": "Vietnam",
                    "trading_hours": {
                        "open": "09:00",
                        "close": "15:00"
                    },
                    "timezone": "Asia/Ho_Chi_Minh"
                },
                "us": {
                    "name": "United States",
                    "trading_hours": {
                        "open": "09:30",
                        "close": "16:00"
                    },
                    "timezone": "America/New_York"
                }
            },
            "ai": {
                "gpt_model": "gpt_assistant:latest",
                "claude_model": "claude-3-sonnet-20240229",
                "max_tokens": 1000
            },
            "analysis": {
                "technical_indicators": [
                    "RSI", "MACD", "Bollinger_Bands", "Moving_Averages",
                    "Stochastic", "Williams_R", "ATR", "Volume"
                ],
                "fundamental_ratios": [
                    "P/E", "P/B", "P/S", "ROE", "ROA", "Debt_to_Equity",
                    "Current_Ratio", "Quick_Ratio", "Profit_Margin"
                ]
            },
            "commands": {
                "priority": [
                    "quick", "stock", "risk",
                    "fundamental", "technical", "sentiment",
                    "portfolio", "backtest", "ai"
                ],
                "aliases": {
                    "scan": "quick",
                    "check": "stock",
                    "analyze": "stock"
                }
            }
        }
        
        # Load configuration
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Merge with default config
                return self._merge_configs(self.default_config, config)
            else:
                # Create default config file
                self._save_config(self.default_config)
                return self.default_config
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.default_config
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def _merge_configs(self, default: Dict, custom: Dict) -> Dict:
        """Merge custom config with default config"""
        result = default.copy()
        for key, value in custom.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (dot notation supported)"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value by key (dot notation supported)"""
        keys = key.split('.')
        config = self.config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        
        # Save to file
        self._save_config(self.config)
    
    def get_env(self, key: str, default: Any = None) -> Any:
        """Get environment variable"""
        return os.getenv(key, default)
    
    def get_trading_config(self) -> Dict[str, Any]:
        """Get trading configuration"""
        return self.get('trading', {})
    
    def get_market_config(self, market: str) -> Dict[str, Any]:
        """Get market configuration"""
        return self.get(f'markets.{market}', {})
    
    def get_ai_config(self) -> Dict[str, Any]:
        """Get AI configuration"""
        return self.get('ai', {})
    
    def get_commands_config(self) -> Dict[str, Any]:
        """Get commands configuration"""
        return self.get('commands', {})
    
    def get_command_priority(self) -> list:
        """Get command priority list"""
        return self.get('commands.priority', [])
    
    def get_command_aliases(self) -> Dict[str, str]:
        """Get command aliases"""
        return self.get('commands.aliases', {})
    
    def reload(self):
        """Reload configuration from file"""
        self.config = self._load_config()
    
    def export(self, filename: str = None):
        """Export configuration to file"""
        if not filename:
            filename = f"config_export_{int(time.time())}.json"
        
        self._save_config(self.config)
        return filename
