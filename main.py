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

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key press only for the specific input"""
        if event.input.id == "btc_address":
            self.check_balance()

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
        try:
            url = f"https://blockchain.info/q/addressbalance/{address}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            satoshis = int(response.text)
            return satoshis / 100_000_000
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                raise Exception(f"HTTP - 404. The public wallet: {address} was not found.")
            else:
                raise Exception(f"HTTP error: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            raise Exception(f"Connection error: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            raise Exception(f"Request timed out: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            raise Exception(f"Request failed: {req_err}")
        except ValueError as json_err:
            raise Exception(f"Invalid response: {json_err}")

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

