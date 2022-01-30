from brownie import network, NftCollection
import time
import pytest
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENT,
    get_contract,
    get_account,
)
from scripts.deploy_and_create import deploy_and_create


def test_can_create_nft_collection_integration():
    # deploy the contract
    # create an NFT
    # get a random breed back
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip("ONly for integration testing")
    # Act
    nft_collection, creation_tx = deploy_and_create()
    time.sleep(60)
    # Assert
    assert nft_collection.tokenCounter() == 1
