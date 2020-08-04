from uuid import uuid4
from flask import Flask, jsonify, request
from blockchain import Blockchain


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
        'previous_hash': block['previous_hash'],
    }
    return jsonify(res), 200


# Create the /transactions/new endpoint,
# which is a POST request, since we’ll be sending data to it
@app.route('/trx/new', methods=['POST'])
def new_trx():
    values = request.get_json()
    # check that te required fields are in the POSTed data:
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing Values', 400

    # Create a new Transaction
    index = blockchain.new_trx(values['sender'], values['recipient'], values['amount'])
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


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for n in nodes:
        blockchain.register_node(n)

    res = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes)
    }

    return jsonify(res), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        res = {
            'message': 'Our Chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        res = {
            'message': 'Our Chain is authoritative',
            'chain': blockchain.chain
        }

        return jsonify(res), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=6000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)
