from brownie import NftCollection
from scripts.helpful_scripts import fund_with_link, get_account
from web3 import Web3


def main():
    account = get_account()
    nft_collection = NftCollection[-1]
    fund_with_link(nft_collection.address, amount=Web3.toWei(0.1, "ether"))
    creation_tx = nft_collection.createCollectible({"from": account})
    creation_tx.wait(1)
    print("Collection Created!")
