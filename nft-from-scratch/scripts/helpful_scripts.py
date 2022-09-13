from brownie import AdvancedCollectible, accounts, config, interface, network

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_breed(breed_number):
    switch = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}
    return switch[breed_number]


def fund_advanced_collectible(nft_contract):
    dev = get_account()
    link_token = interface.LinkTokenInterface(
        config["networks"][network.show_active()]["link_token"]
    )
    link_token.transfer(nft_contract, 100000000000000000, {"from": dev})


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
