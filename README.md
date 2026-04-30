# AutoLotto — Blockchain-Based Decentralized Lottery System

> **Network:** Ethereum Sepolia Testnet  
> **Author:** Kubra Banu

---

## Overview

AutoLotto is a decentralized lottery system built on Ethereum using Solidity smart contracts. It replaces centralized lottery management with transparent, automated, on-chain execution — no intermediaries, no manual prize distribution, fully auditable on Etherscan.

Users enter by sending ETH to the contract. A pseudo-random winner is selected from all participants, the prize pool is automatically transferred to the winner's wallet, and the lottery resets for the next round.

---

## Live Deployment

| Detail | Value |
|--------|-------|
| Network | Ethereum Sepolia Testnet |
| Contract Address | `0x7Cf12187dE99aBa948Dcb9260Dc9D817925ba16E` |
| Owner Wallet | `0x5F9b18F59B772055834822d015D45fDdb741ddB0` |
| Entry Fee | 0.01 ETH |
| Etherscan | [View on Sepolia Etherscan](https://sepolia.etherscan.io/address/0x7Cf12187dE99aBa948Dcb9260Dc9D817925ba16E) |

---

## Features

- Decentralized participation — no central authority
- On-chain participant storage
- Automated ETH prize distribution via smart contract
- Public transaction verification through Etherscan
- Lottery auto-resets after each round
- Owner-restricted winner selection

---

## Repository Structure

```
AutoLotto/
├── AutoLoto.sol              # Main Solidity smart contract
├── interact.py               # Python (Web3.py) interaction script
├── requirements.txt          # Python dependencies
├── hardhat.config.js         # Hardhat configuration (optional local testing)
├── package.json              # Node.js dependencies for Hardhat
├── .env.example              # Environment variable template
├── deployment/
│   └── deploy-instructions.md  # Step-by-step deployment guide
├── tests/
│   └── test_autolotto.py     # Python test suite
└── README.md                 # This file
```

---

## Quick Start

### Option A — Remix IDE (Easiest, No Setup Required)

See [`deployment/deploy-instructions.md`](deployment/deploy-instructions.md) for a full step-by-step guide.

1. Open [Remix IDE](https://remix.ethereum.org)
2. Upload `AutoLoto.sol`
3. Compile with Solidity `^0.8.0`
4. Connect MetaMask → Sepolia Testnet
5. Deploy and interact

### Option B — Python Interaction (Web3.py)

```bash
# 1. Clone the repo
git clone https://github.com/KubraBanu/Autolotto.git
cd Autolotto

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env with your private key and RPC URL

# 4. Run the interaction script
python interact.py
```

### Option C — Local Testing with Hardhat

```bash
# Install Node.js dependencies
npm install

# Run local tests
npx hardhat test

# Deploy to Sepolia
npx hardhat run scripts/deploy.js --network sepolia
```

---

## Smart Contract Functions

| Function | Access | Description |
|----------|--------|-------------|
| `enterLottery()` | Public (payable) | Enter by sending >= 0.01 ETH |
| `getPlayers()` | Public (view) | Returns all current participant addresses |
| `pickWinner()` | Owner only | Selects winner, transfers prize, resets lottery |
| `random()` | Private (view) | Generates pseudo-random index for winner selection |

---

## Security Notes

- Winner selection uses pseudo-randomness from `block.timestamp`, `block.prevrandao`, and player addresses
- This is suitable for educational/testnet use — for production, integrate [Chainlink VRF](https://docs.chain.link/vrf) for verifiable randomness
- `pickWinner()` is restricted to contract owner to prevent unauthorized draws
- All transactions are publicly auditable on Etherscan

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Smart Contract | Solidity `^0.8.0` |
| Blockchain | Ethereum Sepolia Testnet |
| Development IDE | Remix IDE |
| Wallet | MetaMask |
| Blockchain Explorer | Etherscan (Sepolia) |
| Python Interaction | Web3.py |
| Local Testing | Hardhat (optional) |
| Version Control | GitHub |

---

## Testing Results

All core functions were tested successfully on Sepolia Testnet:

- [x] Smart contract compilation
- [x] Contract deployment on Sepolia
- [x] MetaMask wallet integration
- [x] `enterLottery()` — 0.01 ETH entry executed
- [x] `getPlayers()` — participant addresses returned correctly
- [x] `pickWinner()` — winner selected, prize transferred, lottery reset
- [x] Transactions verified on Etherscan

---

## References

- Buterin, V. (2014). [Ethereum White Paper](https://ethereum.org/en/whitepaper/)
- Chainlink Labs. (2020). [Chainlink VRF](https://blog.chain.link/chainlink-vrf-on-chain-verifiable-randomness/)
- Dixit et al. (2022). Blockchain based secure lottery platform. IEEE CICT 2022.
- [Ethereum Documentation](https://ethereum.org)
- [Solidity Documentation](https://docs.soliditylang.org)
- [Web3.py Documentation](https://web3py.readthedocs.io)

---

## License

MIT License — see [LICENSE](LICENSE) for details.
