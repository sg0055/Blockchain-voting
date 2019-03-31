from hash_util import hash_string_256, hash_block
class Verification:
    @classmethod
    def verify_chain(cls,blockchain):
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
           
            if block.prev_hash != hash_block(blockchain[index - 1]):
                
                return False
            """ Check for fingerprint also"""
            #if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            #   print('Proof of work is invalid')
            #  return False
        return True