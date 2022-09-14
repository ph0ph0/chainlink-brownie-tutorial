// SPDX-License_Identifier: MIT

pragma solidity >=0.6.6 <0.9.0;

// AggregatorV3Interface is an interface contract. These compile down to ABI and are needed
// to interact with another contract. This one is used to get the price feed of asset pairs.
// We pass in the address of the contract that we want to interact with and then can use the
// interface to interact with it.
// You can find the repo here: https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol
// If we look at the code, we can see that it has 3 functions stubs. This is what we use to interact with
// contracts that will get us a price feed.
// You can find the list of feeds for MN here: https://data.chain.link/ethereum/mainnet
// Unfortunately I cant find the rinkeby addresses page, below is the rinkeby Eth/USD pair i found though.
// 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
//

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

// If using solidity version < 0.8, you should use safe math to prevent overflow.
// import SafeMath;

contract FundMe {
    // This keeps track of how much money each address has sent
    mapping(address => uint256) public addressToAmountFunded;

    // Incredibly, you can't access the keys of a mapping in s,
    // you must know them before hand...
    address[] public funders;

    // Owner of the contract
    address public owner;

    // The public feed for getting the token price
    AggregatorV3Interface public priceFeed;

    constructor(address _publicFeedAddress) public {
        // The account that deploys the contract
        owner = msg.sender;

        // Setup the priceFeed
        priceFeed = AggregatorV3Interface(_publicFeedAddress);
    }

    // A payable function is a function that you can send Wei to.
    // Each function has a "value" input, and that is how much
    // wei you would like to send to that function.
    function fund() public payable {
        // We want this function to only allow donations greater than
        // 50 dollars. We must ensure that everything has 18 decimals...
        // That is so confusing.
        uint256 minUsdAmount = 0;

        // A require statement is like an assert in Cadence.
        require(
            getUSDConversion(msg.value) >= minUsdAmount,
            "You need to spend more ETH!"
        );

        // msg.sender is the address of the caller of the function
        // msg.value is the wei that they sent to the function
        addressToAmountFunded[msg.sender] += msg.value;

        //  We need to know what the ETH -> USD exchange rate is.
    }

    function getVersion() public view returns (uint256) {
        // This line here says that we have a contract at this address that implements this interface.
        // If that is true, then we should be able to call a function from this interface.
        // Note that if we want to use the priceFeed, we must deploy the contract to rinkeby, which means that
        // we must set the environment on the left to Injected Web 3 so that we can use MM to select Rinkeby.

        priceFeed.version();
    }

    // This method gets the current usd/eth price, with 8 decimal places, so you need to add
    // the decimal 8 from the end.
    function getPrice() public view returns (uint256) {
        // Destructure the tuple out of the return from latestRoundData();
        (, int256 answer, , , ) = priceFeed.latestRoundData();

        // We multiply by 10^10 as answer comes back with 8 decimal places, we
        // need to convert it to wei which is 10^18
        return uint256(answer * 1000000000);
    }

    function getUSDConversion(uint256 ethAmount) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        // We need to divide by 10^18 to remove the 10^18 supplied by each factor.
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

    function getEntranceFee() public view returns (uint256) {
        // minimumUsd
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    modifier onlyOwner() {
        // Ensure that the person calling is the owner of the contract.
        require(msg.sender == owner, "You are not the owner!");
        // The underscore ensures that the code run afterwards is executed
        _;
    }

    // This function withdraws the funds in the contract to the caller
    function withdraw() public payable onlyOwner {
        // Every address has a transfer method that allows you to send it
        // ether.
        // We get the balance of the contract by grabbing the address using
        // the 'this' keyword, which refers to the contract that we are
        // currently in.
        // We must cast the msg.sender address as payable so that it can
        // receive the funds that we are sending to it.
        payable(msg.sender).transfer((address(this).balance));

        // When we empty the contract, we want to also empty the
        // addressToAmountFunded mapping. Incredibly, in s, there
        // is no clean way to empty an array or access the values
        // under the keys if you dont know the key. Therefore, we
        // have to keep track using the funders array.
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        // reset the array as well
        funders = new address[](0);
    }
}
