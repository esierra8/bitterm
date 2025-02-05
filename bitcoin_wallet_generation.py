from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.keys import HDKey


class BitcoinKeyCreation():
    
    def __init__(self):
        self.private_key = None

    def generate_mnemonic_and_private_key():
        # Generate a 12-word mnemonic phrase
        mnemonic = Mnemonic().generate(strength=128)
        print("Mnemonic Phrase:", mnemonic)

        # Convert mnemonic into seed
        seed = Mnemonic().to_seed(mnemonic)

        # Derive master private key
        self.private_key = HDKey.from_seed(seed, network='testnet')
        print("Private Key (WIF):", self.private_key.wif())
        print("Address:", self.private_key.address())

        return mnemonic, self.private_key


