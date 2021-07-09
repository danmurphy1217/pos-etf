from argparse import ArgumentError
from os import error
from algosdk.transaction import (
    AssetTransferTxn,
    write_to_file
)
from algosdk.v2client import algod

from cli.utils import add_network_params, sign_and_send, balance_formatter
from cli.utils.constants import algoetf_addr, asset_id


class Transaction:

    def __init__(self, client: algod.AlgodClient, sender: str, receiver_address: str, passphrase: str, amount: float):
        """
        What is common across both buy and sell transactions? I should use
        the common values to instantiate this client
        """
        self.client = client
        self.sender = sender
        self.receiver_address = receiver_address
        self.passphrase = passphrase
        self.amount = amount

    def do(self, txn_type: str):
        """
        perform the specified txn type.
        
        :param txn_type -> `str`: the type of txn to perform, as specified by args.buy or args.sell.
        """
        if txn_type not in ('buy', 'sell'):
            raise ArgumentError(None, "`txn_type` must be buy or sell.")

        return Buy(self).transfer() if txn_type == 'buy' else Sell(self).transfer()


class Buy():
    def __init__(self, transaction: Transaction):
        self.transaction = transaction

    def transfer(self) -> None:
        """
        Creates an unsigned transfer transaction that is then sent off for signing
        and submission to the blockchain via the `sign_and_send` utility function.

        The transaction is submitted for the specified `asset_id` to the specified address
        for the specified amount.

        :return -> ``None``:
        """

        transfer_data = {
            "sender": self.transaction.sender,
            "receiver": self.transaction.receiver_address,
            "amt": self.transaction.amount,
            "index": asset_id,
        }

        data = add_network_params(self.transaction.client, transfer_data)
        transaction = AssetTransferTxn(**data)
        print(data)

        if self.transaction.passphrase:
            transaction_info = sign_and_send(
                transaction, self.transaction.passphrase, self.transaction.client)
            formatted_amount = balance_formatter(
                self.transaction.amount, asset_id, self.transaction.client)
            print("Transferred {} from {} to {}".format(
                formatted_amount, self.transaction.sender, self.transaction.receiver_address))
            print("Transaction ID Confirmation: {}".format(
                transaction_info.get("tx")))
        else:
            write_to_file([transaction], "transfer.txn")


class Sell(Buy):
    def __init__(self, transaction: Transaction):
        """
        what do I need to allow someone to sell the token????
        """
        super().__init__(transaction)
