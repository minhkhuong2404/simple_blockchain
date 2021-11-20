import json
import time
from hashlib import sha256


class Transaction:
    def __init__(self, from_address, to_address, amount):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.time = time.time()
        self.signature = ''

    def print(self):
        return 'from {0} -> to {1} : {2} BTC at {3} \t\t'.format(self.from_address, self.to_address, self.amount, self.time)

    def compute_hash(self):
        block_string = json.dumps(self.from_address + self.to_address + self.amount + str(self.time), sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

    def sign_transaction(self):
        self.signature = self.compute_hash()

    def is_valid(self):
        # mining reward
        if self.from_address == '':
            return True
        # no signature
        if self.signature == '':
            return False
        return self.signature == self.compute_hash()


class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.nonce = nonce
        self.hash = "0"
        self.transactions = transactions
        self.timestamp = time.time()
        self.previous_hash = previous_hash

    def print_transaction(self):
        transaction_str = ''
        for transaction in self.transactions:
            transaction_str += transaction.print()
        return transaction_str

    def compute_hash(self):
        block_string = json.dumps(str(self.hash) + str(self.previous_hash) + self.print_transaction(), sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

    def proof_of_work(self):
        self.nonce = 0

        while not self.hash.startswith('0' * Blockchain.difficulty):
            self.nonce += 1
            self.hash = self.compute_hash()
        return self.hash

    def has_valid_transaction(self):
        for transaction in self.transactions:
            if not transaction.is_valid():
                return False
        return True


class Blockchain(object):
    difficulty = 4  # class attribute

    def __init__(self):
        self.pending_transactions = []  # instance attribute
        self.chain = []
        self.add_genesis_block()

    def print(self):
        for chain in self.chain:
            print("""
                'hash': {0}
                'index': {1}
                'previous_hash': {2}
                'nonce': {3}
                'timestamp': {4}
                'transactions': {5}
            """.format(chain.hash, chain.index, chain.previous_hash,
                       chain.nonce, chain.timestamp, chain.print_transaction()))

    def add_genesis_block(self):
        """
                A function to generate genesis block and appends it to
                the chain. The block has index 0, previous_hash as 0, and
                a valid hash.
                """
        genesis_block = Block(0, [], "0")
        genesis_block.proof_of_work()
        self.chain.append(genesis_block)
        self.pending_transactions = []

    def new_block(self, block, proof):
        previous_hash = self.get_last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not Blockchain.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    @property
    def get_last_block(self):
        return self.chain[-1]

    def new_transaction(self, transaction):
        if not transaction.from_address or not transaction.to_address:
            return False
        if not transaction.is_valid() and not float(transaction.amount) < 0:
            return False
        self.pending_transactions.append(transaction)

    def mine(self):
        if not self.pending_transactions:
            return False

        last_block = self.get_last_block

        new_block = Block(
            last_block.index + 1,
            self.pending_transactions,
            last_block.hash
        )

        proof = new_block.proof_of_work()
        self.new_block(new_block, proof)

        self.pending_transactions = []
        return True

    @classmethod
    def is_valid_proof(cls, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.proof_of_work())

    def check_chain_validity(self):
        result = True
        previous_hash = "0"

        for block in self.chain:
            block_hash = block.hash

            if not self.is_valid_proof(block, block_hash) or \
                    previous_hash != block.previous_hash or \
                    not block.has_valid_transaction():
                result = False
                break

            block.hash, previous_hash = block_hash, block_hash

        return result


blockchain = Blockchain()

t1 = Transaction("Satoshi", "Mike", '5')
t1.sign_transaction()
blockchain.new_transaction(t1)
t2 = Transaction("Mike", "Satoshi", '1')
t2.sign_transaction()
blockchain.new_transaction(t2)
t3 = Transaction("Satoshi", "Hal Finney", '5')
t3.sign_transaction()
blockchain.new_transaction(t3)
blockchain.mine()

t4 = Transaction("Mike", "Alice", '1')
t4.sign_transaction()
blockchain.new_transaction(t4)
t5 = Transaction("Alice", "Bob", '0.5')
t5.sign_transaction()
blockchain.new_transaction(t5)
blockchain.mine()

t6 = Transaction("Vine", "Mark", '0.01')
t6.sign_transaction()
blockchain.new_transaction(t6)
blockchain.mine()

print("My blockchain: ")
blockchain.print()
print("Blockchain's validity :")
print(blockchain.check_chain_validity())

blockchain.chain[1].transactions[0] = Transaction("A", "B", "100")
blockchain.print()

print("Blockchain's validity :")
print(blockchain.check_chain_validity())
