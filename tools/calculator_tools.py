from crewai.tools import tool 

class calculator():
    @tool("make a calculation")
    @staticmethod
    def calc(operation):
        """Useful to perform any mathematical calculations,
like sum, minus, multiplication, division, etc.
The input to this tool should be a mathematical
expression, a couple examples are `200*7` or `5000/2*10`
"""
        try:
            return eval(operation)
        except SyntaxError:
            return "error:not valid syntax"