"""
AutoLotto — Python Interaction Script
Uses Web3.py to interact with the deployed AutoLotto contract on Sepolia Testnet.

Setup:
    1. pip install -r requirements.txt
    2. cp .env.example .env
    3. Fill in your RPC_URL, PRIVATE_KEY, and CONTRACT_ADDRESS in .env
    4. python interact.py
"""

import os
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ── Configuration ─────────────────────────────────────────────────────────────
RPC_URL          = os.getenv("RPC_URL", "https://rpc.sepolia.org")
PRIVATE_KEY      = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "0x7Cf12187dE99aBa948Dcb9260Dc9D817925ba16E")
ENTRY_FEE_WEI    = int(os.getenv("ENTRY_FEE_WEI", "10000000000000000"))  # 0.01 ETH

# ── AutoLotto ABI ─────────────────────────────────────────────────────────────
# Minimal ABI covering all public contract functions
CONTRACT_ABI = [
    {
        "inputs": [],
        "name": "enterLottery",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getPlayers",
        "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "pickWinner",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "entryFee",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "lotteryRound",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# ── Connect to Ethereum ───────────────────────────────────────────────────────
def connect():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        raise ConnectionError(f"Could not connect to Ethereum node at {RPC_URL}")
    print(f"Connected to Sepolia Testnet | Block: {w3.eth.block_number}")
    return w3


# ── Load Contract ─────────────────────────────────────────────────────────────
def load_contract(w3):
    address = Web3.to_checksum_address(CONTRACT_ADDRESS)
    contract = w3.eth.contract(address=address, abi=CONTRACT_ABI)
    return contract


# ── Read Functions ────────────────────────────────────────────────────────────
def get_contract_info(w3, contract):
    """Print current contract state."""
    owner        = contract.functions.owner().call()
    entry_fee    = contract.functions.entryFee().call()
    lottery_round = contract.functions.lotteryRound().call()
    players      = contract.functions.getPlayers().call()
    balance_wei  = w3.eth.get_balance(Web3.to_checksum_address(CONTRACT_ADDRESS))

    print("\n── AutoLotto Contract State ──────────────────────────")
    print(f"  Contract Address : {CONTRACT_ADDRESS}")
    print(f"  Owner            : {owner}")
    print(f"  Entry Fee        : {Web3.from_wei(entry_fee, 'ether')} ETH")
    print(f"  Lottery Round    : {lottery_round}")
    print(f"  Prize Pool       : {Web3.from_wei(balance_wei, 'ether')} ETH")
    print(f"  Players ({len(players)}):")
    for i, p in enumerate(players, 1):
        print(f"    {i}. {p}")
    print("──────────────────────────────────────────────────────\n")


# ── Write Functions ───────────────────────────────────────────────────────────
def enter_lottery(w3, contract):
    """Enter the lottery by sending 0.01 ETH."""
    if not PRIVATE_KEY:
        print("ERROR: PRIVATE_KEY not set in .env file")
        return

    account = w3.eth.account.from_key(PRIVATE_KEY)
    print(f"Entering lottery from wallet: {account.address}")

    # Check balance
    balance = w3.eth.get_balance(account.address)
    if balance < ENTRY_FEE_WEI:
        print(f"ERROR: Insufficient balance. Have {Web3.from_wei(balance, 'ether')} ETH, need 0.01 ETH")
        return

    # Build transaction
    nonce = w3.eth.get_transaction_count(account.address)
    tx = contract.functions.enterLottery().build_transaction({
        'from':     account.address,
        'value':    ENTRY_FEE_WEI,
        'gas':      100000,
        'gasPrice': w3.eth.gas_price,
        'nonce':    nonce,
        'chainId':  11155111  # Sepolia chain ID
    })

    # Sign and send
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash   = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Transaction sent: {tx_hash.hex()}")
    print("Waiting for confirmation...")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    if receipt.status == 1:
        print(f"Success! Entered lottery. Gas used: {receipt.gasUsed}")
        print(f"View on Etherscan: https://sepolia.etherscan.io/tx/{tx_hash.hex()}")
    else:
        print("Transaction failed — check Etherscan for details")


def pick_winner(w3, contract):
    """Pick a winner (owner only)."""
    if not PRIVATE_KEY:
        print("ERROR: PRIVATE_KEY not set in .env file")
        return

    account = w3.eth.account.from_key(PRIVATE_KEY)
    owner   = contract.functions.owner().call()

    if account.address.lower() != owner.lower():
        print(f"ERROR: Only the owner ({owner}) can call pickWinner()")
        print(f"Your address: {account.address}")
        return

    players = contract.functions.getPlayers().call()
    if len(players) == 0:
        print("ERROR: No players in the lottery yet")
        return

    print(f"Picking winner from {len(players)} players...")

    nonce = w3.eth.get_transaction_count(account.address)
    tx = contract.functions.pickWinner().build_transaction({
        'from':     account.address,
        'gas':      200000,
        'gasPrice': w3.eth.gas_price,
        'nonce':    nonce,
        'chainId':  11155111
    })

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash   = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"Transaction sent: {tx_hash.hex()}")
    print("Waiting for confirmation...")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    if receipt.status == 1:
        print(f"Winner picked successfully! Gas used: {receipt.gasUsed}")
        print(f"View on Etherscan: https://sepolia.etherscan.io/tx/{tx_hash.hex()}")
    else:
        print("Transaction failed — check Etherscan for details")


# ── Main Menu ─────────────────────────────────────────────────────────────────
def main():
    print("=" * 54)
    print("  AutoLotto — Blockchain Lottery Interaction Script")
    print("=" * 54)

    w3       = connect()
    contract = load_contract(w3)

    while True:
        print("\nOptions:")
        print("  1. View contract info & players")
        print("  2. Enter lottery (0.01 ETH)")
        print("  3. Pick winner (owner only)")
        print("  4. Exit")
        choice = input("\nChoice: ").strip()

        if choice == "1":
            get_contract_info(w3, contract)
        elif choice == "2":
            enter_lottery(w3, contract)
        elif choice == "3":
            pick_winner(w3, contract)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
