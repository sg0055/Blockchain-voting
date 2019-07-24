import json
from hash_util import hash_block
from block import Block
from time import time
from verification import Verification
import requests

class Blockchain:
    def __init__(self,evm_id):
         genesis_block = Block(0, '',evm_id,'')
         self.__chain=[genesis_block]
         self.resolve_conflicts = False
         self.hosting_node=evm_id
         self.load_data()
         self.length=len(self.__chain)
         self.__peers=set()

    def get_chain(self):
          return self.__chain[:]


    def load_data(self):
        print("Loading data........")
        global blockchain
        try:
            with open('blockchain-{}.txt'.format(str(self.hosting_node)[:8]), mode='r') as f:
                
                file_content = f.readlines()
                
                blockchain = json.loads(file_content[0][:-1])
            
                updated_blockchain = []
                for block in blockchain:
                    updated_block = Block(block['index'], block['prev_hash'],block['evm_id'], block['vote'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.__chain = updated_blockchain
                peers = json.loads(file_content[1])
                print("peers: "+str(file_content[1]))
                self.__peers = set(peers)
        except (IOError, IndexError):
               print("Handled Exception")
        
        finally:
            print('Cleanup!')



    def save_data(self):
        try:
            with open('blockchain-{}.txt'.format(str(self.hosting_node)[:8]), mode='w') as f:
                saveable_chain = [block.__dict__ for block in self.__chain]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                f.write(json.dumps(list(self.__peers)))    
        except IOError:
            print('Saving failed!')


    def get_last_blockchain_value(self):
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]



    def mine_block(self,vote):
        if self.hosting_node==None:
            return Flase
        
        last_block = self.__chain[-1]
        
        hashed_block = hash_block(last_block)
        
        block = Block(len(self.__chain),hashed_block,self.hosting_node,vote)
        self.__chain.append(block)
        self.length=len(self.__chain)
        self.save_data()
    
        for node in self.__peers:
            url = 'http://{}/Broadcast'.format(node)
            converted_block = block.__dict__.copy()
            
           
            try:
                response = requests.post(url, json={'block': converted_block})
                if response.status_code == 400 or response.status_code == 500:
                    print('Block declined, needs resolving')
                if response.status_code == 409:
                    self.resolve_conflicts = True
                    self.resolve()

            except requests.exceptions.ConnectionError:
                continue
        return True

    def sync(self,block):
        print("Updating incoming block.....")
        last_block=self.__chain[-1]
        updated_block=Block(len(self.__chain),hash_block(last_block),block['evm_id'],block['vote'], block['timestamp'])
        self.__chain.append(updated_block)
        self.save_data()

    def resolve(self):
            print("Syncing Blockchain")
            replace=False
            longest_length = self.length
            longest_node=''
            for node in self.__peers:
                url = 'http://{}/len'.format(node)
                try:
                    response = requests.get(url)
                    length = response.json()
    
                    if (length > longest_length):
                        replace=True
                        longest_length=length
                        longest_node=node
                except requests.exceptions.ConnectionError:
                    continue
            if replace:
                url = 'http://{}/chain'.format(longest_node)
                print("Node finded")
                response = requests.get(url)
                longest_node_chain=response.json()
                node_chain = [Block( 
                                    block['index'],
                                    block['prev_hash'],
                                    block['evm_id'],
                                    block['vote'],
                                    block['timestamp']) for block in longest_node_chain]
                self.resolve_conflicts = False
                reolace=False
                self.__chain = node_chain
                self.length=len(self.__chain)
                self.save_data()


    def add_block(self, block):
        hashes_match = hash_block(self.__chain[-1]) == block['prev_hash']
        if not hashes_match:
            return False
        
        converted_block = Block(
            block['index'],
            block['prev_hash'],
            block['evm_id'],
            block['vote'],
            block['timestamp'])
        self.__chain.append(converted_block)
        self.length=len(self.__chain)
        self.save_data()
        return True

    def add_peer_node(self, node):
        
        self.__peers.add(node)
        self.save_data()
    
    def count(self):
        countd={}
        for i in range(1,self.length):
            if "Cand"+self.__chain[i].vote in countd:
                countd["Cand"+self.__chain[i].vote]+=1
            else:
                 countd["Cand"+self.__chain[i].vote]=1
        
        try:
            with open('result-{}.txt'.format(str(self.hosting_node)[:8]), mode='w') as f:
               f.write(json.dumps(countd))
               return countd
        except IOError:
            print('Saving failed!')
           #if self.hosting_node==self.__chain[i].evm_id:
                