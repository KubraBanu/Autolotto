require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.0",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },

  networks: {
    // Local development network (default)
    hardhat: {
      chainId: 31337,
    },

    // Ethereum Sepolia Testnet
    sepolia: {
      url: process.env.RPC_URL || "https://rpc.sepolia.org",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
      chainId: 11155111,
      gasPrice: "auto",
    },
  },

  // Etherscan verification (optional)
  etherscan: {
    apiKey: {
      sepolia: process.env.ETHERSCAN_API_KEY || "",
    },
  },

  // Path configuration
  paths: {
    sources:   "./",        // Looks for .sol files in root
    tests:     "./test",
    cache:     "./cache",
    artifacts: "./artifacts",
  },
};
