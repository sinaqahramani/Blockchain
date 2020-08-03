from time import time
class Blockchain():
    """This class is responsible for managing the chain.
    It will store transactions and have some helper methods
    for adding new blocks to the chain.
    """
    def __init__(self):
        self.chain = []
        self.current_trxs = []
        # Create the genesis block:
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash = None):
        """
        Creates a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transaction': self.current_trxs,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions:
        self.current_trxs = []
        self.chain.append(block)
        return block

    def new_trx(self,sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The Index of the Block that will hold this transaction
        """

        self.current_trxs.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        """Returns the last Block in the chain"""
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """Hash a Block"""
        pass

