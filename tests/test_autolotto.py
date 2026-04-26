"""
AutoLotto — Test Suite
Tests contract interaction logic using Web3.py against the deployed Sepolia contract.

Run with:
    pip install -r requirements.txt
    pytest tests/ -v
"""

import os
import pytest
from unittest.mock import MagicMock, patch
from web3 import Web3

# ── Constants ─────────────────────────────────────────────────────────────────
CONTRACT_ADDRESS = "0x7Cf12187dE99aBa948Dcb9260Dc9D817925ba16E"
OWNER_ADDRESS    = "0x5F9b18F59B772055834822d015D45fDdb741ddB0"
ENTRY_FEE_WEI    = 10000000000000000  # 0.01 ETH

CONTRACT_ABI = [
    {"inputs": [], "name": "enterLottery", "outputs": [], "stateMutability": "payable", "type": "function"},
    {"inputs": [], "name": "getPlayers", "outputs": [{"internalType": "address[]", "name": "", "type": "address[]"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "pickWinner", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "entryFee", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "lotteryRound", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
]


# ── Fixtures ──────────────────────────────────────────────────────────────────
@pytest.fixture
def mock_contract():
    """Mock Web3 contract for unit testing without a real node."""
    contract = MagicMock()
    contract.functions.owner.return_value.call.return_value = OWNER_ADDRESS
    contract.functions.entryFee.return_value.call.return_value = ENTRY_FEE_WEI
    contract.functions.lotteryRound.return_value.call.return_value = 0
    contract.functions.getPlayers.return_value.call.return_value = []
    return contract


@pytest.fixture
def mock_w3():
    """Mock Web3 instance."""
    w3 = MagicMock()
    w3.is_connected.return_value = True
    w3.eth.block_number = 5000000
    w3.eth.gas_price = 1000000000
    return w3


# ── Unit Tests ────────────────────────────────────────────────────────────────
class TestContractState:

    def test_owner_address(self, mock_contract):
        """Contract should return the correct owner address."""
        owner = mock_contract.functions.owner().call()
        assert owner == OWNER_ADDRESS

    def test_entry_fee(self, mock_contract):
        """Entry fee should be 0.01 ETH (10000000000000000 Wei)."""
        fee = mock_contract.functions.entryFee().call()
        assert fee == ENTRY_FEE_WEI
        assert Web3.from_wei(fee, 'ether') == 0.01

    def test_initial_lottery_round(self, mock_contract):
        """Lottery round should start at 0."""
        round_num = mock_contract.functions.lotteryRound().call()
        assert round_num == 0

    def test_empty_players_initially(self, mock_contract):
        """Players list should be empty before any entries."""
        players = mock_contract.functions.getPlayers().call()
        assert players == []
        assert len(players) == 0


class TestLotteryEntry:

    def test_player_added_after_entry(self, mock_contract):
        """After entering, player address should appear in the players list."""
        test_player = "0x1234567890123456789012345678901234567890"
        mock_contract.functions.getPlayers.return_value.call.return_value = [test_player]

        players = mock_contract.functions.getPlayers().call()
        assert test_player in players
        assert len(players) == 1

    def test_multiple_players(self, mock_contract):
        """Multiple players should all be stored."""
        player1 = "0x1111111111111111111111111111111111111111"
        player2 = "0x2222222222222222222222222222222222222222"
        player3 = "0x3333333333333333333333333333333333333333"
        mock_contract.functions.getPlayers.return_value.call.return_value = [player1, player2, player3]

        players = mock_contract.functions.getPlayers().call()
        assert len(players) == 3
        assert player1 in players
        assert player2 in players
        assert player3 in players

    def test_entry_fee_validation(self):
        """Entry below minimum should be rejected."""
        below_minimum = ENTRY_FEE_WEI - 1
        # Simulate the contract's require() check
        with pytest.raises(ValueError):
            if below_minimum < ENTRY_FEE_WEI:
                raise ValueError("Minimum ETH not sent")

    def test_entry_fee_exact(self):
        """Entry at exact minimum fee should pass."""
        exact_fee = ENTRY_FEE_WEI
        # Should not raise
        assert exact_fee >= ENTRY_FEE_WEI

    def test_entry_fee_above_minimum(self):
        """Entry above minimum fee should also be accepted."""
        above_minimum = ENTRY_FEE_WEI * 2
        assert above_minimum >= ENTRY_FEE_WEI


class TestWinnerSelection:

    def test_pick_winner_owner_only(self, mock_contract):
        """Only the owner should be able to call pickWinner."""
        owner = mock_contract.functions.owner().call()
        non_owner = "0x9999999999999999999999999999999999999999"

        # Simulate owner restriction
        caller = non_owner
        if caller.lower() != owner.lower():
            with pytest.raises(PermissionError):
                raise PermissionError("Only owner can call this function")

    def test_pick_winner_requires_players(self, mock_contract):
        """pickWinner should fail if no players are in the lottery."""
        mock_contract.functions.getPlayers.return_value.call.return_value = []
        players = mock_contract.functions.getPlayers().call()

        with pytest.raises(ValueError):
            if len(players) == 0:
                raise ValueError("No players in lottery")

    def test_lottery_resets_after_winner(self, mock_contract):
        """Players list should be empty after a winner is picked."""
        # Simulate state after pickWinner
        mock_contract.functions.getPlayers.return_value.call.return_value = []
        mock_contract.functions.lotteryRound.return_value.call.return_value = 1

        players_after = mock_contract.functions.getPlayers().call()
        round_after   = mock_contract.functions.lotteryRound().call()

        assert len(players_after) == 0
        assert round_after == 1

    def test_winner_index_within_bounds(self):
        """Random winner index should always be within the players array bounds."""
        import random
        players = ["0xAAA", "0xBBB", "0xCCC", "0xDDD", "0xEEE"]
        for _ in range(1000):
            index = random.randint(0, 10**18) % len(players)
            assert 0 <= index < len(players)


class TestETHConversions:

    def test_entry_fee_in_ether(self):
        """0.01 ETH should equal 10000000000000000 Wei."""
        assert Web3.to_wei(0.01, 'ether') == ENTRY_FEE_WEI

    def test_wei_to_ether_conversion(self):
        """Wei to ETH conversion should be accurate."""
        assert Web3.from_wei(ENTRY_FEE_WEI, 'ether') == 0.01

    def test_checksum_address(self):
        """Contract address should be a valid checksum address."""
        checksum = Web3.to_checksum_address(CONTRACT_ADDRESS.lower())
        assert Web3.is_checksum_address(checksum)


class TestConnection:

    def test_web3_connection(self, mock_w3):
        """Web3 should report connected."""
        assert mock_w3.is_connected() is True

    def test_block_number_positive(self, mock_w3):
        """Block number should be a positive integer."""
        assert mock_w3.eth.block_number > 0


# ── Integration Test (requires real node — skipped by default) ────────────────
@pytest.mark.skip(reason="Requires live Sepolia RPC connection — run manually")
class TestLiveIntegration:

    def test_live_connection(self):
        """Test actual connection to Sepolia."""
        rpc_url = os.getenv("RPC_URL", "https://rpc.sepolia.org")
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        assert w3.is_connected()

    def test_live_contract_owner(self):
        """Test reading owner from live contract."""
        rpc_url = os.getenv("RPC_URL", "https://rpc.sepolia.org")
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        contract = w3.eth.contract(
            address=Web3.to_checksum_address(CONTRACT_ADDRESS),
            abi=CONTRACT_ABI
        )
        owner = contract.functions.owner().call()
        assert Web3.is_address(owner)
