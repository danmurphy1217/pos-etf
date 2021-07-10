from argparse import ArgumentError
from os import error
from algosdk.transaction import (
    PaymentTxn,
    AssetTransferTxn,
    write_to_file
)
from algosdk.v2client import algod

from cli.utils import add_network_params, sign_and_send, balance_formatter, convert_algos_to_microalgo
from cli.utils.constants import algoetf_addr, asset_id
class Transaction:

    def __init__(self, client: algod.AlgodClient, sender: str, receiver_address: str, buy_or_sell_passphrase: str, algo_exchange_passphrase: str, amount: float):
        """
        What is common across both buy and sell transactions? I should use
        the common values to instantiate this client
        """
        self.client = client
        self.sender = sender
        self.receiver_address = receiver_address
        self.buy_or_sell_passphrase = buy_or_sell_passphrase
        self.algo_exchange_passphrase = algo_exchange_passphrase
        self.amount = amount

    def do(self, *args):
        """
        perform the specified txn type.
        
        :param txn_type -> `str`: the type of txn to perform, as specified by args.buy or args.sell.
        """

        assert all(txn_type in ('buy', 'sell', 'exchange') for txn_type in args)
        
        for txn_type in args:
            print(txn_type)
            # if txn_type not in ('buy', 'sell', 'exchange'):
                # raise ArgumentError(None, "`txn_type` must be `buy`, `sell`, and/or `exchange`.")
            if txn_type == 'buy':
                txn_obj = Buy(self)
            elif txn_type == 'sell':
                txn_obj = Sell(self)
            elif txn_type == 'exchange':
                txn_obj = Exchange(self)

            txn_obj.transfer() # perform the txn

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

        formatted_algo_amt = self.transaction.amount

        transfer_data = {
            "sender": self.transaction.sender,
            "receiver": self.transaction.receiver_address,
            "amt": formatted_algo_amt,
            "index": asset_id,
        }

        data = add_network_params(self.transaction.client, transfer_data)
        transaction = AssetTransferTxn(**data)
        print(data)

        if self.transaction.buy_or_sell_passphrase:
            transaction_info = sign_and_send(
                transaction, self.transaction.buy_or_sell_passphrase, self.transaction.client)
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
        super().__init__(transaction)

class Exchange(Sell):
    def __init__(self, transaction: Transaction):
        """
        what do I need to allow someone to exchange the token????
        """
        super().__init__(transaction)
    
    def transfer(self):
        """
        exchange algos for the token (from buyer -> seller if Sell(), seller -> buyer if Buy())
        """
        # ! If Sell(), algos move from ETF Address to user addr, if Buy() algos move from user addr to ETF addr
        # ! the only real diff is who is signing the txn (whose passphrase do we need to complete the txn?)

        formatted_algo_amt = round(convert_algos_to_microalgo(self.transaction.amount))

        payment_data = {
            "sender": self.transaction.receiver_address, # the person receiving the token must liquidate algos
            "receiver": self.transaction.sender, # the person sending the token to another receives algos in return
            "amt": formatted_algo_amt,
        }

        data = add_network_params(self.transaction.client, payment_data)
        transaction = PaymentTxn(**data)

        if self.transaction.algo_exchange_passphrase:
            transaction_info = sign_and_send(
                transaction, self.transaction.algo_exchange_passphrase, self.transaction.client)
            formatted_amount = balance_formatter(
                self.transaction.amount, asset_id, self.transaction.client)
            print("Transferred {} Algos from {} to {}".format(
                self.transaction.amount, self.transaction.receiver_address, self.transaction.sender))
            print(transaction_info)
            print("Transaction ID Confirmation: {}".format(
                transaction_info.get("tx")))
        else:
            write_to_file([transaction], "transfer.txn")