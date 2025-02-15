import requests
from bitcoin_wallet_generation import BitcoinKeyCreation 
from bitcoin_address_validator import BitcoinAddressValidator
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import Footer, Header, Input, Button, Static


class ChatMessage(Static):
    """
    A chat message widget for displaying chat bubbles.

    Attributes:
        message (str): The text content of the message.
        sender (str): The sender identifier (e.g., 'system', 'user', 'bot').
    """
    def __init__(self, message: str, sender: str = "system", **kwargs) -> None:
        # Pass the message text to the parent Static widget
        super().__init__(message, **kwargs)
        self.message = message
        self.sender = sender
        # Add CSS classes for styling; these can be defined in your style.tcss
        self.add_class("chat-bubble")
        self.add_class(sender)



class BtcWalletManagement(App):
    """A Textual app to manage bitcoin wallets in terminal."""

    CSS_PATH = "style.tcss"
    BINDINGS = [("d", "toggle_dark", "Toogle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header()
        with Vertical():
            yield VerticalScroll(id="chat_container")
            yield Button("Create private key", id="create_private_key_button")
            yield Input(placeholder="Enter Bitcoin Public Address", id="user_input")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Bitcoin Door"
        self.sub_title = "Open to the Bitcoin Network and real understanding."

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle Enter key press only for the specific input"""
        if event.input.id == "user_input":
            self.process_user_input()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "send_button":
            self.process_user_input()

        if event.button.id == "create_private_key_button":
            self.create_private_key()

    def add_message_to_chat(self, message: str, sender: str = "system") -> None:
        """Add a chat message to the chat container."""
        chat_container = self.query_one("#chat_container", VerticalScroll)
        chat_msg = ChatMessage(message, sender=sender)
        chat_container.mount(chat_msg)

    def is_bitcoin_address(self, input) -> bool:
        if not input or not BitcoinAddressValidator.is_valid(input):
            self.add_message_to_chat("Bitcoin public address is not valid.")
            return False
        try:
            balance = self.get_btc_balance(input)
            self.add_message_to_chat(f"Balance: {balance} BTC")
            return True
        except Exception as e:
            self.add_message_to_chat(f"Error: {str(e)}")
            return False
    
    def process_user_input(self) -> None:
        """Fetch and display the balance of the Bitcoin address."""
        user_input_widget = self.query_one("#user_input", Input)
        input = user_input_widget.value.strip()
        self.add_message_to_chat(str(input), sender="user")
        if not self.is_bitcoin_address(input):
            return

    def create_private_key(self) -> None:
        mnemonic, private_key = BitcoinKeyCreation().generate_mnemonic_and_private_key()
        mess = f"KEY: {private_key} - Mnemonic: {mnemonic}"
        self.add_message_to_chat(mess)
        pass
        
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

    def action_toogle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"

        )

if __name__ == "__main__":
    app = BtcWalletManagement()
    app.run()

