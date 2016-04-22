
import CASClient

def main():
	C = CASClient.CASClient()
	netid = C.Authenticate()
	return netid
