from config import (
    creator_address,
    creator_passphrase,
    receiver_address,
    asset_id,
    receiver_passphrase,
    asset_details
)
from util import (
    add_network_params,
    sign_and_send,
    generate_new_account,
    balance_formatter
)
from algosdk import algod
from algosdk.transaction import (
    AssetConfigTxn, 
    AssetTransferTxn, 
    write_to_file
)
from pathlib import Path
import os
import asyncio, aiofiles
from util import generate_new_account

def generate_accounts():
    """generate creator and receiver accounts for test transactions."""
    for i in range(2):
        open(f"account_{i}.json", "w").write(generate_new_account())

async def get_api_token(home_dir: str) -> str:
    """
    retrieve and return the API token from the $HOME/node/data folder.

    :param home_dir -> ``str``: the home directory of the current user.
    :return -> ``str``: the API token
    """
    async with aiofiles.open(os.path.join(home_dir, "algod.token"), "r") as api_token_file:
        api_token = await api_token_file.read()
    
    return api_token.strip()

async def get_network_info(home_dir: str) -> str:
    """
    retrieve and return the network information (URL and PORT)

    :param home_dir -> ``str``: the home directory of the current user.
    :return -> ``str``: the URL and PORT formatted as http://{URL}:{PORT}
    """
    async with aiofiles.open(os.path.join(home_dir, "algod.net"), "r") as algorand_network_file:
        network_info = await algorand_network_file.read()
        cleaned_network_info = network_info.strip()
    
    return "http://{0}".format(cleaned_network_info)

def create(passphrase:str= None):
    """
    creates the asset that is defined in `config.py`, signs it, and sends it
    to the algorand network if the senders passphrase is supplied. Otherwise,
    the transaction is written to a file.

    :param passphrase -> ``str``: the user passphrase.
    """
    transaction_data = add_network_params(client, asset_details)
    transaction = AssetConfigTxn(**transaction_data)

    if passphrase:
        transaction_info = sign_and_send(transaction, passphrase, client)
        print(f"Create asset confirmation, transaction ID: {transaction}")
        asset_id = transaction_info['txresults'].get('createdasset')
        print(f"Asset ID: {asset_id}")
    else:
        write_to_file([transaction], "create_coin.txn")

def opt_in(passphrase:str= None):
    """
    Creates, signs, and sends an opt-in transaction for the specified asset_id.
    If the passphrase is not supplied, writes the unsigned transaction to a file.

    :param passphrase -> ``str``: the user passphrase.
    """
    opt_in_data = {
        "sender": creator_address,
        "receiver": receiver_address,
        "amt": 10,
        "index": asset_id
    }

    transaction_data = add_network_params(client, opt_in_data)
    transaction = AssetTransferTxn(**transaction_data)
    if passphrase:
        txinfo = sign_and_send(transaction, passphrase, client)
        created_asset_id = txinfo['txresults'].get('createdasset')
        print("Opted in to asset ID: {}".format(created_asset_id))
        print("Transaction ID Confirmation: {}".format(txinfo.get("tx")))
    else:
        write_to_file([transaction], "optin.txn")

def check_holdings(asset_id, address):
    """
    Checks the asset balance for the specific address and asset id.
    """
    account_info = client.account_info(address)
    assets = account_info.get("assets")
    if assets:
        asset_holdings = account_info["assets"]
        print(asset_holdings)
        asset_holding = asset_holdings.get(str(asset_id))
        print(asset_holding)
        if not asset_holding:
            print("Account {} must opt-in to Asset ID {}.".format(address, asset_id))
        else:
            amount = asset_holding.get("amount")
            print("Account {} has {}.".format(address, balance_formatter(amount, asset_id, client)))
    else:
        print("Account {} must opt-in to Asset ID {}.".format(address, asset_id))

HOME_DIR = str(Path.home())
ALGORAND_NODE_DIR = os.path.join(HOME_DIR, "node")
ALGORAND_MAIN_NET_DATA_DIR = os.path.join(ALGORAND_NODE_DIR, "testnetdata")

client = algod.AlgodClient(asyncio.run(get_api_token(ALGORAND_MAIN_NET_DATA_DIR)), asyncio.run(get_network_info(ALGORAND_MAIN_NET_DATA_DIR)))

# print(create(creator_passphrase))
# opt_in(creator_passphrase)
print(check_holdings(asset_id, "MXIGC5RCUFNFV2TB7ODAGQ4H7VC75DCH2SBBG7ATWPLB4YHBO7FFPNVLJ4"))