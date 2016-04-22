import urllib, re, mechanize
class CASClient:
   def __init__(self, service_url):
      self.cas_url = 'https://authenticate.princeton.edu/cas/'
      #self.cas_url = 'https://fed.princeton.edu/cas/'
      self.service_url = service_url + "gotoBB"
   def Authenticate(self):
      login_url = self.cas_url + 'login' \
         + '?service=' + urllib.quote(self.service_url)
      return login_url
   def Validate(self, ticket):
      val_url = self.cas_url + "validate" + \
         '?ticket=' + urllib.quote(ticket) + \
         '&service=' + urllib.quote(self.service_url)
      
      br = mechanize.Browser()
      cookiejar = mechanize.LWPCookieJar()
      br.set_cookiejar( cookiejar ) 
      print ("COOKIEJAR BEFORE GOING TO SITE_URL "),
      print(cookiejar)
      print
      
      # Browser options 
      br.set_handle_equiv( True ) 
      br.set_handle_gzip( True ) 
      br.set_handle_redirect( True ) 
      br.set_handle_referer( True ) 
      br.set_handle_robots( False ) 
      br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 )
      br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ] 
      br.open('http://localhost:8000')

      r = br.open(val_url)
      r = r.readlines()
      print ("COOKIEJAR AFTER GOING TO SITE_URL AND ADDING TICKET"),
      print(cookiejar)    
      print (r)
      print (br)
      print(r[1].strip())
      #r = urllib.urlopen(val_url).readlines()   # returns 2 lines
      #badr = urllib.urlopen(val_url).readlines()
      #print ("r is " + str(r))
      #print ("badr is " + str(badr))
      if len(r) == 2 and re.match("yes", r[0]) != None:
         return (r[1].strip(), br, cookiejar)
      return None
def main():
  print "CASClient does not run standalone"
if __name__ == '__main__':
  main()