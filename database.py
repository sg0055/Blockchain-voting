from firebase import firebase
firebase = firebase.FirebaseApplication('https://bevm-nullbyte.firebaseio.com/voters_data', None)
result = firebase.get('/voters_data',None)
#result = firebase.post('/voters_data/1',{'fing_print':'3232','tranc_id':'3443234'})
print(list(result))