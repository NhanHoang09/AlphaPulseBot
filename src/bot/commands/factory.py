"""
Command Factory
Factory pattern để tạo và quản lý commands
"""

from typing import Dict, Type
from .base_commands import BaseCommands
from .ai_commands import AICommands
from .prediction_commands import PredictionCommands
from .portfolio_commands import PortfolioCommands
from .assistant_commands import AssistantCommands
from .utility_commands import UtilityCommands
from .button_handlers import ButtonHandlers
from .fundamental_commands import FundamentalCommands
from .sentiment_commands import SentimentCommands
from .backtest_commands import BacktestCommands
from .advanced_commands import AdvancedCommands

class CommandFactory:
    """Factory để tạo và quản lý commands"""
    
    def __init__(self):
        self.commands: Dict[str, Type[BaseCommands]] = {
            'ai': AICommands,
            'prediction': PredictionCommands,
            'portfolio': PortfolioCommands,
            'assistant': AssistantCommands,
            'utility': UtilityCommands,
            'button': ButtonHandlers,
            'fundamental': FundamentalCommands,
            'sentiment': SentimentCommands,
            'backtest': BacktestCommands,
            'advanced': AdvancedCommands
        }
    
    def create_command(self, command_type: str, bot_instance) -> BaseCommands:
        """Create command instance"""
        if command_type not in self.commands:
            raise ValueError(f"Unknown command type: {command_type}")
        
        return self.commands[command_type](bot_instance)
    
    def get_all_commands(self, bot_instance) -> Dict[str, BaseCommands]:
        """Get all command instances"""
        return {
            command_type: self.create_command(command_type, bot_instance)
            for command_type in self.commands.keys()
        }
    
    def get_command_types(self) -> list:
        """Get all available command types"""
        return list(self.commands.keys())
