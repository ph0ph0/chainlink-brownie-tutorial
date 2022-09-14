# https://www.youtube.com/watch?v=M576WGiDBdQ&t=10028s
# Lesson 5: 04:27

# --Intro--
# This is the deployment script. We run scripts in brownise using `brownie run <path>`

# Brownie has it's own account handling package, and we can import the yaml file as config
from brownie import accounts, config, network

# We can also import our contracts easily
from brownie import SimpleStorage
import os

# To deploy to testnet, run `brownie networks list` to see what nw are available.
# Then specify the network as a flag: `brownie run ./scripts/deploy.py --network rinkeby`


def deploy():
    # --Accounts--
    # You can access the nth account in the brownie package using the below
    # account = accounts[0]
    # print("0th brownie account", account)
    # If you want to add your own account and private key, run brownie accounts new <name-of-account>
    # I added one called dev-account. This is apparently one of the safest ways to add your keys.
    # To see the acounts run `brownie accounts list`
    # To load an account that you have added:
    # account = accounts.load("dev-account")
    # print("dev-account", account)
    # To load an account from .env file
    account = accounts.add(os.getenv("PRIVATE_KEY"))
    print(".env dev account", account)
    # To load an account from brownie-config.yaml
    account = accounts.add(config["wallets"]["from_key"])
    print("brownie-config.yaml account", account)
    # To load using a custom function
    account = get_account()

    # --Deployment--
    # the deploy command wraps up a whole load of manual code that we had to write before.
    # It must alwasy contain a 'from' k/v.
    simple_storage = SimpleStorage.deploy({"from": account})
    print("simple_storage", simple_storage)
    # Brownie is smart enough to know that because this is a view function, it must be a call
    stored_value = simple_storage.retrieveFavouriteNumber()
    print("stored value", stored_value)
    # We can call a function in a contract using the following approach. We must always include
    # the 'from' k/v
    tx = simple_storage.store(15, {"from": account})
    updated_value = simple_storage.retrieveFavouriteNumber()
    print("updated value", updated_value)
    pass


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy()
