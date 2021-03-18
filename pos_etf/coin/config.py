creator_address = ""
creator_passphrase = \
    ""

receiver_address = ""
receiver_passphrase = \
    ""

asset_details = {
    "sender": creator_address,
    "asset_name": "PosETF",
    "unit_name": "Pos",
    "manager": creator_address,
    "reserve": creator_address,
    "freeze": creator_address,
    "clawback": creator_address,
    "total": 10000000000,
    "decimals": 0,
    "default_frozen": False,
    # "url": "METADATA IMAGE", # https://developer.algorand.org/tutorials/create-dogcoin/#1-generate-the-dogcoin-creator-and-receiver-accounts
    "metadata_hash": b"\xe3\xb0\xc4B\x98\xfc\x1c\x14\x9a\xfb\xf4\xc8\x99o\xb9$'\xaeA\xe4d\x9b\x93L\xa4\x95\x99\x1bxR\xb8U", # bytes hash of url
}