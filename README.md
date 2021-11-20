# How to use
## blockchain.py
- create a Blockchain object
- create new transactions for each block `.add_transaction("Satoshi", "Mike", '5 BTC')`
and finish that block with `.add_block(num)` with `num` is random number
- use `.print()` to print out the blockchain

## blockchain_pow.py
- create a Blockchain object
- for each transaction, we create an instance of Transaction object, then sign the transaction
with `.sign_transaction()`. Then we can add it to the block using `blockchain.add_transaction()`
- After adding and signing all transactions, we need to calculate and add the block using `.add_block()`
- To print the blockchain, use `.print()`
- To check validity of the blockchain, use `.check_chain_validity()`
