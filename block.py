from time import time

class Block:
    def __init__(self,index,prev_hash,id,vote,time=time()):
        self.index=index
        self.prev_hash=prev_hash
        self.evm_id=id
        self.vote=vote
        self.timestamp=time

    def __repr__(self):
        return str(self.__dict__)