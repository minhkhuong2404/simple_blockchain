import json
import time
from hashlib import sha256


class Block:
    def __init__(self, index, nonce, transactions, timestamp, previous_hash):
        self.index = index
        self.hash = self.compute_hash()
        self.nonce = nonce
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain(object):
    def __init__(self):
        self.difficulty = 2
        self.pending_transactions = []
        self.chain = []
        self.add_genesis_block()

    def print(self):
        for chain in self.chain:
            print("""
            'hash': {0},
            'index': {1},
            'previous_hash': {2},
            'nonce': {3},
            'timestamp': {4},
            'transactions': {5},
            """.format(chain.hash, chain.index, chain.previous_hash,
                       chain.nonce, chain.timestamp, chain.transactions))

    def add_genesis_block(self):
        self.chain.append(
            Block(0, 100, [], time.time(), previous_hash="0"))

    def add_block(self, proof):
        block = Block(
            len(self.chain),
            proof,
            self.pending_transactions,
            time.time(),
            self.get_previous_hash()
        )
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def get_previous_hash(self):
        return self.chain[len(self.chain) - 1].hash

    def add_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.pending_transactions.append(transaction)


blockchain = Blockchain()

blockchain.add_transaction("Satoshi", "Mike", '5 BTC')
blockchain.add_transaction("Mike", "Satoshi", '1 BTC')
blockchain.add_transaction("Satoshi", "Hal Finney", '5 BTC')
blockchain.add_block(12345)

blockchain.add_transaction("Mike", "Alice", '1 BTC')
blockchain.add_transaction("Alice", "Bob", '0.5 BTC')
blockchain.add_transaction("Bob", "Mike", '0.5 BTC')
blockchain.add_block(6789)

blockchain.add_block(12350)

print("My blockchain: ")
blockchain.print()
