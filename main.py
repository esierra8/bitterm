import requests
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Footer, Header, Input, Button, Static

class BtcWalletManagement(App):
    """A Textual app to manage bitcoin wallets in terminal."""

    CSS_PATH = "style.tcss"
    BINDINGS = [("d", "toggle_dark", "Toogle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header()
        yield Container(
            Input(placeholder="Enter Bitcoin Public Address", id="btc_address"),
            Button("View Balance", id="check_balance"),
            Static("balance will be displayed here.", id="balance_display"),
        )
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Bitcoin Door"
        self.sub_title = "Open to the Bitcoin Network and real understanding."

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "check_balance":
            self.check_balance()

    def check_balance(self) -> None:
        """Fetch and display the balance of the Bitcoin address."""
        address_input = self.query_one("#btc_address", Input)
        address = address_input.value.strip()

        # TODO: Validate Bitcoin address to match all bitcoin addresses.
        if not address:
            self.update_balance_display("Please enter a valid Bitcoin address.")
            return
        try:
            balance = self.get_btc_balance(address)
            self.update_balance_display(f"Balance: {balance} BTC")
        except Exception as e:
            self.update_balance_display(f"Error: {str(e)}")
        
    def get_btc_balance(self, address: str) -> float:
        """Feth the balance of a Bitcoin address using the blockchain.info API."""
        url = f"https://blockchain.info/q/addressbalance/{address}"
        response = requests.get(url)
        response.raise_for_status()
        satoshis = int(response.text)
        return satoshis / 100_000_000

    def update_balance_display(self, message: str) -> None:
        """Update the balance display widget."""
        balance_display = self.query_one("#balance_display", Static)
        balance_display.update(message)


    def action_toogle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"

        )

if __name__ == "__main__":
    app = BtcWalletManagement()
    app.run()

