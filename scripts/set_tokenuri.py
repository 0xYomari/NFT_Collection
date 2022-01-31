from black import token
from brownie import accounts, network, NftCollection
from scripts.helpful_scripts import OPENSEA_URL, get_breed, get_account

dog_meatadata_dic = {
    "PUG": "https://ipfs.io/ipfs/QmRTxvZAdLgACDqxJxbTNjSASogyUqgToHwnDD4xbD4KcK?filename=1-PUG.json",
    "SHIBA-INU": "https://ipfs.io/ipfs/QmTdUckbgzzNVEYcd2yLoTCQ36cMy2CScifZCTrX9mW5Kx?filename=1-SHIBA-INU.json",
    "ST-BERNARD": "",
}


def main():
    print(f"Working on {network.show_active()}")
    nft_collection = NftCollection[-1]
    number_of_collectibles = nft_collection.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds")
    for token_id in range(number_of_collectibles):
        breed = get_breed(nft_collection.tokenIdToBreed(token_id))
        if not nft_collection.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokeURI of {token_id}")
            set_tokenURI(token_id, nft_collection, dog_meatadata_dic[breed])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes, and hit the refresh metadata butoon")
