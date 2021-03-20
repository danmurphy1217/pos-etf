# pos_etf/coin Overview

## config.py
This file contains three things:

1. **Asset ID**: This value should be set to the ID of the created asset. The Asset ID is used in transactions to determine which asset is being sent from owner to receiver, and it is also used to easily tell how much of what asset a wallet contains.
2. **Creator and Receiver Address/Passphrase**: Test accounts used for basic transactions, opting into receiving the asset, etc...
3. **Asset Details**: these are the details that define the asset. You can define the asset name, unit name, the total number of coins that can be in circulation, and more.

## util.py
This file contains a variety of utility functions that help create the asset, opt in users, and sign and send transactions:

1. `generate_new_account`:
2. `add_network_params`:
3. `file_to_hash`:
4. `wait_for_confirmation`:
5. `sign_and_send`:
6. `balance_formatter`:

## main.py
This file contains functions that create the actual asset and sign and send transactions to the algorand blockchain:

1. `generate_accounts`:
2. `get_api_token`:
3. `get_network_info`:
4. `create`:
5. `opt_in`:
6. `check_holdings`:
7. `transfer`:

