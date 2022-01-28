from brownie import network, config, NftCollection
from scripts.helpful_scripts import get_account, OPENSEA_URL, get_contract


def deploy_and_create():
    account = get_account()
    nft_collection = NftCollection.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )


def main():
    deploy_and_create()
