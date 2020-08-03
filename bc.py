class Blockchain():
    """This class is responsible for managing the chain.
    It will store transactions and have some helper methods
    for adding new blocks to the chain.
    """
    def __init__(self):
        self.chain = []
        self.current_trx = []

    def new_block(self):
        """Creats a new Block and adds it to the chain"""
        pass

    def new_trx(self):
        """Adds a new transaction to the list of tarnsactions"""
        pass

    @staticmethod
    def hash(block):
        """Hash a Block"""
        pass

    @property
    def last_block(self):
        """Returns the last Block in the chain"""
        pass