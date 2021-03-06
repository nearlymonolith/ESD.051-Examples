# Examples of Supporting [Angel.com][angel] transaction pages, for [EDS.051][esd.051]
[angel]: http://www.angel.com       "Angel.com"
[esd.051]: https://stellar.mit.edu/S/course/ESD/sp11/ESD.051/index.html     "MIT ESD.051"

#### Created by [Anthony Morelli][nm]. Questions? Email [eid-questions@mit.edu][eq]
[nm]: https://github.com/nearlymonolith
[eq]: mailto:eid-questions@mit.edu


As explained in class, Angel is a wonderful platform for creating voice applications, but
trades of extensibility and flexibility in exchange for ease of use by a non-technical
user. Luckily, it also contains the ability to create transaction pages, which open
up the option to interface with any application, provided you can do so via a URL.

The examples provided include interfacing with Angel to retrieve variables, querying
external APIs to retrieve data, parsing XML to extract the data you're interested in,
and formatting the data so that Angel can understand your response.

To serve your scripts online, we suggest hosting them via [scripts.mit.edu][scripts]. This
will allow you to host them for free! You're particularly interested in the
[MIT SIPB Web Script Service][sipbscripts]. If you need to set up a database, use
[MIT SIPB MySQL Service][sql], and always [check the FAQ][faq] before contacting the [TAs][ta] or 
[scripts team][scriptemail].

[scripts]: http://scripts.mit.edu/
[sipbscripts]: http://scripts.mit.edu/web/
[sql]: http://scripts.mit.edu/mysql/
[faq]: http://scripts.mit.edu/faq/
[ta]: mailto:eid-questions@mit.edu
[scriptemail]: mailto:eid-questions@mit.edu

### Helpful Documentation Provided by Angel

 - [AngelXML Samples][1]: A small collection of example pages that show go to play prompts, add
   keyword responses, add error strategies (no input, no match), and create a
   question page.

 - [Transaction Page AngelXML Examples][2]: A much more exhaustive collection of sample
   AngelXML pages that cover almost all of the functionality you would ever need to
   accomplish just about anything via transaction pages.

 - [Transaction Page AngelXML Schema][3]: A complete definition of the AngelXML schema.
   You don't need to understand this to make a useful page, and it is complete overkill
   unless you're really interested in how it works under the hood. It will be largely
   incomprehensible unless you've had extensive XML experience.

 - [AngelXML and PHP][4]: A simple example of using PHP with AngelXML, just in case you
   prefer that to python.

 - [Transaction Page Overview][5]: A quick refresher on transaction pages.

[1]: https://www.socialtext.net/ivrwiki/angelxml_samples
[2]: https://www.socialtext.net/ivrwiki/transaction_page_angelxml_examples
[3]: https://www.socialtext.net/ivrwiki/index.cgi?transaction_page_angelxml
[4]: https://www.socialtext.net/ivrwiki/angelxml_and_php
[5]: https://www.socialtext.net/ivrwiki/transaction_page_overview

### Example Files

All python files have comments and explanations in the file. These should suffice to
make the code readable and understand how to accomplish certain objectives, although
the explanations assume a good working knowledge of and familiarity with python.

 - `Transaction_pages_web.pdf`: The presentation from class, just for reference.

 - `weather.py`: The example from class (and the presentation). Includes retrieving
   variables from a transaction page, querying the Google weather API for information,
   parsing XML for data, and creating a TTS prompt for Angel to read

Planahead was my individual project from the Fall 2010 EID class. It allowed users to
store addresses and various routes between them, and then would query Google for the current
traffic data and projected travel time between a particular source and destination,
and present that to the user so they knew which route to take.

 - `planahead/9000_GetPreliminaryInfo.py`: The purpose of this module is to accept caller id 
   from angel and then hit the database (actually stubbed off and represented by a python 
   dictionary) to see if they're a registered user. If not, it assigned them 1111111111 as 
   a number, which is the corresponding id for the demo account in the database. That way, 
   they can demo the application without being registered.

 - `planahead/9100_GetSource.py`: This module dynamically creates an AngelXML question page to ask 
   the user for their source address. It's dynamic because we have to create the list of
   accepted responses based on the names of addresses they've saved in the stubbed database.

 - `planahead/9200_GetDestination.py`: Gets the user's desired destination address, similar
   to 9100.

 - `planahead/9300_GetRouteInfo.py`: This is the main logical page in the application. It 
   accepts a source and destination address and queries the database to retrieve any google 
   maps urls corresponding to routes between the two.  It then scrapes the page for the 
   current traffic information, and finds the projected route time either with or without
   traffic, making sure to tell the user whether or not the projected time includes traffic.
   It the sorts the routes based on projected time to destination and sends them back to Angel
   in the form of a number of different variables, along with one describing how many routes
   are there.  Additionally, if the user has only saved one route between destinations, it 
   will retrieve the next few fastest routes from Google to try and still give them information
   about alternate possibilities.

 - `planahead/getUser.py`: This module is rather boring. We're simulating a nosql database 
   using a dictionary.  This is a good example of stubbing, though, since we put this in 
   an external module in comparison to all the modules that require user info. This means 
   that conceivably,if we were to connect this to an actual database, the rest of our code 
   would remain (largely) unchanged. Go Modular Design!

 - `planahead/parseMap.py`: This module is an example of parsing xml to find pertinent 
   information. In this case, the xml is actually the html of a google maps page. We use 
   the lxml library to load it as a python object, and the html soup parser to fix any
   issues understanding the html and still retrieve acceptable, well structured xml.

### Helpful Python Libraries

The following libraries relate in some way to what you'll be attempting to accomplish
via transaction pages. In addition to the ones listed here, you should always search for
a relevant library before doing anything overly complicated, like using Twitter, Facebook,
Netflix, or any other API. Chances are someone has written a nice python library for it.

 - [`cgi`][a1]: This is how you get variables out of URL parameters. Useful for transmitting
   variables from Angel to your script.

 - [`lxml`][a2]: Arguably the best xml-processing library in python. Allows you to conveniently
   represent xml as a python object and perform intelligent processing/querying. Although not
   a part of the python standard library, it is installed on `scripts.mit.edu`, so there
   should not be an issue.

 - [`json`][a3]: Converts JSON into a python dictionary, making it easier to manage.

 - [`urllib2`][a4]: Allows you to load data from a URL into python, useful for accessing APIs.

[a1]: http://docs.python.org/library/cgi.html
[a2]: http://lxml.de/
[a3]: http://docs.python.org/library/json.html
[a4]: http://docs.python.org/library/urllib2.html
