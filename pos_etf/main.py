import argparse
from PyInquirer import prompt
import os
from pathlib import Path
from typing import Optional, Dict
import json

from cli.auth import Auth
from cli.utils import extract_matching_pub_key, extract_matching_passphrase, clean_acct_names
from cli.error import DuplicateAcctNameError
from cli.transaction import Transaction
from cli.utils.constants import algoetf_addr

user_home_dir = str(Path.home())  # same as os.path.expanduser("~")
equit_ease_dir = os.path.join(user_home_dir, ".pos_etf")
credentials_file_path = Path(os.path.join(equit_ease_dir, "credentials"))
default_file_path = Path(os.path.join(equit_ease_dir, "default.json"))


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
        help="""Valid options are 'login' or 'signup'. If 'login', log into an already-existent address. If 'signup', sign up for an account."""
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
        nargs=1,
        help="""View Your POS_ETF holdings."""
    )

    return parser


def handle_auth_flow(auth_type: str):
    """handle login/signup flow for user."""

    addr_and_key_questions = [
        {"type": "password", "name": "public_key", "message": "passphrase:"},
        {
            "type": "password",
            "name": "private_key",
            "message": "private key:",
        },
    ]

    def acct_name_question(default_val: Optional[str] = None, extras: Dict[str, str] = {}):
        init_dict = {
            "type": "input",
            "name": "acct_name",
            "message": f"account name: {default_val}"
        }
        init_dict.update(extras)
        return init_dict

    if auth_type == "signup":
        auth_results = prompt(addr_and_key_questions)
        customized_acct_question = acct_name_question(
            f"[{auth_results['public_key']}]")
        name_for_acct = prompt(customized_acct_question)

    elif auth_type == "login":
        auth_results = dict()
        cleaned_acct_names = clean_acct_names(credentials_file_path)

        customized_acct_question = acct_name_question(
            extras={
                "type": "list",
                "choices": cleaned_acct_names
            }
        )
        name_for_acct = prompt(customized_acct_question)

    acct_name_results = name_for_acct.get("acct_name", '')
    auth_results["acct_name"] = acct_name_results if acct_name_results != '' else auth_results.get(
        'public_key')

    if auth_type == "signup" and auth_results["acct_name"] in clean_acct_names(credentials_file_path):
        raise DuplicateAcctNameError(
            "Account name {} already exists. Account names must be unique.".format(auth_results["acct_name"]))

    return auth_results


def get_default_account():
    """read in the default account name from ~/.pos_etf/default.json"""
    try:
        default_file_content = open(default_file_path, "r")
        jsonified_default_file_content = json.load(default_file_content)
        default_acct_name = jsonified_default_file_content['account_name']
        return default_acct_name

    except FileNotFoundError:
        raise FileNotFoundError("default.json does not exist yet")


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
        priv_key = auth_results.get('passphrase') if auth_type == "signup" else extract_matching_passphrase(
            auth_results['acct_name'], [line.strip("[]\n") for line in open(credentials_file_path).readlines()])

        if auth_type == "login":
            os.environ['ALGOETF_PROFILE'] = auth_results['acct_name']
        else:
            get_default_account()

        auth = Auth(
            pub_key,
            priv_key,
            auth_results['acct_name'],
            credentials_file_path,
            "https://testnet.algoexplorerapi.io",
        )

        print(auth.verify(auth_type))

        # Auth("MXIGC5RCUFNFV2TB7ODAGQ4H7VC75DCH2SBBG7ATWPLB4YHBO7FFPNVLJ4", "privst key", credentials_file_path,
        #      "https://testnet.algoexplorerapi.io", arg_namespace=args).verify()

    else:

        if args.buy:

            if not os.environ.get("ALGOETF_PROFILE"):
                default_account_name = get_default_account()

            else:
                default_account_name = os.environ.get("ALGOETF_PROFILE")

            
            print(default_account_name)
            # client = algod.AlgodClient(asyncio.run(get_api_token(
            #     ALGORAND_MAIN_NET_DATA_DIR)), asyncio.run(get_network_info(ALGORAND_MAIN_NET_DATA_DIR)))

            # txn = Transaction(client, algoetf_addr,)

            print("Buying TXN")
        elif args.sell:

            if not os.environ.get("ALGOETF_PROFILE"):
                default_account_name = get_default_account()

            else:
                default_account_name = os.environ.get("ALGOETF_PROFILE")

            print(default_account_name)
            print("SELLING TXN")


if __name__ == '__main__':
    main()
