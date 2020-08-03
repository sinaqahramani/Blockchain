class Blockchain():
    """This class is responsible for managing the chain.
    It will store transactions and have some helper methods
    for adding new blocks to the chain.
    """
    def __init__(self):
        self.chain = []
    self.current_trxs = []

    def new_block(self):
        """Creats a new Block and adds it to the chain"""
        pass

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

    @staticmethod
    def hash(block):
        """Hash a Block"""
        pass

    @property
    def last_block(self):
        """Returns the last Block in the chain"""
        pass