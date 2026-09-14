from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.metrics import dp
import ast
import operator

Window.clearcolor = (0.96, 0.96, 0.96, 1)


class SafeCalculator:
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def calculate(self, expression):
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")

        tree = ast.parse(expression, mode="eval")
        return self._evaluate(tree.body)

    def _evaluate(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError()

        if isinstance(node, ast.BinOp):
            operation = self.operators.get(type(node.op))
            if operation is None:
                raise ValueError()
            return operation(
                self._evaluate(node.left),
                self._evaluate(node.right)
            )

        if isinstance(node, ast.UnaryOp):
            operation = self.operators.get(type(node.op))
            if operation is None:
                raise ValueError()
            return operation(self._evaluate(node.operand))

        raise ValueError()


class CalculatorApp(App):

    def build(self):
        self.title = "Calculator"

        root = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10)
        )

        self.display = TextInput(
            text="",
            readonly=True,
            multiline=False,
            halign="right",
            font_size=dp(34),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.1, 0.1, 0.1, 1),
            cursor_color=(0.2, 0.2, 0.2, 1),
            padding=[dp(10), dp(18)]
        )

        root.add_widget(self.display)

        buttons = GridLayout(
            cols=4,
            spacing=dp(8),
            size_hint_y=0.72
        )

        keys = [
            "C", "⌫", "%", "÷",
            "7", "8", "9", "×",
            "4", "5", "6", "-",
            "1", "2", "3", "+",
            "0", ".", "(", ")",
            "="
        ]

        for key in keys:
            button = Button(
                text=key,
                font_size=dp(24),
                background_normal="",
                background_color=(1, 1, 1, 1),
                color=(0.1, 0.1, 0.1, 1)
            )

            button.bind(on_press=self.button_pressed)
            buttons.add_widget(button)

        root.add_widget(buttons)

        return root

    def button_pressed(self, instance):
        value = instance.text

        if value == "C":
            self.display.text = ""

        elif value == "⌫":
            self.display.text = self.display.text[:-1]

        elif value == "=":
            self.calculate()

        else:
            self.display.text += value

    def calculate(self):
        expression = self.display.text

        if not expression:
            return

        try:
            result = SafeCalculator().calculate(expression)

            if isinstance(result, float) and result.is_integer():
                result = int(result)

            self.display.text = str(result)

        except ZeroDivisionError:
            self.display.text = "Cannot divide by zero"

        except Exception:
            self.display.text = "Error"


if __name__ == "__main__":
    CalculatorApp().run()
