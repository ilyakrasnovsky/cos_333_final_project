import urllib, re
class CASClient:
   def __init__(self, service_url):
      self.cas_url = 'https://authenticate.princeton.edu/cas/'
      self.service_url = service_url + "gotoBB"
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
def main():
  print "CASClient does not run standalone"
if __name__ == '__main__':
  main()