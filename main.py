from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

class BtcWalletManagement(App):
    """A Textual app to manage bitcoin wallets in terminal."""

    BINDINGS = [("d", "toggle_dark", "Toogle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header()
        yield Footer()

    def action_toogle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"

        )

if __name__ == "__main__":
    app = BtcWalletManagement()
    app.run()


