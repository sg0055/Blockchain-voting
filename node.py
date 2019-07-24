from blockchain import Blockchain

from getkeys import Key
class Node:
    def __init__(self,key):
        self.blockchain=Blockchain(key)

    def Cast_vote(self):
        cand = input('Enter the Candidate_no: ')
        return cand


    def get_user_choice(self):
        user_input = input('Your choice: ')
        return user_input


    def print_blockchain_elements(self):
        for block in self.blockchain.get_chain():
            print('Outputting Block')
            print(block)
        else:
            print('-' * 20)
    
    def listen_input(self):
        waiting_for_input = True
        while waiting_for_input:
            
            print('\n\n\nPlease choose')
            print('1: Vote')
            print('2: Output the blockchain block')
            print('3: Add a Node')
            print('4: Count')
            print('q: Quit\n')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                vote=self.Cast_vote()
                if self.blockchain.resolve_conflicts:
                    print('Resolve conflicts first.....')
                    self.blockchain.resolve()
                if self.blockchain.mine_block(vote):
                    print('Vote Successful')
             
            elif user_choice == '2':
                self.print_blockchain_elements()
            elif user_choice == '3':
                self.blockchain.add_peer_node(input())
            elif user_choice == '4':
                 self.blockchain.count()
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print('Input was invalid, please pick a value from the list!')
            
        else:
            print('Ending session.....!')

if __name__=='__main__':
    node=Node()
    
    node.listen_input()