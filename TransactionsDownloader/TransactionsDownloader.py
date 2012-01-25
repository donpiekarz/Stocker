
# global
import sys
import os
import urllib2
import time 
from optparse import OptionParser
import re

# project
import stocker.utils
import stocker.TransactionsDownloader.config



# creates needed directories for transactions
def checkDirs():
    for company in stocker.TransactionsDownloader.configCompanies.tracked:
	path = os.path.join(stocker.TransactionsDownloader.config.configTransactionsDir, company)
	if(not os.path.exists(path)):
	    os.makedirs(path)
	    
	#print path

def main():
    print "TransactionsDownloader starts ..."
    options = parseCommandLine()
    args = { "date" : options.date }
    logger = stocker.utils.getLogger("TransactionsDownloader")
    checkDirs()



    for company in stocker.TransactionsDownloader.configCompanies.tracked:
        path = os.path.join(stocker.TransactionsDownloader.config.configTransactionsDir, company, args["date"]+".csv")
        
        args["id"]=stocker.TransactionsDownloader.configCompanies.onetIds[company]
        
        url = stocker.TransactionsDownloader.config.configTransactionsURL % args
        print company, url
        
        try:
            conn = urllib2.urlopen(url)
        except Exception as e:
            print e
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




