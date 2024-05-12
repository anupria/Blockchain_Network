import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Genesis Block
        self.new_block(previous_hash= '1', proof=100)

    def new_block(self, proof, previous_hash= None):
        """
        create a new Block in the Blockchain
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp' : time(),
            'transactions' : self.current_transactions, 
            'proof' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1]),
        }

        #reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block
    
    def new_transaction(self, sender, recipient, amount):
        """
        create a new transaction to go into the next mined block
        """
        self.current_transactions.append({
            'sender' : sender,
            'recipient' : recipient,
            'amount' : amount,
        })
        return self.last_block['index'] + 1
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    @staticmethod
    def hash(block):
        """
        create a SHA-256 hash of a block
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
        - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
        - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# Instantiate the Blockchain
blockchain = Blockchain()

blockchain.new_transaction("Anu", "Bhavesh", 1)
blockchain.new_transaction("Bhavesh", "Chaitanya", 2)

#Mine a new block
last_block = blockchain.last_block
last_proof = last_block['proof']
proof = blockchain.proof_of_work(last_proof)

# Add a new block to the chain
previous_hash = blockchain.hash(last_block)
block = blockchain.new_block(proof, previous_hash)

print("Blockchain:", blockchain.chain)
