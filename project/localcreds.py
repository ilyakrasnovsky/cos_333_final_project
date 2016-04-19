'''
Sets up SECRET_KEY and FIREBASE_KEY for developing our 
application locally on your machine. Run:

$ python localcreds.py '<SECRET_KEY_HERE>' '<FIREBASE_KEY_HERE>'

to set it up (NOTE THE QUOTES!). This only needs to be done once.
'''
import os, sys

def get_credentials(key=None, firebase=False):
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    if (firebase):
        credential_path = os.path.join(credential_dir,
                                   'ASSIGNCALS_FIREBASE_SECRET.txt')
    else:
        credential_path = os.path.join(credential_dir,
                                   'ASSIGNCALS_SECRET.txt')
    if (key != None):
        with open (credential_path, 'w') as secret_file:
            secret_file.write(key)    
    with open (credential_path, 'r') as secret_file:
        SECRET_KEY = secret_file.read()
    return SECRET_KEY

#Tester client
def main(argv):
    if (len(argv) >= 2):
        KEY = argv[0]
        FIREBASE_KEY = argv[1]
    else:
        KEY = None
        FIREBASE_KEY = None
    print ("SECRET_KEY SET TO  : " + get_credentials(KEY))
    print ('FIREBASE_KEY SET TO : ' + get_credentials(FIREBASE_KEY, firebase=True))

if __name__ == '__main__':
    main(sys.argv[1:])