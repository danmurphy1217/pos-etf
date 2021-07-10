import re
from typing import List, Dict
from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk import algod as algod_v1
from . import constants

def clean_acct_names(user_dotfile: str) -> List[str]:
    """
    clean all account names and return them

    :param user_dotfile -> ``str``: path to users `.pos_etf` dotfile
    """
    all_acct_names = filter(
        re.compile(
            r"^\[[a-zA-Z0-9]").search, open(user_dotfile).readlines()
    )

    def formatted_acct_names(acct_names): return [
        name.strip("[]\n") for name in acct_names
    ]

    list_of_formatted_acct_names = formatted_acct_names(all_acct_names)

    return list_of_formatted_acct_names


def extract_matching_pub_key(acct_name: str, dotfile_contents: List[str]):
    """
    extract public key that matches `acct_name`.

    :param acct_name -> ``str``: the name of the account
    """
    index_of_acct_name = dotfile_contents.index(acct_name)
    index_of_pub_key = index_of_acct_name + 1

    messy_pub_key = dotfile_contents[index_of_pub_key]

    clean_pub_key = messy_pub_key.split(" = ")[-1]
    return clean_pub_key


def extract_matching_passphrase(acct_name: str, dotfile_contents: List[str]):
    """
    extract the passphrase that matches `acct_name`.

    :param acct_name -> ``str``: the name of the account
    """
    index_of_acct_name = dotfile_contents.index(acct_name)
    index_of_passphrase = index_of_acct_name + 2

    messy_passphrase = dotfile_contents[index_of_passphrase]

    clean_passphrase = messy_passphrase.split(" = ")[-1]
    return clean_passphrase


def add_network_params(client: algod.AlgodClient, tx_data: Dict[str, str or int]) -> Dict[str, str or int]:
    """
    Adds network-related parameters to supplied transaction data.

    :param client -> ``algod.AlgodClient``: an algorand client object.
    :param tx_data -> ``Dict[str, str or int]``: data for the transaction.
    """
    params = client.suggested_params()
    tx_data["first"] = params.first
    tx_data["last"] = params.last
    tx_data["gh"] = params.gh
    tx_data["gen"] = params.gen
    tx_data["fee"] = round(convert_algos_to_microalgo(.01))
    tx_data["flat_fee"] = True
    return tx_data


def sign_and_send(transaction: str, passphrase: str, client: algod.AlgodClient) -> Dict[str, str or int]:
    """
    sign and send a transaction to the algorand network. Return the transaction
    info when the transaction is completed.

    :param transaction -> ``algosdk.transaction.AssetTransferTxn``: the transaction object.
    :param passphrase -> ``str``: the public key for the user involved in the transaction.
    :param client -> ``algod.AlgodClient``: an algorand client object.
    """
    private_key = mnemonic.to_private_key(passphrase)
    signed_transaction = transaction.sign(private_key)
    transaction_id = signed_transaction.transaction.get_txid()
    client.send_transaction(signed_transaction, headers={
                            'content-type': 'application/x-binary'})
    transaction_info = wait_for_confirmation(client, transaction_id)
    return transaction_info


def wait_for_confirmation(client: algod.AlgodClient, transaction_id: str, timeout: int = 100) -> Dict[str, str or int]:
    """
    Check for when the transaction is confirmed by the network. Once confirmed, return
    the transaction information.

    :param client -> ``algod.AlgodClient``: an algorand client object.
    :param transaction_id -> ``str``: id for the transaction.
    """
    start_round = client.status()["last-round"] + 1;
    current_round = start_round


    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return 
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:  
            raise Exception(
                'pool error: {}'.format(pending_txn["pool-error"]))
        client.status_after_block(current_round)                   
        current_round += 1
    raise Exception(
        'pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))

    # while True:
    #     transaction_info = client.pending_transaction_info(transaction_id)
    #     print(transaction_info)
    #     if transaction_info.get("round") and transaction_info.get("round") > 0:
    #         print(
    #             f"Transaction {transaction_id} confirmed in round {transaction_info.get('round')}.")
    #         return transaction_info
    #     else:
    #         print("Waiting for confirmation...")
    #         current_round += 1
    #         print(current_round)
    #         client.status_after_block(current_round)


def balance_formatter(amount, asset_id, client):
    """
    Returns the formatted units for a given asset and amount.

    :param amount -> ``int``:
    :param asset_id -> ``int``: the ID for the asset.
    :param client -> ``algod.Client``: instantiated client object.
    """
    v1_client = algod_v1.AlgodClient(client.algod_token, client.algod_address, headers={'User-Agent': 'DanM'})
    
    asset_info = v1_client.asset_info(asset_id)
    decimals = asset_info.get("decimals")
    unit = asset_info.get("unitname")
    formatted_amount = amount/10**decimals
    return "{} {}".format(formatted_amount, unit)

def convert_microalgos_to_algos(microalgos_amt : int):
    return microalgos_amt * constants.amt_algos_in_one_microalgo

def convert_algos_to_microalgo(algos_amt : int):
    return algos_amt * constants.amt_microalgos_in_one_algo