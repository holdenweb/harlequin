from __future__ import annotations

from typing import Union

from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.validation import Integer
from textual.widget import Widget
from textual.widgets import Button, Checkbox, Input


class RunQueryBar(Horizontal):
    def __init__(
        self,
        *children: Widget,
        name: Union[str, None] = None,
        id: Union[str, None] = None,  # noqa
        classes: Union[str, None] = None,
        disabled: bool = False,
        max_results: int = 10_000,
    ) -> None:
        self.max_results = max_results
        super().__init__(
            *children, name=name, id=id, classes=classes, disabled=disabled
        )

    def compose(self) -> ComposeResult:
        self.transaction_button = Button(
            "Tx: Auto", id="transaction_button", classes="hidden"
        )
        self.limit_checkbox = Checkbox("Limit ", id="limit_checkbox")
        self.limit_input = Input(
            str(min(500, self.max_results)),
            id="limit_input",
            validators=Integer(
                minimum=0,
                maximum=self.max_results if self.max_results > 0 else None,
                failure_description=(
                    f"Please enter a number between 0 and {self.max_results}."
                    if self.max_results > 0
                    else "Please enter a number greater than 0."
                ),
            ),
        )
        self.run_button = Button("Run Query", id="run_query")
        yield self.transaction_button
        yield self.limit_checkbox
        yield self.limit_input
        yield self.run_button

    def on_mount(self) -> None:
        if self.app.is_headless:
            self.limit_input.cursor_blink = False

    @on(Input.Changed, "#limit_input")
    def handle_new_limit_value(self, message: Input.Changed) -> None:
        """
        check and uncheck the box for valid/invalid input
        """
        if (
            message.input.value
            and message.validation_result
            and message.validation_result.is_valid
        ):
            self.limit_checkbox.value = True
        else:
            self.limit_checkbox.value = False

    @property
    def limit_value(self) -> int | None:
        if not self.limit_checkbox.value or not self.limit_input.is_valid:
            return None
        try:
            return int(self.limit_input.value)
        except ValueError:
            return None

    def set_not_responsive(self) -> None:
        self.add_class("non-responsive")

    def set_responsive(self) -> None:
        self.remove_class("non-responsive")
