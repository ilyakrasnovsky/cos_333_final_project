from firebase import firebase
from requests import HTTPError

firebase = firebase.FirebaseApplication('https://burning-inferno-5981.firebaseio.com/', authentication=None)
    
#Fake aircraft class for practice
class aircraft:
    def __init__(self, name, mtow, S):
        self.name  = name
        self.mtow  = mtow
        self.S  = S

#Convert instance of aircraft class into a dictionary,
#where every instance variable is stored under its name
def make_air_dict(aircraft):
    air_dict = dict()
    air_dict['name'] = aircraft.name
    air_dict['mtow'] = aircraft.mtow
    air_dict['S']    = aircraft.S
    return air_dict

#Convert instance an aircraft dictionary,
#into an instance of the aircraft class
def make_air_class(air_dict):
    air = aircraft(air_dict['name'], air_dict['mtow'], air_dict['S'])
    return air

#Add a converted aircraft dictionary to the firebase,
#returns True if successful, False if name collision,
#or access denied
def add_to_db(air_dict):
    isPresent = get_from_db(air_dict['name'])
    if (isPresent == None):
        try:
            firebase.post('/aircraft-dev/%s' % air_dict['name'], air_dict)
            #print ("Add successful")
            return True
        except HTTPError:
            #print ("Add unsuccessful : access denied")
            return False
    else:
        #print ("Add unsuccessful : already present")
        return False

#Retrieve information about an aircraft in the database from
#its name. Returns a dictionary describing the aircraft, or
#None if not found
def get_from_db(air_name):
    retrieved = firebase.get('/aircraft-dev', air_name)
    if (retrieved == None):
        #print ("Not found")
        return None
    else:
        #print ("found : " + str(retrieved.values()[0])) 
        return make_air_class(retrieved.values()[0]) 

#Delete the aircraft entry with the given name from the
#database. Return True if successful, False otherwise
def delete_from_db(air_name):
    try:
        firebase.delete('/aircraft-dev', air_name)
        #print ("Delete successful")
        return True
    except HTTPError:
        #print ("Delete unsuccessful : access denied")
        return False
    
#Update

#print(result['name'])
#print(result['mtow'])
#print(result['S'])

#Tester client
def main():
    #print("STARTING BY CONNECTING TO THE FIREBASE")
    print ("SEARCHING THE DATABASE FOR THE A300")
    found = get_from_db('A300') 
    if (found !=None):
        print (found.name)
    print ("ADDING THE A300 TO THE DATABASE")
    new_air = aircraft('A300', 165000, 260)
    new_air_dict = make_air_dict(new_air)
    add_to_db(new_air_dict)
    print ("ADDING THE 747SR TO THE DATABASE")
    new_air = aircraft('747SR', 340190, 525)
    new_air_dict = make_air_dict(new_air)
    add_to_db(new_air_dict)
    print ("SEARCHING THE DATABASE FOR THE 747SR")
    found = get_from_db('747SR') 
    if (found != None):
        print (found.mtow)
    else:
        print ('not found')
    print ("DELETING THE 747SP FROM THE DATABASE")
    delete_from_db('747SP')
    print ("DELETING THE 747SR FROM THE DATABASE")
    delete_from_db('747SR')

if __name__ == '__main__':
    main()

'''
ASYNC GET AND CALLBACK EXAMPLE
def put_aircraft(air_dict):
    with open('/aircraft/%s.json' % air_dict['name'], 'w') as airfile:
        airfile.write(json.dumps(air_dict, cls=jsonutil.JSONEncoder))

#firebase.get_async('/users', None, {'print': 'pretty'}, callback=log_user)
'''