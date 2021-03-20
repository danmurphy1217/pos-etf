# pos_etf/coin Overview

## config.py
This file contains three things:

1. **Asset ID**: This value should be set to the ID of the created asset. The Asset ID is used in transactions to determine which asset is being sent from owner to receiver, and it is also used to easily tell how much of what asset a wallet contains.
2. **Creator and Receiver Address/Passphrase**: Test accounts used for basic transactions, opting into receiving the asset, etc...
3. **Asset Details**: these are the details that define the asset. You can define the asset name, unit name, the total number of coins that can be in circulation, and more.

## util.py
This file contains a variety of utility functions that help create the asset, opt in users, and sign and send transactions:

1. `generate_new_account`: generate a new algorand account and return the address, private key, and passphrase
2. `add_network_params`: add network parameters to the transaction data that is passed to the function. The passed transaction data is dynamic, while these parameters should be constant or derived by a function each time it is called.
3. `file_to_hash`: reads the byte representation of a file, return the sha256 representation of the bytes if the return_type is bytes.
4. `wait_for_confirmation`: while the transaction is not confirmed by the network, increment the round and update the block status. if round exists and its value is > 0, return the transaction information.
5. `sign_and_send`: signs a transaction and sends it to the network. First, we retrieve the private key from an accounts passphrase. Then, we use the private key to sign the transaction abd use the signed transaction to retrieve the transaction ID. Finally, we send a transaction to the network with the signed transaction, wait for confirmation, and return the transaction information.
6. `balance_formatter`: format an amount of units for an asset.

## main.py
This file contains functions that create the actual asset and sign and send transactions to the algorand blockchain:

1. `generate_accounts`: generate two new accounts, useful for generating a **creator** and **receiver** for testing purposes of opting in and receiver/transferring assets.
2. `get_api_token`: async function that retrieves the API token from the algorand node (test net or data, depending on the scenario).
3. `get_network_info`: async function that retrieves the network info (url/port) from the algorand node (test net or data, depending on the scenario)
4. `create`: creates the asset, uses `passphrase` to retrieve the users private key and sign the transaction.
5. `opt_in`: opts in a user to receive and store/transfer the asset. 
6. `check_holdings`: check the balance for an asset in the specified wallet address
7. `transfer`: transfer the asset from the creator to the receiver. Currently, these values are static but the end goal would be purchase the coin from the creators wallet and send it to the receivers where it could appreciate.



