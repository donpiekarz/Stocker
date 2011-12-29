
# global
import sys
import os
import urllib2
import time 
from optparse import OptionParser
import re

# project
from config import *


# creates needed directories for transactions
def checkDirs():
    for company in configCompanies.tracked:
	path = os.path.join(configTransactionsDir, company)
	if(not os.path.exists(path)):
	    os.makedirs(path)
	    
	#print path

def main():
    print "TransactionsDownloader starts ..."

    options = parseCommandLine()
    args = { "date" : options.date }
    
    checkDirs()



    for company in configCompanies.tracked:
	path = os.path.join(configTransactionsDir, company, args["date"]+".csv")
	
	args["id"]=configCompanies.onetIds[company]
	
	url = configTransactionsURL % args
	print company, url
	
	conn = urllib2.urlopen(url)
	f = open(path, 'wb')
	f.write(conn.read())
	f.close()
	
	
    print "all done"



def parseCommandLine():
    parser = OptionParser()

    parser.add_option("-d", "--date", type="string", dest="date", default="", help="Download transactions for date", metavar="DATE")


    (options, _) = parser.parse_args()

    if options.date == "":
        options.date = time.strftime("%Y-%m-%d",  time.gmtime())

    if not re.match("\d{4}-\d{2}-\d{2}", options.date):
        parser.error("Option --date should be %Y-%m-%d e.g. 2011-12-29")

    return options


if __name__ == "__main__":
    sys.exit(main())




