from brownie import AdvancedCollectible, network, interface
from scripts.helpful_scripts import get_breed, get_account
from metadata.rinkeby.urls import dog_ipfs_urls

OPENSEA_FORMAT = OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"


def main():
    print("Working on " + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(
        "Number of advanced collectibles deployed is "
        + str(number_of_advanced_collectibles)
    )

    urls = dog_ipfs_urls.dog_urls

    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        print("url for {}: ".format(breed) + str(urls[breed]))
        if advanced_collectible.tokenURI(token_id).startswith("None"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, advanced_collectible, urls[breed])
        else:
            print("Skipping {}, we've already set that tokenURI".format(token_id))


def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = get_account()
    transaction = nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    # Wait for confirmations
    transaction.wait(1)
    print("Transaction: " + str(transaction))
    print(
        "Awesome! You can now view your nft on OpenSea at ".format(
            OPENSEA_FORMAT.format(nft_contract.address, token_id)
        )
    )
    print("Please give up to 20 mins and hit the refresh metadata button")
