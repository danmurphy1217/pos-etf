from dataclasses import dataclass
from typing import List, Dict
import requests


@dataclass
class Transaction:
    """
    Store data for each transaction retrieved
    from the Algorand blockchain.
    """

    sender: str
    receiver: str
    amount: int
    fee: int


def algo_poller(base_url: str, endpoint: str, params: Dict[str, int or str]) -> List[Transaction]:
    """
    poller function for extracting transaction data from the Algorand blockchain
    (via algorand indexer)

    :param base_url -> ``str``: the base url for the request
    :param endpoint -> ``str``: the endpoint for the request
    :param params -> ``Dict[str, int or str]``: params for the request object. Should be 
                    valid parameters for the request

    :return -> ``List[Transaction]``: list of all transactions for `asset_id` in the given wallet address.
    """
    response = requests.get(base_url + endpoint, params=params)
    response.raise_for_status()

    json_response = response.json()
    transactions = json_response['transactions']

    data = []
    for transaction in transactions:
        asset_transfer_transaction = transaction.get(
            "asset-transfer-transaction", None)
        if asset_transfer_transaction:
            amount = asset_transfer_transaction['amount']
            receiver = asset_transfer_transaction['receiver']
            fee = transaction['fee']
            sender = transaction['sender']
            data.append(Transaction(
                sender=sender,
                receiver=receiver,
                amount=amount,
                fee=fee
            ))
    return data


print(algo_poller(base_url="https://testnet.algoexplorerapi.io/idx2/", endpoint="/v2/transactions",
                  params={"address": "MXIGC5RCUFNFV2TB7ODAGQ4H7VC75DCH2SBBG7ATWPLB4YHBO7FFPNVLJ4", "asset-id": 14875048}))
