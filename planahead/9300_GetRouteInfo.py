#!/usr/bin/python
import cgi
from heapq import heappush, heappop
import parseMap, getUser

# This is the main logical page in the application. It accepts a source and destination address
# and queries the database to retrieve any google maps urls corresponding to routes between the two.
# It then scrapes the page for the current traffic information, and finds the projected route time
# either with or without traffic, making sure to tell the user whether or not the projected time includes
# traffic. It the sorts the routes based on projected time to destination and sends them back to Angel in
# the form of a number of different variables, along with one describing how many routes are there.
# Additionally, if the user has only saved one route between destinations, it will retrieve the next few
# fastest routes from Google to try and still give them information about alternate possibilities.

def idToInfo(number):
    # gets user object from DB, as usual
    return getUser.get(number)[1]

def getRouteInfo(doc, source, destination):
    # first block here checks each route (trip) the user has saved, and sees if it has the proper
    # source and destination addresses. If so, it adds the trip to a list of potential routes.
    helpful = []
    for t in doc['trips']:
        if t['source'] == source and t['destination'] == destination:
            helpful.append(t)
    routes = len(helpful)
    # There are two different logical possibilities depending on the number of saved routes.
    # If the user has only one route, we query google for the top 3 routes it suggests and
    # give information about these three. This involves getting the html for the google maps page,
    # and then parsing it for the time, title, and whether it involves traffic. We then add it
    # list of routes as a dictionary containing the useful information.
    if routes == 1:
        t = parseMap.parseMap(parseMap.urlToET(helpful[0]['map']), True)
        info = []
        for temp in t:
            if 'traffic' in temp:
                traf = 'with current traffic.'
                norm = temp['traffic']
            else:
                traf = 'but we have no current traffic data.'
                norm = temp['normal']
            norm = norm[:norm.find("in traffic")]
            norm = norm.replace("min", "minutes")
            norm = norm.replace("minutess ", "minutes")
            if 'title' in helpful[0]:
                title = helpful[0]['title']
            else:
                title = temp['name']
            info.append({'title' : title, 'normal' : norm, 'traffic' : traf})
    else:
        # If the user has multiple routes saved, we use those instead of asking google
        # for its suggestions, parsing them in the same fashion as before
        info = []
        for r in helpful:
            temp = parseMap.parseMap(parseMap.urlToET(r['map']))
            temp = temp[0]
            if 'traffic' in temp:
                traf = 'with current traffic.'
                norm = temp['traffic']
            else:
                traf = 'but we have no current traffic data.'
                norm = temp['normal']
            norm = norm[:norm.find("in traffic")]
            norm = norm.replace("min", "minutes")
            norm = norm.replace("minutess ", "minutes")
            if 'title' in r:
                title = r['title']
            else:
                title = temp['name']
            info.append({'title' : title, 'normal' : norm, 'traffic' : traf})
    inorder = []
    # this next part just cleans up the information to register hours vs minutes and then
    # orders the routes from fastest to slowest using heapsort
    for item in info:
        val = 0
        time = item['normal']
        hours = time.find('hours')
        minutes = time.find('minutes')
        if hours > 0:
            val += (int(time[:hours]) * 60)
        else:
            hours = 0
        if minutes >0:
            if hours == 0:
                val += (int(time[:minutes]))
            else:
                val += (int(time[hours + 5 : minutes]))
        heappush(inorder, (val, item))
    return [heappop(inorder)[1] for item in info]


def toAngelXML(info):
    # here, we just define a number of variables of the form r1title, r1normal, r1traffic, etc.
    # to send angel the information we've retrieved. 
    xmlstring = """<ANGELXML><MESSAGE><PLAY><PROMPT type=\"text\">.</PROMPT></PLAY><GOTO destination="/3101" /></MESSAGE><VARIABLES>\n"""
    xmlstring += '<VAR name="numroutes" value="' + str(len(info)) + '"/>\n' 
    for i in range(len(info)):
        xmlstring += '<VAR name="r' + str(i+1) + 'title" value="' + info[i]['title'] + '"/>\n' 
        xmlstring += '<VAR name="r' + str(i+1) + 'normal" value="' + info[i]['normal'] + '"/>\n'
        xmlstring += '<VAR name="r' + str(i+1) + 'traffic" value="' + info[i]['traffic'] + '"/>\n'    
    xmlstring += """</VARIABLES></ANGELXML>"""
    return xmlstring

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers
inputs = cgi.FieldStorage()
if "number" not in inputs or "source" not in inputs or "destination" not in inputs:
    num = "2012475876"
    source = "girlfriend"
    destination = "home"
else:
    num = inputs["number"].value
    source = inputs['source'].value
    destination = inputs['destination'].value
print toAngelXML(getRouteInfo(idToInfo(num), source, destination))

