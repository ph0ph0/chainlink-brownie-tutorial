// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

// import "hardhat/console.sol";

contract SimpleStorage {
    // This will get initialised to 0
    uint256 favouriteNumber;

    struct Person {
        uint256 favouriteNumber;
        string name;
    }

    Person[] public people;
    mapping(string => uint256) public nameToFavouriteNumber;

    function addPerson(string memory _name, uint256 _favouriteNumber) public {
        people.push(Person({favouriteNumber: _favouriteNumber, name: _name}));
        nameToFavouriteNumber[_name] = _favouriteNumber;
        // console.log("fav num", nameToFavouriteNumber[_name]);
    }

    function store(uint256 _favouriteNumber) public returns (uint256) {
        favouriteNumber = _favouriteNumber;
        return favouriteNumber;
    }

    // view reads state from the BC.
    // pure only does maths and doesnt save state anywhere
    function retrieveFavouriteNumber() public view returns (uint256) {
        return favouriteNumber;
    }
}
