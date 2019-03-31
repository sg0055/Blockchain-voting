from uuid import uuid4
from os.path import exists
class Key:

    def __init__(self):
        self.key=None
        self.assign_key()
        
    def load_key(self):
        try:
            with open('key.txt',mode='r') as f:
                key=f.read()
            return key 
        except(IOError,IndexError):
            print("Key Loading falied..")

    def assign_key(self):
        try:   
            if exists('key.txt'):
                    self.key=self.load_key()
            else:
                self.key=self.generate_key()
                self.save_key()    
        except(IOError,IndexError):
            print("Key Assignment falied..")
                    
    def save_key(self):
        try:
            with open("key.txt",mode='w') as f:
                f.write(self.key)
        except(IOError,IndexError):
            print("Key Saving falied..")

    def generate_key(self):
        return str(uuid4())