from flask import Flask,jsonify, request, send_from_directory
from flask_cors import CORS
from node import Node
from getkeys import Key
import threading
from verification import Verification

EVM=Flask(__name__)

CORS(EVM)

@EVM.route('/',methods=['GET'])
def get_ui():
    return send_from_directory('ui','node.html')
    #response={'message':'Node alive'}
    return jsonify(response), 200

@EVM.route('/chain',methods=['GET'])
def brodcast_chain():
    chain=node.blockchain.get_chain()
    dict_chain=[block.__dict__.copy() for block in chain]
    return jsonify(dict_chain), 200

def start_node(port):
    EVM.run(host='0.0.0.0',port=port,threaded=True,debug=None)

@EVM.route('/len',methods=['GET'])
def get_chainLength():
    length=node.blockchain.length
    return jsonify(length), 200

@EVM.route('/result',methods=['GET'])
def result():
    rel=node.blockchain.count()
    #dict_rel=[{cand} for cand in rel]
    return jsonify(rel), 200

@EVM.route('/vote',methods=['POST'])
def vote():
    v=request.get_json()
    node.blockchain.mine_block(v['vote'])
    #print(v['vote'])
    response = {
            'message': 'vote get successfully'}
    return jsonify(response), 200


@EVM.route('/Broadcast',methods=['POST'])
def broadcast_block():
    values = request.get_json()
    if not values:
        response = {'message': 'No data found.'}
        return jsonify(response), 400
    if 'block' not in values:
        response = {'message': 'Some data is missing.'}
        return jsonify(response), 400
    block = values['block']
    my_chain=node.blockchain.get_chain()
    if block['index'] == my_chain[-1].index + 1:
        if node.blockchain.add_block(block):
            response = {'message': 'Block added'}
            return jsonify(response), 201
        else:
            response = {'message': 'Block seems invalid.'}
            return jsonify(response), 409
    elif block['index'] >  my_chain[-1].index:
        response = {
            'message': 'Blockchain seems to differ from local blockchain.'}
        node.blockchain.resolve_conflicts = True
        node.blockchain.resolve()
        return jsonify(response), 200
    else:
        response = {
            'message': 'Blockchain seems to be shorter, block not added'}
        node.blockchain.sync(block)
        return jsonify(response), 409

if __name__=='__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5000)
    args = parser.parse_args()
    port = args.port
    t1=threading.Thread(target=start_node, args=(port,))
    t1.daemon = True
    t1.start()
    verifier=Verification()
    Nkey=Key()
    #Nkey.assign_key()
    node=Node(Nkey.key)
    if not verifier.verify_chain(node.blockchain.get_chain()):
        print("\nInvalid Blockchain!! Exiting.....\n")
        exit()
    node.listen_input()
    node.blockchain.save_data()
    exit()
    
    

