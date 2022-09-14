from brownie import accounts, config, SimpleStorage

# To run the tests, run `brownie test`
# To run only one test: `brownie test -k <test name>`
# To run a python shell for debugging if the test fails `brownie test --pdb`
# You can then use this to paste in variables to work out what went wrong
# To run verbose `brownie test -s`
# NOTE PyTest is the brains behind brownie testing so you refer to those docs


def test_deploy():
    # Arrange
    account = accounts[0]
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieveFavouriteNumber()
    expected = 0
    # Assert
    assert expected == starting_value


def test_updating_storage():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # Act
    expected = 15
    simple_storage.store(15, {"from": account})
    # Assert
    assert expected == simple_storage.retrieveFavouriteNumber()
