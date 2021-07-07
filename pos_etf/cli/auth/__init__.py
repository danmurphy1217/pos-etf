from typing import Optional, Dict
import argparse
import pathlib
import os
import requests
from urllib.parse import urlencode
import re

from cli.utils import clean_acct_names
from cli.error import AccountNameError, AddressError

class Auth(object):

    def __init__(self, linked_wallet_address: str, linked_private_key: str, account_name: str, user_dotfile: pathlib.Path, base_url: str):
        self.linked_wallet_address: str = linked_wallet_address
        self.linked_private_key = linked_private_key
        self.user_dotfile = user_dotfile
        self.base_url: str = base_url
        self.account_name = account_name

    def _request(self, endpoint: str, params: Dict[str, str]):
        """Private method for sending off-chain requests."""

        stringified_params = "?" + urlencode(params)
        response = requests.get(self.base_url + endpoint + stringified_params)
        response.raise_for_status()
        return response.json()

    def _write(self, mode: str = 'w'):
        """
        Write account information to `self.user_dotfile`.
        
        :param mode -> ``str``: the mode for writing to the file (should be `w` or `a`)
        """
        with open(self.user_dotfile, mode) as f:
            f.writelines([
                f"[{self.account_name}]\n",
                f"addr = {self.linked_wallet_address}\n",
                f"pk = {self.linked_private_key}\n"
            ])
        f.close()

        return f"{self.account_name} successfully created."

    def _make_dotfile(self):
        """Create .pos_etf dotfile on users computer."""
        try:
            os.makedirs(os.path.dirname(self.user_dotfile))
        except Exception as e:
            print("Error creating dotfile. See traceback:")
            print(e)

    def verify(self, auth_type: str):
        """Verify the provided wallet address."""

        if os.path.exists(self.user_dotfile):

            if auth_type == "signup":
                try:

                    self._request(
                        endpoint="/idx2/v2/transactions",
                        params={"address": self.linked_wallet_address}
                    )

                    self._write(mode='a')

                    os.environ['ALGOETF_PROFILE'] = self.account_name
                except requests.exceptions.HTTPError as e:
                    raise AddressError(
                        f"Address {self.linked_wallet_address} is invalid.")
            else:

                list_of_formatted_acct_names = clean_acct_names(self.user_dotfile)

                if self.account_name in list_of_formatted_acct_names:
                    os.environ['ALGOETF_PROFILE'] = self.account_name
                    return True
                else:
                    raise AccountNameError(
                        f"{self.account_name} does not exist. Run `algoetf --signup to begin.`")

        else:
            try:

                self._request(
                    endpoint="/idx2/v2/transactions",
                    params={"address": self.linked_wallet_address}
                )

                self._make_dotfile()

                print(self._write())
                os.environ['ALGOETF_PROFILE'] = self.account_name

            except requests.exceptions.HTTPError as e:
                raise AddressError(
                    f"Address {self.linked_wallet_address} is invalid.")
