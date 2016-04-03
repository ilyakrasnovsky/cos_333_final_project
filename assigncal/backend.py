from firebase import firebase
from requests import HTTPError
from django.conf import settings

#Authentication 
FIREBASE_URL = settings.FIREBASE_URL
FIREBASE_KEY = settings.FIREBASE_KEY
authentication = firebase.FirebaseAuthentication(FIREBASE_KEY, 'ilyakrasnovsky@gmail.com', admin = True)
fdb = firebase.FirebaseApplication(FIREBASE_URL, authentication=authentication)

#Add to db
def add_to_db(stuff):
    fdb.post('/text/%s' % stuff['name'], stuff)
    '''
    isPresent = get_from_db(stuff)
    if (isPresent == None):
        try:
            fdb.post('/text/', stuff)
            #print ("Add successful")
            return True
        except HTTPError:
            #print ("Add unsuccessful : access denied")
            return False
    else:
        #print ("Add unsuccessful : already present")
        return False
    '''
#Get from db
def get_from_db(name):
    retrieved = fdb.get('/text', name)
    if (retrieved == None):
        #print ("Not found")
        return None
    else:
        #print ("found : " + str(retrieved.values()[0])) 
        return retrieved.values()