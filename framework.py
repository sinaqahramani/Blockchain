from blockchain import Blockchain
from flask import Flask, jsonify, request
from uuid import uuid4

# Instantiate Our Node
app = Flask(__name__)

# Generate a globally unique address for this node:
node = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

# Create the /mine endpoint, which is a GET request.
# It has to do three things:
#  - Calculate the Proof of Work
#  - Reward the miner (us) by adding a transaction granting us 1 coin
#  - Forge the new Block by adding it to the chain
@app.route('/mine', methods=['GET'])
def mine():
    # Run the POW alogorithm to get the next proof.
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.pow(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.

    blockchain.new_trx(
        sender="0",
        recipient=node,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    res = {
        'message': "new Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash':block['previous_hash'],
    }
    return jsonify(res), 200


# Create the /transactions/new endpoint,
# which is a POST request, since we’ll be sending data to it
@app.route('/trx/new', methods=['POST'])
def new_trx():
    values = request.get_json()
    # check that te required fields are in the POSTed data:
    required = ['sender', 'recepient', 'amount']
    if not all (k in values for k in required):
        return 'Missing Values', 400

    # Create a new Transaction
    index = blockchain.new_trx(values['sender'], values['recepient'], values['amount'])
    res = {
        'message': f'Transaction will be added to Block {index}'
    }

    return jsonify(res), 201

# Create the /chain endpoint, which returns the full Blockchain:
@app.route('/chain', methods=['GET'])
def full_chain():
    res = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(res), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
