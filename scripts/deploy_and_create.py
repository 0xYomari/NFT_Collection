from brownie import network, config, NftCollection
from scripts.helpful_scripts import (
    get_account,
    OPENSEA_URL,
    get_contract,
    fund_with_link,
)


def deploy_and_create():
    account = get_account()
    nft_collection = NftCollection.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )

    fund_with_link(nft_collection.address)
    creating_tx = nft_collection.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New token has been created!")
    return nft_collection, creating_tx


def main():
    deploy_and_create()
