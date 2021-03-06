from lxml import etree as ET
import lxml.html.soupparser as soup
import urllib2

# This module is an example of parsing xml to find pertinent information. In this case, the xml
# is actually the html of a google maps page. We use the lxml library to load it as a python object,
# and the html soup parser to fix any issues understanding the html and still retrieve acceptable,
# well structured xml

def urlToET(url, tryAgain = True):
    # This just attempt to load the URL twice to account for the possibility of network trouble.
    # This is not a good example of error-proof code, but it still greatly reduces the probability
    # of errors in retrieval effecting your application.
    try:
        fURL = urllib2.urlopen(url)
    except Exception, e:
        if tryAgain:
            return urlToET(url, tryAgain = False)
        else:
            return None
    return soup.parse(fURL)

def parseMap(tree, multiple=False):
    # This function parses the inputted xml data for either one or more routes, finding the relevant
    # information about each. It uses xpath, a way of searching for a particular node within a
    # tree of xml data.
    routes = []
    # These next two lines find all nodes that look like <div class='dir-altroute-inner'>....</div> (inside
    # certain parent nodes), which correpond to the route information we're looking for. You can look at
    # ./map.html if you want to see the raw info, although it's pretty ugly.
    route_div = '//ol[@id="dir_altroutes_body"]/li[@class="dir-altroute"]/div[@class="dir-altroute-inner"]'
    div_list = tree.xpath(route_div)
    x = 0
    for div in div_list:
        # This bit of arguably ugly xml parsing is just pulling names and project times from the route
        # info, and remembering if they include projected traffic or not.
        attribs = {}
        for i in div.findall('div'):
            cl = i.get('class')
            if cl is not None:
                if cl.find('altroute-rcol') >= 0:
                    if cl.find('altroute-info') >= 0:
                        attribs['traffic'] = i.text.strip()
                    else:
                        attribs['normal'] = i.text.strip()
                elif cl.find('altroute-info') >= 0:
                    attribs['dist'] = i.text.strip()
            else:
                link = i.find('a')
                if link is not None:
                    attribs['name'] = link.text.strip()
        routes[len(routes):] = [attribs]
        x += 1
        if x == 3 or multiple == False:
            return routes
    return routes


