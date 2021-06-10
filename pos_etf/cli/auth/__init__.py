from typing import Optional, Dict
import pathlib
import os
import requests
from urllib.parse import urlencode
import re

"""
Signup flow is to create a profile name, provide wallet address and private key.

I then need to verify that this are correct prior to writing to any files or passing 
onto the next step in the process.

For reusability, I should first check to see if profile name exists in the dotfile,
Then if it does not I can ping and verify with algorand. If it does, I can assume that
it was alraedy verified by me during the sign up process.
"""


class AddressError(Exception):

    def __init__(self, message: str):
        Exception.__init__(self, message)


class AccountNameError(Exception):

    def __init__(self, message: str = "Provided Account Name does not exist. Run `algoetf --signup` to begin."):
        self.message = message
        super().__init__(message)


class Auth(object):

    def __init__(self, linked_wallet_address: str, linked_private_key: str, user_dotfile: pathlib.Path, base_url: str, account_name: Optional[str] = None):
        self.linked_wallet_address: str = linked_wallet_address
        self.linked_private_key = linked_private_key
        self.user_dotfile = user_dotfile
        self.base_url: str = base_url
        self.account_name: Optional[str] = account_name if account_name is not None else linked_wallet_address

    def _request(self, endpoint: str, params: Dict[str, str]):
        """Private method for sending off-chain requests."""

        stringified_params = "?" + urlencode(params)
        response = requests.get(self.base_url + endpoint + stringified_params)
        response.raise_for_status()
        return response.json()

    def _write(self):
        """Write account information to `self.user_dotfile`."""
        with open(self.user_dotfile, "w") as f:
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

    def verify(self):
        """Verify the provided wallet address."""

        if os.path.exists(self.user_dotfile):

            all_acct_names = filter(
                re.compile(
                    r"^\[[a-zA-Z0-9]").search, open(self.user_dotfile).readlines()
            )

            def formatted_acct_names(acct_names): return [
                name.strip("[]\n") for name in acct_names
            ]

            list_of_formatted_acct_names = formatted_acct_names(all_acct_names)

            if self.account_name in list_of_formatted_acct_names:
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
            except requests.exceptions.HTTPError as e:
                raise AddressError(
                    f"Address {self.linked_wallet_address} is invalid.")

            # print("I need to verify with algorand and then write to file.")
