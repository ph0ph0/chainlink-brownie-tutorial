from brownie import accounts, network, AdvancedCollectible
from metadata import sample_metadata
from scripts.helpful_scripts import get_breed
from pathlib import Path
import os
import requests
import json


def main():
    print("Working on " + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    print("advanced collectible: {}".format(advanced_collectible))
    number_of_tokens = advanced_collectible.tokenCounter()
    print("The number of deployed tokens is {}".format(number_of_tokens))
    write_metadata(number_of_tokens, advanced_collectible)


def write_metadata(number_of_tokens, nft_contract):
    for token_id in range(number_of_tokens):
        collectible_metadata = sample_metadata.metadata_template
        breed = get_breed(nft_contract.tokenIdToBreed(token_id))
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active())
            + str(token_id)
            + "-"
            + breed
            + ".json"
        )
    if Path(metadata_file_name).exists():
        print("{} already exists!".format(metadata_file_name))
    else:
        print("Creating metadata file {}".format(metadata_file_name))
        collectible_metadata["name"] = breed = get_breed(
            nft_contract.tokenIdToBreed(token_id)
        )
        collectible_metadata["description"] = "A beautiful {} pup!".format(
            collectible_metadata["name"]
        )
        print("Collectible_metadata: {}".format(collectible_metadata))
        image_to_upload = None
        if os.getenv("UPLOAD_IPFS") == "true":
            image_path = "./img/{}.png".format(breed.lower().replace("_", "-"))
            image_to_upload = upload_to_ipfs(image_path)
        collectible_metadata["image"] = image_to_upload
        with open(metadata_file_name, "w") as file:
            json.dump(collectible_metadata, file)
        if os.getenv("UPLOAD_IPFS") == "true":
            upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://localhost:5001"
        response = requests.post(
            ipfs_url + "/api/v0/add", files={"files": image_binary}
        )
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        uri = "https://ipfs.io/ipfs/{}?filename={}".format(ipfs_hash, filename)
        print(uri)
        return uri
    return None


# http://127.0.0.1:5001/
# curl -X POST -F file=@img/pug.png http://localhost:5001/api/v0/add
# 0x2930FF5F0b22C4E801A0BCdA1f0dFf99B0634Bab
