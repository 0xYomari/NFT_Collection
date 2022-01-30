from urllib import response
from brownie import NftCollection, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json


def main():
    nft_collection = NftCollection[-1]
    number_of_nft_collection = nft_collection.tokenCounter()
    print(f"You have created {number_of_nft_collection} collectibles!")
    for token_id in range(number_of_nft_collection):
        breed = get_breed(nft_collection.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
    collectible_metadata = metadata_template
    if Path(metadata_file_name).exists():
        print(f"{metadata_file_name} already exits! Delete it to overwrite")
    else:
        print(f"Creating metadata_file: {metadata_file_name}")
        collectible_metadata["name"] = breed
        collectible_metadata["description"] = f"An adorable {breed} pup!"
        image_path = "./img/" + breed.lower().replace("_", "_") + ".png"
        image_uri = upload_to_ipfs(image_path)
        collectible_metadata["image"] = image_uri
        with open(metadata_file_name, "w") as file:
            json.dump(collectible_metadata, file)
        upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
