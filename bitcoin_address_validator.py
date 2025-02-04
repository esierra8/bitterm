import hashlib

class BitcoinAddressValidator:
    """
    A simple validator for legacy Bitcoin public addresses (Base58Check encoded).
    It validates that an address:
      - Consists only of valid Base58 characters.
      - Decodes to 25 bytes (1 version byte, 20-byte hash, 4-byte checksum).
      - Has a correct checksum.
      - Uses an allowed version byte (0x00 for P2PKH and 0x05 for P2SH on mainnet).
    """

    BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    @staticmethod
    def base58_decode(s: str) -> bytes:
        """Decodes a Base58 encoded string into bytes."""
        num = 0
        for char in s:
            if char not in BitcoinAddressValidator.BASE58_ALPHABET:
                raise ValueError(f"Invalid character {char} in Base58 string")
            num = num * 58 + BitcoinAddressValidator.BASE58_ALPHABET.index(char)
        
        # Convert the integer to bytes.
        # Determine how many bytes are needed.
        num_bytes = (num.bit_length() + 7) // 8
        decoded = num.to_bytes(num_bytes, byteorder='big') if num_bytes > 0 else b''
        
        # Add back leading zero bytes (represented as '1' in Base58)
        n_pad = len(s) - len(s.lstrip('1'))
        return b'\x00' * n_pad + decoded

    @classmethod
    def is_valid(cls, address: str) -> bool:
        """
        Validates a legacy Bitcoin address.
        
        Parameters:
            address (str): The Bitcoin address to validate.
        
        Returns:
            bool: True if the address is valid, False otherwise.
        """
        # Basic type check.
        if not isinstance(address, str):
            return False
        
        # Check that all characters are in the Base58 alphabet.
        if any(char not in cls.BASE58_ALPHABET for char in address):
            return False
        
        try:
            decoded = cls.base58_decode(address)
        except ValueError:
            return False
        
        # A valid legacy address should be exactly 25 bytes.
        if len(decoded) != 25:
            return False
        
        # Extract the components: version, hash160, and checksum.
        version = decoded[0]
        hash160 = decoded[1:-4]
        checksum = decoded[-4:]
        vh160 = decoded[:-4]
        
        # Compute the checksum by performing a double SHA-256.
        computed_checksum = hashlib.sha256(hashlib.sha256(vh160).digest()).digest()[:4]
        if checksum != computed_checksum:
            return False
        
        # Check the version byte.
        # For Bitcoin mainnet legacy addresses, allowed versions are:
        #   0x00: P2PKH addresses (usually start with '1')
        #   0x05: P2SH addresses (usually start with '3')
        if version not in (0, 5):
            return False
        
        return True

# Example usage:
if __name__ == "__main__":
    valid_addresses = [
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",  # The famous Genesis address (P2PKH)
        "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",  # A typical P2SH address
    ]
    invalid_addresses = [
        "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNb",  # Likely a typo in checksum
        "4J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",  # Invalid version character (starts with '4')
        "NotARealAddress123",
    ]
    
    for addr in valid_addresses:
        print(f"Address {addr} is valid: {BitcoinAddressValidator.is_valid(addr)}")
    
    for addr in invalid_addresses:
        print(f"Address {addr} is valid: {BitcoinAddressValidator.is_valid(addr)}")

