from brownie import network, NftCollection
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENT,
    get_contract,
    get_account,
)
from scripts.deploy_and_create import deploy_and_create


def test_can_create_advanced_collection():
    # deploy the contract
    # create an NFT
    # get a random breed back
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip("ONly for local testing")
    # Act
    nft_collection, creation_tx = deploy_and_create()
    requestId = creation_tx.events["requestCollectible"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, nft_collection.address, {"from": get_account()}
    )
    # Assert
    assert nft_collection.tokenCounter() == 1
    assert nft_collection.tokenIdToBreed(0) == random_number % 3
