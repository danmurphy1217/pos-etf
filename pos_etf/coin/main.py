from config import *
from algosdk import algod
from algosdk.transaction import AssetConfigTxn
from algosdk.transaction import write_to_file

client = algod.AlgodClient("5fd254f3dd0638175d7cc386b87ac97fe54bf4cf462e09e9c8864b48fa7e185a", "http://127.0.0.1:8080")

print(client.status().get('lastRound'))

def create():
    """
    creates the asset that is defined in `config.py`, signs it, and sends it
    to the algorand network if the senders passphrase is supplied. Otherwise,
    the transaction is written to a file.
    """