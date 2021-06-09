from typing import Optional
import pathlib
import os

"""
Signup flow is to create a profile name, provide wallet address and private key.

I then need to verify that this are correct prior to writing to any files or passing 
onto the next step in the process.

For reusability, I should first check to see if profile name exists in the dotfile,
Then if it does not I can ping and verify with algorand. If it does, I can assume that
it was alraedy verified by me during the sign up process.
"""


class Auth(object):

    def __init__(self, linked_wallet_address: str, linked_private_key: str, user_dotfile: pathlib.Path, account_name: Optional[str] = None):
        self.linked_wallet_address: str = linked_wallet_address
        self.linked_private_key = linked_private_key
        self.user_dotfile = user_dotfile
        self.account_name: Optional[str] = account_name if account_name is not None else linked_wallet_address

    def _request(self):
        """Private method for sending off-chain requests."""

    def verify(self):
        """Verify the provided wallet address."""

        if os.path.exists(self.user_dotfile):
            print("Check profile names")
            print(
                "If profile name exists good to go, if not then ping algorand and then write to file")
        else:
            os.path.touch()
            print("I need to verify with algorand and then write to file.")
