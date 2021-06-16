import re
from typing import List

def clean_acct_names(user_dotfile: str) -> List[str]:
    """
    clean all account names and return them
    
    :param user_dotfile -> ``str``: path to users `.pos_etf` dotfile
    """
    all_acct_names = filter(
        re.compile(
            r"^\[[a-zA-Z0-9]").search, open(user_dotfile).readlines()
    )

    def formatted_acct_names(acct_names): return [
        name.strip("[]\n") for name in acct_names
    ]

    list_of_formatted_acct_names = formatted_acct_names(all_acct_names)

    return list_of_formatted_acct_names

def extract_matching_pub_key(acct_name: str, dotfile_contents: List[str]):
    """
    extract public key that matches `acct_name`.

    :param acct_name -> ``str``: the name of the account
    """
    index_of_acct_name = dotfile_contents.index(acct_name)
    index_of_pub_key = index_of_acct_name + 1
    
    messy_pub_key = dotfile_contents[index_of_pub_key]

    clean_pub_key = messy_pub_key.split(" = ")[-1]
    return clean_pub_key

def extract_matching_priv_key(acct_name: str, dotfile_contents: List[str]):
    """
    extract private key that matches `acct_name`.

    :param acct_name -> ``str``: the name of the account
    """
    index_of_acct_name = dotfile_contents.index(acct_name)
    index_of_priv_key = index_of_acct_name + 2

    messy_priv_key = dotfile_contents[index_of_priv_key]

    clean_priv_key = messy_priv_key.split(" = ")[-1]
    return clean_priv_key

