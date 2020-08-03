from blockchain import Blockchain
from flask import Flask, jsonify, request
from uuid import uuid4

# Instantiate Our Node
app = Flask(__name__)

# Generate a globally unique address for this node:
node = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    return "We'll mine a new block"


@app.route('/trx/new', methods=['POST'])
def new_trx():
    return "new transaction"


@app.route('/chain', methods=['GET'])
def full_chain():
    res = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(res), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
