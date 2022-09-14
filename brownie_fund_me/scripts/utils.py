from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_price_feed_address():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        print(f"The active network is ${network.show_active()}")
        return config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        print(f"The active network is ${network.show_active()}")
        print("Deploying mocks...")
        # We only need to deploy this contract once
        if len(MockV3Aggregator) <= 0:
            # 18 decimal points, starting value of 2000*10^8
            MockV3Aggregator.deploy(
                DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": account}
            )
        print(f"Mocks deployed!")
        # Return the most recent deployment, of which there will only be one
        return MockV3Aggregator[-1].address


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
