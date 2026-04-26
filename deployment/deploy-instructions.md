# AutoLotto — Deployment Instructions

Complete step-by-step guide to deploy and interact with the AutoLotto smart contract on the Ethereum Sepolia Testnet.

---

## Prerequisites

Before you begin, make sure you have:

- A modern web browser (Chrome or Firefox recommended)
- MetaMask browser extension installed
- A basic understanding of Ethereum wallets and transactions

---

## Step 1 — Install MetaMask

1. Visit [metamask.io](https://metamask.io) and install the browser extension
2. Create a new wallet or import an existing one
3. **Securely save your seed phrase** — never share it with anyone
4. Your wallet will be created with a public address (e.g., `0x5F9b...`)

---

## Step 2 — Configure Sepolia Testnet

MetaMask may already have Sepolia configured. If not:

1. Open MetaMask → click the network dropdown (top center)
2. Click **"Add network"** → **"Add a network manually"**
3. Enter the following details:

| Field | Value |
|-------|-------|
| Network Name | Sepolia Testnet |
| RPC URL | `https://sepolia.infura.io/v3/YOUR_INFURA_KEY` or `https://rpc.sepolia.org` |
| Chain ID | `11155111` |
| Currency Symbol | `SepoliaETH` |
| Block Explorer | `https://sepolia.etherscan.io` |

4. Click **Save** and switch to Sepolia Testnet

---

## Step 3 — Get Free Sepolia Test ETH

You need Sepolia ETH to pay gas fees and enter the lottery. Use one of these faucets:

| Faucet | URL |
|--------|-----|
| Alchemy Sepolia Faucet | https://sepoliafaucet.com |
| Infura Sepolia Faucet | https://www.infura.io/faucet/sepolia |
| Chainlink Faucet | https://faucets.chain.link/sepolia |
| QuickNode Faucet | https://faucet.quicknode.com/ethereum/sepolia |

1. Copy your MetaMask wallet address
2. Paste it into any faucet above
3. Complete the verification and request ETH
4. Wait 1–2 minutes for the ETH to arrive in your wallet
5. Confirm balance in MetaMask — you need at least **0.05 ETH** to test comfortably

---

## Step 4 — Open Remix IDE

1. Go to [remix.ethereum.org](https://remix.ethereum.org)
2. In the left sidebar, click the **File Explorer** icon
3. Click the **+** icon to create a new file
4. Name it `AutoLoto.sol`
5. Copy and paste the full contract code from [`AutoLoto.sol`](../AutoLoto.sol) in this repository

---

## Step 5 — Compile the Contract

1. In Remix, click the **Solidity Compiler** icon (left sidebar, looks like `<S>`)
2. Set compiler version to **`0.8.0`** or any `^0.8.x`
3. Click **"Compile AutoLoto.sol"**
4. You should see a green checkmark — no errors

---

## Step 6 — Connect MetaMask to Remix

1. In Remix, click the **Deploy & Run Transactions** icon (left sidebar)
2. Under **Environment**, select **"Injected Provider - MetaMask"**
3. MetaMask will pop up — click **Connect** and approve
4. Confirm your wallet address appears in the **Account** field in Remix
5. Make sure the network shows **Sepolia** in MetaMask

---

## Step 7 — Deploy the Contract

1. In Remix Deploy panel, ensure **Contract** is set to `AutoLotto`
2. Leave constructor parameters empty (none required)
3. Click the orange **Deploy** button
4. MetaMask will pop up with a gas fee estimate — click **Confirm**
5. Wait 15–30 seconds for the transaction to be mined
6. The deployed contract will appear under **"Deployed Contracts"** in Remix
7. Copy the contract address — you'll need it for Etherscan verification

---

## Step 8 — Verify on Etherscan

1. Go to [sepolia.etherscan.io](https://sepolia.etherscan.io)
2. Search for your contract address
3. You should see the deployment transaction
4. Click **"Contract"** tab → **"Verify and Publish"** to make the source code public
5. Select:
   - Compiler: Solidity (Single file)
   - Compiler version: `v0.8.0`
   - License: MIT
6. Paste the contract source code and click **Verify**

---

## Step 9 — Interact with the Contract

### Enter the Lottery

1. In Remix under "Deployed Contracts", expand your deployed AutoLotto
2. Find the `enterLottery` function
3. In the **Value** field (top of Deploy panel), enter `10000000000000000` (= 0.01 ETH in Wei)
4. Select **Wei** from the dropdown
5. Click `enterLottery` — MetaMask will confirm the transaction

### Check Players

1. Click `getPlayers` (no ETH needed)
2. The list of participant addresses will appear below the button

### Pick a Winner (Owner Only)

1. Make sure MetaMask is connected with the **owner wallet** (the one that deployed)
2. Click `pickWinner`
3. Confirm in MetaMask
4. The entire contract balance transfers to the winner automatically
5. The lottery resets for the next round

---

## Step 10 — Verify Transactions on Etherscan

After each action:

1. Go to [sepolia.etherscan.io](https://sepolia.etherscan.io)
2. Search your contract address: `0x7Cf12187dE99aBa948Dcb9260Dc9D817925ba16E`
3. Click **"Internal Txns"** to see ETH transfers
4. Click any transaction hash to see full details

---

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `Minimum ETH not sent` | Sent less than 0.01 ETH | Set value to exactly `10000000000000000` Wei |
| `Only owner can call this function` | Wrong wallet calling pickWinner | Switch MetaMask to the owner wallet |
| `Transfer failed` | No players in the lottery | Enter the lottery with at least 1 player first |
| Transaction stuck/pending | Gas price too low | Speed up in MetaMask or wait |
| MetaMask not connecting | Wrong network | Switch MetaMask to Sepolia Testnet |

---

## ETH Unit Reference

| Unit | Wei Value | ETH Value |
|------|-----------|-----------|
| Entry Fee | `10000000000000000` | 0.01 ETH |
| 0.05 ETH | `50000000000000000` | 0.05 ETH |
| 0.1 ETH | `100000000000000000` | 0.1 ETH |

**Tip:** Use [eth-converter.com](https://eth-converter.com) to convert between ETH and Wei.

---

## Re-Deploying the Contract

To deploy a fresh instance:

1. Repeat Steps 4–8 above
2. A new contract address will be generated
3. Update the contract address in `interact.py` and `.env` if using Python
