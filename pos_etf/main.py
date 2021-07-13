import argparse
from PyInquirer import prompt
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
import asyncio
from algosdk.v2client import algod

from cli.auth import Auth
from cli.utils import extract_matching_pub_key, extract_matching_passphrase, clean_acct_names, send_request_to
from cli.utils.constants import algoetf_addr, creator_passphrase, asset_id
from cli.error import DuplicateAcctNameError, NoSpecifiedAccountError, InvalidAuthArgError
from cli.transaction import Transaction

user_home_dir = str(Path.home())  # same as os.path.expanduser("~")
pos_etf_dir = os.path.join(user_home_dir, ".pos_etf")
credentials_file_path = Path(os.path.join(pos_etf_dir, "credentials"))
default_file_path = Path(os.path.join(pos_etf_dir, "default.json"))


# DONE: on buy, Algos must be transferred from receiver -> sender in exchange for POS coin sent from sender -> receiver (and the Algos should be converted to underlying holdings of POS coin 1x per day).
# DONE: on sell, Algos are sent from the receiver (the algoetf addr) to the sender and the sender sends the receiver POS coin (which should be converted to underlying holdings of POS coin 1x per day).
#DONE: calculate NAV of the ETF when someone buys or sells, use the NAV to determine how many Algos must be sent for the exchange

#TODO: After determining how many Algos are sent, determine how to calculate the % of the underlying assets that must be bought with the Algos/transfer algos to USDC

def init_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """
    instantiate the parser object with necessary arguments.

    :param parser -> ``argparse.ArgumentParser``: a parser object with no arguments added.

    :returns parser -> ``argparse.ArgumentParser``: a parser object containing the needed arguments.    
    """
    parser.add_argument(
        "auth",
        type=str,
        nargs="?",
        help="""Valid option is signup'. If 'signup', sign up for an account."""
    )

    parser.add_argument(
        "--buy",
        type=str,
        nargs=1,
        help="""Purchase POS_ETF."""
    )

    parser.add_argument(
        "--sell",
        type=str,
        nargs=1,
        help="""Sell POS_ETF."""
    )

    parser.add_argument(
        "--view",
        type=str,
        nargs="?",
        const="None",
        help="""View Your POS_ETF holdings."""
    )

    parser.add_argument(
        "--account",
        type=str,
        nargs=1,
        help="""View Your POS_ETF holdings."""
    )

    return parser

def acct_name_question(default_val: Optional[str] = None, extras: Dict[str, str] = {}):
    init_dict = {
        "type": "input",
        "name": "acct_name",
        "message": f"account name: {default_val}"
    }
    init_dict.update(extras)
    return init_dict

def handle_auth_flow(auth_type: str):
    """handle signup flow for user."""
    if not os.path.exists(pos_etf_dir):
        os.makedirs(pos_etf_dir)
        credentials_file_path.touch()
        default_file_path.touch()

    addr_and_key_questions = [
        {"type": "password", "name": "public_key", "message": "address:"},
        {
            "type": "password",
            "name": "passphrase",
            "message": "passphrase:",
        },
    ]

    if auth_type != 'signup':
        raise InvalidAuthArgError("Invalid authorization value provided. Currently, `signup` is the only value accepted.")

    if auth_type == "signup":
        auth_results = prompt(addr_and_key_questions)
        customized_acct_question = acct_name_question(
            f"[{auth_results['public_key']}]")
        name_for_acct = prompt(customized_acct_question)

    acct_name_results = name_for_acct.get("acct_name", '')
    auth_results["acct_name"] = acct_name_results if acct_name_results != '' else auth_results.get(
        'public_key')

    if auth_type == "signup" and auth_results["acct_name"] in clean_acct_names(credentials_file_path):
        raise DuplicateAcctNameError(
            "Account name {} already exists. Account names must be unique.".format(auth_results["acct_name"]))

    return auth_results

def do_txn(args: Dict[str, Any], default_account_name: str):
    """Build and send transaction"""
    client = algod.AlgodClient(
        "", "https://testnet.algoexplorerapi.io", headers={'User-Agent': 'DanM'})

    pub_key = extract_matching_pub_key(default_account_name, [line.strip(
        "[]\n") for line in open(credentials_file_path).readlines()])
    passphrase = extract_matching_passphrase(default_account_name, [line.strip(
        "[]\n") for line in open(credentials_file_path).readlines()])

    txn = Transaction(client, algoetf_addr, pub_key,
                        creator_passphrase, int(args.buy[0]))
    print(txn.buy())

def display_txn_info(sending_addr: str, receiver_addr: str, amount: int) -> None:
    """display transaction info"""

    sending_addr = sending_addr + " (Wallet Address that holds the pool of POS Coins)" if sending_addr == algoetf_addr else sending_addr

    print("\nTXN INFORMATION:\n")
    print(f"- Sending Address: {sending_addr}")
    print(f"- Receiver Address: {receiver_addr}")
    print(f"- Amount: {amount}\n\n")

    input("If this information is correct, press enter. Otherwise, cancel your request.")

def main():
    base_parser = argparse.ArgumentParser(
        description="CLI for buying and selling the POS_ETF Coin. Proudly built on the Algorand blockchain.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser = init_parser(base_parser)

    args = parser.parse_args()

    auth_type = args.auth

    if auth_type:

        auth_results = handle_auth_flow(auth_type)

        pub_key = auth_results.get('public_key') if auth_type == "signup" else extract_matching_pub_key(
            auth_results['acct_name'], [line.strip("[]\n") for line in open(credentials_file_path).readlines()])
        passphrase = auth_results.get('passphrase') if auth_type == "signup" else extract_matching_passphrase(
            auth_results['acct_name'], [line.strip("[]\n") for line in open(credentials_file_path).readlines()])


        auth = Auth(
            pub_key,
            passphrase,
            auth_results['acct_name'],
            credentials_file_path,
            "https://testnet.algoexplorerapi.io",
        )

        auth.verify(auth_type)

    else:

        if args.buy:

            if not (os.environ.get("ALGOETF_PROFILE") or args.account):
                raise NoSpecifiedAccountError("No account was specified for this request. To specify an account, either include the `--account '[account_name]'` flag in the command line or set an env variable for the ALGOETF_PROFILE key.")


            default_account_name = args.account[0] if args.account else os.environ.get("ALGOETF_PROFILE")

            client = algod.AlgodClient(
                "", "https://testnet.algoexplorerapi.io", headers={'User-Agent': 'DanM'})

            pub_key = extract_matching_pub_key(default_account_name, [line.strip(
                "[]\n") for line in open(credentials_file_path).readlines()])
            passphrase = extract_matching_passphrase(default_account_name, [line.strip(
                "[]\n") for line in open(credentials_file_path).readlines()])


            display_txn_info(sending_addr=algoetf_addr, receiver_addr=pub_key, amount=int(args.buy[0]))

            txn = Transaction(client, algoetf_addr, pub_key, buy_or_sell_passphrase=creator_passphrase, algo_exchange_passphrase=passphrase, amount=int(args.buy[0]))
            txn.do("buy", "exchange")

        elif args.sell:

            if not (os.environ.get("ALGOETF_PROFILE") or args.account):
                raise NoSpecifiedAccountError("No account was specified for this request. To specify an account, either include the `--account '[account_name]'` flag in the command line or set an env variable for the ALGOETF_PROFILE key.")

            
            default_account_name = args.account[0] if args.account else os.environ.get("ALGOETF_PROFILE")
            
            client = algod.AlgodClient(
                "", "https://testnet.algoexplorerapi.io", headers={'User-Agent': 'DanM'})

            pub_key = extract_matching_pub_key(default_account_name, [line.strip(
                "[]\n") for line in open(credentials_file_path).readlines()])
            buy_or_sell_passphrase = extract_matching_passphrase(default_account_name, [line.strip(
                "[]\n") for line in open(credentials_file_path).readlines()])
            
            display_txn_info(sending_addr=pub_key, receiver_addr=algoetf_addr, amount=int(args.sell[0]))

            txn = Transaction(client, sender=pub_key, receiver_address=algoetf_addr, buy_or_sell_passphrase=buy_or_sell_passphrase, algo_exchange_passphrase=creator_passphrase, amount=int(args.sell[0]))
            txn.do("sell", "exchange")
        
        elif args.view:

            if args.view == 'None':

                if not (os.environ.get('ALGOETF_PROFILE', None)):
                    cleaned_acct_names = clean_acct_names(credentials_file_path)

                    customized_acct_question = acct_name_question(
                        extras={
                            "type": "list",
                            "choices": cleaned_acct_names
                        }
                    )
                    name_for_acct = prompt(customized_acct_question)['acct_name']
                
                else:
                    name_for_acct = os.environ.get('ALGOETF_PROFILE')

                pub_key = extract_matching_pub_key(name_for_acct, [
                    line.strip("[]\n") for line in open(credentials_file_path).readlines()
                ])
                # https://testnet.algoexplorerapi.io/v2/accounts/{pubkey}
                json_res = asyncio.run(send_request_to(f"https://testnet.algoexplorerapi.io/v2/accounts/{pub_key}", "GET"))
                list_of_assets = json_res['assets']
                info_for_etf_asset_id = [asset for asset in list_of_assets if asset['asset-id'] == asset_id]
                print(info_for_etf_asset_id[0]['amount'])
            else:
                print("Use provided name and retrieve info for that account")


if __name__ == '__main__':
    main()
