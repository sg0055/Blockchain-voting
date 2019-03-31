import hashlib as hl
import json

def hash_string_256(string):
    
    return hl.sha256(string).hexdigest()


def hash_block(block):
    
    hashable_block = block.__dict__.copy()
    hashed_string=hashable_block['vote']+str(hashable_block['index'])
    return hash_string_256(json.dumps(hashed_string, sort_keys=True).encode())