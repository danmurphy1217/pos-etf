import hashlib
import base64
from algosdk import mnemonic, algod
from typing import Dict
from algosdk import account, mnemonic
import json
def generate_new_account():
    """
    Generate a new Algorand account and print the public address
    and private key mnemonic.
    """
    private_key, public_address = account.generate_account()
    passphrase = mnemonic.from_private_key(private_key)
    return json.dumps({
        "Address": public_address,
        "Key": private_key,
        "Passphrase": passphrase
    })

def add_network_params(client: algod.AlgodClient, tx_data: Dict[str, str or int]) -> Dict[str, str or int]:
    """
    Adds network-related parameters to supplied transaction data.

    :param client -> ``algod.AlgodClient``: an algorand client object.
    :param tx_data -> ``Dict[str, str or int]``: data for the transaction.
    """
    params = client.suggested_params()
    tx_data["first"] = params.get("lastRound")
    tx_data["last"] = params.get("lastRound") + 1000
    tx_data["gh"] = params.get("genesishashb64")
    tx_data["gen"] = params.get("genesisID")
    tx_data["fee"] = .001
    tx_data["flat_fee"] = True
    return tx_data

def file_to_hash(filename: str, return_type="bytes") -> bytes:
    """
    read in byte data and return the SHA512/256 hash representation
    in base64.

    :param filename -> ``str``: the name of the file to read.
    :param return_type -> ``str``: the type of data to return.

    :return -> ``bytes``: hash repr of bytes.
    """
    file_bytes = open(filename, "rb").read()
    hasher = hashlib.sha256()
    hasher.update(file_bytes)

    if return_type == "bytes":
        return hasher.digest()
    elif return_type == "base64":
        return base64.b64encode(hasher.digest())

def wait_for_confirmation(client: algod.AlgodClient, transaction_id: str) -> Dict[str, str or int]:
    """
    Check for when the transaction is confirmed by the network. Once confirmed, return
    the transaction information.

    :param client -> ``algod.AlgodClient``: an algorand client object.
    :param transaction_id -> ``str``: id for the transaction.
    """
    last_round = client.status().get("lastRound")
    while True:
        transaction_info = client.pending_transaction_info(transaction_id)
        print(transaction_info)
        if transaction_info.get("round") and transaction_info.get("round") > 0:
            print(f"Transaction {transaction_id} confirmed in round {transaction_info.get('round')}.")
            return transaction_info
        else:
            print("Waiting for confirmation...")
            last_round += 1
            client.status_after_block(last_round)

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
    client.send_transaction(signed_transaction, headers={'content-type': 'application/x-binary'})
    transaction_info = wait_for_confirmation(client, transaction_id)
    return transaction_info

def balance_formatter(amount, asset_id, client):
    """
    Returns the formatted units for a given asset and amount.

    :param amount -> ``int``:
    :param asset_id -> ``int``: the ID for the asset.
    :param client -> ``algod.Client``: instantiated client object.
    """
    asset_info = client.asset_info(asset_id)
    decimals = asset_info.get("decimals")
    unit = asset_info.get("unitname")
    formatted_amount = amount/10**decimals
    return "{} {}".format(formatted_amount, unit)