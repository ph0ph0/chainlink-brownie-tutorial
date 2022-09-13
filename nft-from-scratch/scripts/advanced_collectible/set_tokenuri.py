from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed


def main():
    print("Working on " + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(
        "Number of advanced collectibles deployed is "
        + str(number_of_advanced_collectibles)
    )
    for token_id in range(number_of_advanced_collectibles):
        breed = getBreed(advanced_collectible.tokenIdToBreed(token_id))
        if advanced_collectible.tokenURI(token_id).startswith("None"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, advanced_collectible, ???)
            
    
