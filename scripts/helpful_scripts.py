from brownie import accounts, network, config, VRFCoordinatorMock, LinkToken, Contract

LOCAL_BLOCKCHAIN_ENVIRONMENT = [
    "ganache",
    "local-ganache",
    "development",
    "hardhat",
    "mainnet-fork",
]

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


def get_account(id=None, index=None):
    if id:
        return accounts.load(id)
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {"link_token": LinkToken, "vrf_coordinator": VRFCoordinatorMock}


def get_contract(contract_name):
    """
    This function will either:
        - Get an address from the config
        - Or deploy a Mock to user for a network that doesn't have the contract

    Args:
        contract_name(string):This is the name of the contract that we will get
        from the config or deploy

    Returns:
        brownie.network.contract.ProjectContract: This is the most recently deployed
        contracts of the type specified by a dictionary. This could either be a mock
        or a 'real' contract on a live network.
    """
    # link_token
    # LinkToken
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        return contract


def deploy_mocks():
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print(f"The active network i s{network.show_active()}")
    print("Deploying mocks....")
    account = get_account()
    print("Deploying Mock LinkToken....")
    link_token = LinkToken.deploy({"from": account})
    print(f"Link Token deployed to {link_token.address}")
    print("Deploying Mock VRF Coordinator....")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print(f"VRFCoordinator deployed to {vrf_coordinator.address}")
    print("All Done!")
