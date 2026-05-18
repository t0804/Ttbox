from core.plugin import BasePlugin

class CalculatorPlugin(BasePlugin):
    @property
    def name(self):
        return 'calculator_plugin'
    @property
    def version(self) -> str:
        return '1.0.0'
