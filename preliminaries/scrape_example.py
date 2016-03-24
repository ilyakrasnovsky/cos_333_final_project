import urllib
import re
import mechanize

def main():
    #Instantiate the browser
    br = mechanize.Browser()

    #List of first URLs to visit (one for each aircraft class)
    url_list = []
    #Big jets
    url_list.append("https://contentzone.eurocontrol.int/aircraftperformance/details.aspx?ICAO=A124&GroupFilter=3")
    #Med jets
    url_list.append("https://contentzone.eurocontrol.int/aircraftperformance/details.aspx?ICAO=A318&GroupFilter=4")
    #Small jets
    url_list.append("https://contentzone.eurocontrol.int/aircraftperformance/details.aspx?ICAO=ASTR&GroupFilter=1")
    #Big props
    url_list.append("https://contentzone.eurocontrol.int/aircraftperformance/details.aspx?ICAO=A748&GroupFilter=9")
    #Med props
    url_list.append("https://contentzone.eurocontrol.int/aircraftperformance/details.aspx?ICAO=AC50&GroupFilter=11")
    #Small props
    url_list.append("https://contentzone.eurocontrol.int/aircraftperformance/details.aspx?ICAO=AC11&GroupFilter=10")
    for curr_url in url_list:
        #Tell the browser to open the first page and find how many
        #aircraft to scrape
        br.open(curr_url)
        html = br.response().read()
        num_air_re = re.search("Page 1 of ..", html)
        num_air = int(num_air_re.group().split('of ')[1])
        #print (num_air)
        print ("NEW CLASS OF AIRCRAFT")
        for i in range (0, num_air):
            #Tell browser to go to curr_url
            br.open(curr_url)
            #Store the html source of the page in html
            html = br.response().read()
            
            #Use regex to search the html for the aircraft name
            air_name_re = re.search("Aircraft name:.*</span>", html)
            air_name_re = re.search('Type">.*<', air_name_re.group())
            air_name = air_name_re.group().split('>')[1]
            air_name = air_name.split('<')[0]
            print ("Aircraft name : " + str(air_name))

            #Search the page for a link labelled "Next >>", and follow it
            if (i < num_air-1):
                curr_url = br.click_link(text='Next >>') 

if __name__ == '__main__':
    main()