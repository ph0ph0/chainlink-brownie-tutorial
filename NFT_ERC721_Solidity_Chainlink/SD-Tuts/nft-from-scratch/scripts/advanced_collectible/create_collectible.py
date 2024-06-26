from brownie import AdvancedCollectible, accounts, config
from scripts.helpful_scripts import get_breed
import time

STATIC_SEED = 123


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    transaction = advanced_collectible.createCollectible(
        STATIC_SEED, "None", {"from": dev}
    )
    # Wait for confirmations
    transaction.wait(1)
    requestId = transaction.events["requestedCollectible"]["requestId"]
    tokenId = advanced_collectible.requestIdToTokenId(requestId)
    time.sleep(35)
    breed = get_breed(advanced_collectible.tokenIdToBreed(tokenId))
    print("dog breed of tokenId {} is {}".format(tokenId, breed))
