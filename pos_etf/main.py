import argparse
from PyInquirer import prompt
import os
import sys
import signal
from pathlib import Path

from cli.auth import Auth

def init_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """
    instantiate the parser object with necessary arguments.

    :param parser -> ``argparse.ArgumentParser``: a parser object with no arguments added.

    :returns parser -> ``argparse.ArgumentParser``: a parser object containing the needed arguments.    
    """
    parser.add_argument(
        "--signup",
        type=str,
        nargs="?",
        help="""Create an account. Credentials are stored in $HOME/.pos_etf"""
    )

    parser.add_argument(
        "--login",
        type=str,
        nargs="?",
        help="""
                Sign into your account. Credentials must match those associated 
                with your profile name in $HOME/.pos_etf
            """
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


def main():
    base_parser = argparse.ArgumentParser(
        description="CLI for buying and selling the POS_ETF Coin. Proudly built on the Algorand blockchain.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser = init_parser(base_parser)

    args = parser.parse_args()

    user_home_dir = str(Path.home())  # same as os.path.expanduser("~")
    equit_ease_dir = os.path.join(user_home_dir, ".pos_etf")
    credentials_file_path = Path(os.path.join(equit_ease_dir, "credentials"))

    print(args)
    Auth("1234", "privst key", credentials_file_path, "My First Johnson").verify()


if __name__ == '__main__':
    main()
