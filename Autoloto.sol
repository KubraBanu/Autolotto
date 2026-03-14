// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/*
-----------------------------------------------------------
AutoLoto - A Blockchain Based Automated Lottery System
-----------------------------------------------------------

This smart contract creates a simple decentralized lottery.

Key idea:
Instead of trusting a company to run the lottery, the rules
are written directly into blockchain code.

This ensures:
- transparency
- automation
- no human manipulation

How the system works:

1. Users send ETH to enter the lottery.
2. Their wallet address is stored in a player list.
3. The contract owner triggers the winner selection.
4. A pseudo-random number selects a winner.
5. The entire ETH pool is automatically sent to the winner.
6. The lottery resets for the next round.

This contract runs on the Ethereum blockchain.
*/


contract AutoLoto {

    /*
    -----------------------------------------------------------
    STATE VARIABLES
    -----------------------------------------------------------
    These variables store important data on the blockchain.
    */

    // Address of the person who deployed the contract
    // This person becomes the lottery administrator
    address public owner;

    // Dynamic list that stores all participant wallet addresses
    address[] public players;

    // Minimum ETH required to join the lottery
    uint public entryFee = 0.01 ether;

    // Keeps track of how many lottery rounds have occurred
    uint public lotteryRound;


    /*
    -----------------------------------------------------------
    CONSTRUCTOR
    -----------------------------------------------------------

    The constructor runs ONLY ONCE when the contract is deployed.

    It sets:
    - the owner of the contract
    - the starting lottery round
    */

    constructor() {

        // msg.sender represents the wallet that deployed the contract
        owner = msg.sender;

        // Start lottery round counter at 1
        lotteryRound = 1;
    }


    /*
    -----------------------------------------------------------
    FUNCTION: enterLottery()
    -----------------------------------------------------------

    This function allows users to participate in the lottery.

    Key requirement:
    The user must send at least the required ETH entry fee.

    When successful:
    - their wallet address is added to the players list
    */

    function enterLottery() public payable {

        // Ensure the user sends enough ETH
        require(msg.value >= entryFee, "Minimum ETH not sent");

        // Add the sender's wallet address to the player list
        players.push(msg.sender);
    }


    /*
    -----------------------------------------------------------
    FUNCTION: getPlayers()
    -----------------------------------------------------------

    This is a "view" function.

    It allows anyone to see the list of current players
    without modifying the blockchain.

    No gas is required to call this function.
    */

    function getPlayers() public view returns(address[] memory) {

        return players;
    }


    /*
    -----------------------------------------------------------
    FUNCTION: pickWinner()
    -----------------------------------------------------------

    This function selects a random winner.

    Only the contract owner is allowed to call it.

    Steps:
    1. Generate a pseudo-random number
    2. Select a winner from the player list
    3. Transfer the entire contract balance to the winner
    4. Reset the lottery
    */

    function pickWinner() public {

        // Ensure only the owner can trigger the draw
        require(msg.sender == owner, "Only owner can pick winner");

        // Ensure at least one player has joined
        require(players.length > 0, "No players in the lottery");

        // Generate a random index based on the number of players
        uint index = random() % players.length;

        // Select the winner
        address winner = players[index];

        /*
        Transfer the entire ETH balance in the contract
        to the winner.

        We use "call" instead of "transfer" because transfer
        is deprecated in modern Solidity.
        */

        (bool success, ) = payable(winner).call{value: address(this).balance}("");

        require(success, "Transfer failed");

        // Reset player list for next round
        delete players;

        // Increment lottery round number
        lotteryRound++;
    }


    /*
    -----------------------------------------------------------
    FUNCTION: random()
    -----------------------------------------------------------

    This function generates a pseudo-random number.

    Important note:
    Blockchain randomness is difficult to achieve perfectly.
    For educational projects, we use blockchain data such as:

    - block timestamp
    - beacon chain randomness (prevrandao)
    - player list

    These values are hashed together using keccak256.
    */

    function random() internal view returns(uint) {

        return uint(

            keccak256(

                abi.encodePacked(

                    block.timestamp,

                    block.prevrandao,

                    players

                )

            )

        );
    }
}