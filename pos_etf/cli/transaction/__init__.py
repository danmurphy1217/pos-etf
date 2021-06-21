from algosdk.transaction import (
    AssetTransferTxn,
    write_to_file
)
from algosdk import algod

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

    def buy(self):
        """fire off a buy transaction to the algorand blockchain."""
        return Buy(self)

    def sell(self):
        """fire off a sell transaction to the algorand blockchain."""
        return Sell(self)


class Buy():
    def __init__(self, transaction: Transaction):
        self.transaction = transaction

    def transfer(self, amount: float) -> None:
        """
        Creates an unsigned transfer transaction that is then sent off for signing
        and submission to the blockchain via the `sign_and_send` utility function.

        The transaction is submitted for the specified `asset_id` to the specified address
        for the specified amount.

        :param amount -> ``float``: the amount of AlgoETF Coins to transfer.
        :param passphrase -> ``str``: the senders passphrase (used to sign the transaction)
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
        if self.transaction.passphrase:
            transaction_info = sign_and_send(
                transaction, self.transaction.passphrase, self.transaction.client)
            formatted_amount = balance_formatter(
                amount, asset_id, self.transaction.client)
            print("Transferred {} from {} to {}".format(
                formatted_amount, algoetf_addr, self.receiver_address))
            print("Transaction ID Confirmation: {}".format(
                transaction_info.get("tx")))
        else:
            write_to_file([transaction], "transfer.txn")


class Sell(Buy):
    def __init__(self, client: algod.AlgodClient, sender: str, receiver_address: str, passphrase: str, amount: float):
        """
        what do I need to allow someone to sell the token????
        """
        super().__init__(client, sender, receiver_address, passphrase, amount)
