// SPDX-License-Identifer: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    address payable[] public players;

    uint256 public usdEntryFee;

    AggregatorV3Interface internal ethUsdPriceFeed;

    constructor(address _priceFeedAddress) public {
        usdEntryFee = 50 * 10**18;
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
    }

    function enter() public {
        // minimum $50
        // require(msg.value >= getEntryFee());
        players.push(msg.sender);
    }

    function getEntryFee() public {
        // Get the stored minimum value
        (, int256 price, , , , ) = ethUsdPriceFeed.latestRoundData();
        // By raising to power 10 we give it 18 decimals as if we check the price
        // feed we can see it already has 8
        uint256 adjustedPrice = uint256(price) * 10**10;
        // We raise useEntryFee to power of 18 to set it to 18 decimals.
        // Since we are dividing by a number with 18 decimals, they
        // cancel each other out.
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public {}

    function endLottery() public {}
}
