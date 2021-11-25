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
        return 'from {0} -> to {1} : {2} BTC at {3} \t'.format(self.from_address,
                                                               self.to_address, self.amount, self.time)

    def compute_hash(self):
        block_string = json.dumps(self.from_address + self.to_address + str(self.amount) + str(self.time), sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

    def sign_transaction(self):
        self.signature = self.compute_hash()

    def is_valid(self):
        # print(self.signature)
        # print(self.compute_hash())
        # mining reward
        if self.from_address == '':
            return True
        # no signature
        if self.signature == '':
            return False
        return self.signature == self.compute_hash()


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0, block_hash="0"):
        self.index = index
        self.nonce = nonce
        self.block_hash = block_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash

    def print_transaction(self):
        transaction_str = ''

        for transaction in self.transactions:
            if type(transaction) == str:
                transaction_str += transaction
            else:
                transaction_str += transaction.print()
        return transaction_str

    def compute_hash(self):
        block_string = json.dumps(str(self.index) + str(self.nonce)
                                  + self.previous_hash
                                  + str(self.timestamp) + self.print_transaction(), sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

    def has_valid_transaction(self, transactions_str=''):
        if transactions_str != '' and type(self.transactions) == str:
            return transactions_str == self.transactions

        for transaction in self.transactions:
            if not transaction.is_valid():
                return False
        return True

    def get_block(self):
        return dict({
            'index': self.index,
            'block_hash': self.block_hash,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'timestamp': self.timestamp,
            'transactions': self.print_transaction()
        })


class Blockchain(object):
    difficulty = 2  # class attribute

    def __init__(self):
        self.pending_transactions = []  # instance attribute
        self.chain = []

    def print(self):
        for chain in self.chain:
            print("""
                'block_hash': {0}
                'index': {1}
                'previous_hash': {2}
                'nonce': {3}
                'timestamp': {4}
                'transactions': {5}
            """.format(chain.block_hash, chain.index, chain.previous_hash,
                       chain.nonce, chain.timestamp, chain.print_transaction()))

    def add_genesis_block(self):
        """
                A function to generate genesis block and appends it to
                the chain. The block has index 0, previous_hash as 0, and
                a valid hash.
                """
        genesis_block = Block(0, [], 0, "0")
        genesis_block.block_hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
        self.pending_transactions = []

    def new_block(self, block_new, proof_new):
        previous_hash = self.get_last_block.block_hash
        if previous_hash != block_new.previous_hash:
            return False

        if not Blockchain.is_valid_proof(block_new, proof_new):
            return False

        block_new.block_hash = proof_new
        self.chain.append(block_new)
        return True

    @property
    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        if not transaction.from_address or not transaction.to_address:
            return False
        if not transaction.is_valid() or float(transaction.amount) < 0:
            return False
        self.pending_transactions.append(transaction)

    def add_block(self):
        if not self.pending_transactions:
            return False

        last_block = self.get_last_block

        add_new_block = Block(
            last_block.index + 1,
            self.pending_transactions,
            time.time(),
            last_block.block_hash
        )

        p_o_w = self.proof_of_work(add_new_block)
        self.new_block(add_new_block, p_o_w)

        self.pending_transactions = []
        return True

    @staticmethod
    def proof_of_work(block_pow):
        block_pow.nonce = 0
        computed_hash = block_pow.compute_hash()

        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block_pow.nonce += 1
            computed_hash = block_pow.compute_hash()
        return computed_hash

    @classmethod
    def is_valid_proof(cls, block_valid, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block_valid.compute_hash())

    @classmethod
    def check_chain_validity(cls, chain):
        result = True
        previous_hash = "0"

        for chain_block in chain:
            if type(chain_block) != dict:
                block_hash = chain_block.block_hash
            else:
                block_hash = chain_block["block_hash"]

            if chain_block.index == 0:
                previous_hash = chain_block.block_hash
                continue
            else:
                delattr(chain_block, "block_hash")
                if not cls.is_valid_proof(chain_block, block_hash):
                    print("Block_hash is not the same as block's proof of work")
                    result = False
                    break
                if previous_hash != chain_block.previous_hash:
                    print(previous_hash)
                    print("Previous hash is not the same, expect: " + str(chain_block.previous_hash))
                    result = False
                    break
                if type(chain_block.transactions) == str:
                    if not chain_block.has_valid_transaction(chain_block.transactions):
                        print("Transactions are not valid")
                        result = False
                        break
                else:
                    if not chain_block.has_valid_transaction():
                        print("Transactions are not valid or not signed")
                        result = False
                        break
                if type(chain_block) != dict:
                    chain_block.block_hash, previous_hash = block_hash, block_hash
                else:
                    chain_block["block_hash"], previous_hash = block_hash, block_hash

        print(result)


# create a blockchain
blockchain = Blockchain()
blockchain.add_genesis_block()

t1 = Transaction("Satoshi", "Mike", 5)
t1.sign_transaction()
blockchain.add_transaction(t1)
t2 = Transaction("Mike", "Satoshi", 1)
t2.sign_transaction()
blockchain.add_transaction(t2)
t3 = Transaction("Satoshi", "Hal Finney", 5)
t3.sign_transaction()
blockchain.add_transaction(t3)
blockchain.add_block()

t4 = Transaction("Mike", "Alice", 100)
t4.sign_transaction()
blockchain.add_transaction(t4)
t5 = Transaction("Alice", "Bob", -0.5)
t5.sign_transaction()
blockchain.add_transaction(t5)
blockchain.add_block()

t6 = Transaction("Vine", "Mark", 0.01)
t6.sign_transaction()
blockchain.add_transaction(t6)
blockchain.add_block()

# make a copy of this blockchain by copy the original blockchain
chain_data = []
for block in blockchain.chain:
    chain_data.append(block.get_block())

generated_blockchain = Blockchain()
generated_blockchain.add_genesis_block()

for idx, block in enumerate(chain_data):
    if idx == 0:
        continue

    new_block = Block(block["index"],
                      block["transactions"],
                      block["timestamp"],
                      block["previous_hash"],
                      block["nonce"])
    proof = block['block_hash']
    generated_blockchain.new_block(new_block, proof)


# check if two blockchains are the same
print("My blockchain: ")
blockchain.print()
print("Blockchain's validity :")
blockchain.check_chain_validity(generated_blockchain.chain)


# ========================
# time to hack this blockchain 😈
target_transactions = generated_blockchain.chain[1].transactions.split('\t')[1]
generated_blockchain.chain[1].transactions = \
    generated_blockchain.chain[1].transactions.replace(target_transactions, Transaction("A", "B", "100").print())
# generated_blockchain.chain[1].hash = "0000huj"
# generated_blockchain.chain[1].nonce = 12345

print("Blockchain's validity :")
blockchain.check_chain_validity(generated_blockchain.chain)
