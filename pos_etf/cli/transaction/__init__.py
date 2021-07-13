from argparse import ArgumentError
import asyncio
from os import error
from algosdk.transaction import (
    PaymentTxn,
    AssetTransferTxn,
    write_to_file
)
from algosdk.v2client import algod

from cli.utils import (
    add_network_params,
    sign_and_send,
    balance_formatter,
    convert_algos_to_microalgo,
    get_algorand_price
)
from cli.utils.constants import algoetf_addr, asset_id
from cli.weights.net_asset_value import NetAssetValue
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
    
    def build_txn(self, txn_obj: PaymentTxn or AssetTransferTxn, **kwargs):
        """
        build a txn object based on the provided kwargs.

        :param txn_obj -> ``PaymentTxn`` or ``AssetTransferTxn``: the txn object to pass the kwargs to.
        :param kwargs -> ``dict``: the kwargs to pass to the txn object.
        """
        transfer_data = {
            "sender": kwargs.get("sender"),
            "receiver": kwargs.get("receiver"),
            "amt": kwargs.get("amt")
        }

        if txn_obj == AssetTransferTxn:
            transfer_data["index"] = kwargs.get("index")

        data = add_network_params(self.transaction.client, transfer_data)
        transaction = txn_obj(**data)
        return transaction
    
    def send_txns(self, txns: PaymentTxn or AssetTransferTxn):
        """
        send txn to the algorand network
        
        :param txns -> ``PaymentTxn`` or ``AssetTransferTxn``: list of ``PaymentTxn`` or ``AssetTransferTxn`` transactions to.
        """
        def handle_algo_txn():
            transaction_info = sign_and_send(
                txn, self.algo_exchange_passphrase, self.client)
            formatted_amount = balance_formatter(
                self.amount, asset_id, self.client)
            print("Transferred {} Algos from {} to {}".format(
                self.amount, self.receiver_address, self.sender))

            print("Transaction ID Confirmation: {}".format(
                transaction_info.get("tx"))) 

        def handle_etf_txn():
            transaction_info = sign_and_send(
                txn, self.buy_or_sell_passphrase, self.client)
            formatted_amount = balance_formatter(
                self.amount, asset_id, self.client)
            print("Transferred {} from {} to {}".format(
                formatted_amount, self.sender, self.receiver_address))
            print("Transaction ID Confirmation: {}".format(
                transaction_info.get("tx")))

        for txn in txns:
            if isinstance(txn, PaymentTxn):
                if self.algo_exchange_passphrase:
                    handle_algo_txn()       
                else:
                    write_to_file([txn], "transfer.txn")
            
            elif isinstance(txn, AssetTransferTxn):
                if self.buy_or_sell_passphrase:
                    handle_etf_txn()
                else:
                    write_to_file([txn], "transfer.txn")


    def do(self, *args):
        """
        perform the specified txn type.
        
        :param txn_type -> `str`: the type of txn to perform, as specified by args.buy or args.sell.
        """

        algorand_in_usd = asyncio.run(get_algorand_price())
        NavStrategy = NetAssetValue("https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail?slug=")
        nav_in_usd = NavStrategy.calculate()
        
        count_algos_needed_for_one_etf_token = nav_in_usd / algorand_in_usd # the number of Algos needed to buy one ETF token
        total_algos_to_be_transferred = count_algos_needed_for_one_etf_token * self.amount

        assert all(txn_type in ('buy', 'sell', 'exchange') for txn_type in args)
        txns = []

        for txn_type in args:
            if txn_type == 'exchange':
                txns.append(Exchange(self).build(total_algos_to_be_transferred))
            elif txn_type == 'buy':
                txns.append(Buy(self).build())
            elif txn_type == 'sell':
                txns.append(Sell(self).build())
        
        
        self.send_txns(txns)

class Buy(Transaction):
    def __init__(self, transaction: Transaction):
        self.transaction = transaction

    def build(self) -> None:
        """
        Creates an unsigned transfer transaction that is then sent off for signing
        and submission to the blockchain via the `sign_and_send` utility function.

        The transaction is submitted for the specified `asset_id` to the specified address
        for the specified amount.

        :return -> ``None``:
        """

        amount_to_buy = self.transaction.amount # amount of etf coin to buy

        transfer_data = {
            "sender": self.transaction.sender,
            "receiver": self.transaction.receiver_address,
            "amt": amount_to_buy,
            "index": asset_id,
        }

        transaction = self.build_txn(AssetTransferTxn, **transfer_data)
        return transaction


class Sell(Buy):
    def __init__(self, transaction: Transaction):
        super().__init__(transaction)

class Exchange(Sell):
    def __init__(self, transaction: Transaction):
        """
        what do I need to allow someone to exchange the token????
        """
        super().__init__(transaction)
    
    def build(self, amount_of_transferred_algos: float or int):
        """
        exchange algos for the token (from buyer -> seller if Sell(), seller -> buyer if Buy())

        :param amount_of_transferred_algos -> ``float`` or ``int``: the amount of algos to be transferred.
        """

        formatted_algo_amt = round(convert_algos_to_microalgo(amount_of_transferred_algos))

        payment_data = {
            "sender": self.transaction.receiver_address, # the person receiving the token must liquidate algos
            "receiver": self.transaction.sender, # the person sending the token to another receives algos in return
            "amt": formatted_algo_amt, # amount of algos to exchange for the etf coin.
        }
        
        transaction = self.build_txn(PaymentTxn, **payment_data)

        return transaction