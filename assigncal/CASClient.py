import urllib, re
class CASClient:
   def __init__(self):
      self.cas_url = 'https://fed.princeton.edu/cas/'
      #self.service_url = 'https://localhost:8000/gotoBB'
      self.service_url = 'http://assign-cals-cos333.herokuapp.com/gotoBB'
   def Authenticate(self):
      login_url = self.cas_url + 'login' \
         + '?service=' + urllib.quote(self.service_url)
      return login_url
   def Validate(self, ticket):
      val_url = self.cas_url + "validate" + \
         '?ticket=' + urllib.quote(ticket) + \
         '&service=' + urllib.quote(self.service_url)
      r = urllib.urlopen(val_url).readlines()   # returns 2 lines
      if len(r) == 2 and re.match("yes", r[0]) != None:
         return r[1].strip()
      return None
      '''
      val_url = self.cas_url + "serviceValidate" + \
         '?ticket=' + urllib.quote(ticket) + \
         '&service=' + urllib.quote(self.ServiceURL())   
      print (val_url)
      r = urllib.urlopen(val_url).readlines()   # returns 2 lines
      print (r)
      '''
def main():
  print "CASClient does not run standalone"
if __name__ == '__main__':
  main()