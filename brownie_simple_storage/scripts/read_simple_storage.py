# https://www.youtube.com/watch?v=M576WGiDBdQ&t=10028s
# 04:55:00
# This is an example of how you can read values from a contract that is deployed to a chain
# Note that we are accessing the SimpleStorage contract here, which has been deployed to
# rinkeby using the deploy.py script

from brownie import accounts, SimpleStorage, config

# Note that SimpleStorage is just an array. If we print it, it describes it as an object.
# We can access the address that it is deployed to by indexing into the 0th element
# eg SimpleStorage[0]. However, that is the first deployment of the contract. If we want
# the most recent, we use SimpleStorage[-1]


def read_contract():
    simple_storage = SimpleStorage[-1]
    # To interact with a contract, we need its address and its ABI.
    # Brownie has the address as it is in the build > deployments folder, and it has the
    # ABI in build > contracts folder. Therefore we can just call methods directly on the
    # contract variable.
    print(simple_storage.retrieveFavouriteNumber())
    pass


def main():
    read_contract()
