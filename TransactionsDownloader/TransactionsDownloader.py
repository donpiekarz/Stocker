
# global
import sys
import os
import urllib2
from cookielib import CookieJar
import time 
from optparse import OptionParser
import re
import logging

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
    logger.info("BEGIN")
    logger.info("Downloading data for date: %s" % args["date"])
    checkDirs()



    for company in stocker.TransactionsDownloader.configCompanies.tracked:
        path = os.path.join(stocker.TransactionsDownloader.config.configTransactionsDir, company, args["date"]+".csv")
        
        args["id"]=stocker.TransactionsDownloader.configCompanies.onetIds[company]
        
        url = stocker.TransactionsDownloader.config.configTransactionsURL % args
        print company, url
        logger.info("getting comapny: %s" % company)
        logger.debug("url: %s" % url)
        
        attempt = 0
        success = False
        while attempt < stocker.TransactionsDownloader.config.configMaxAttepmts and not success:
            try:
                cj = CookieJar()
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                conn = opener.open(url)
                success = True
            except urllib2.URLError as e:
                attempt += 1
                logger.error("Downloading data, attempt: %d, Exception: %s, url: %s" % (attempt, e, url))
        
        if attempt >= stocker.TransactionsDownloader.config.configMaxAttepmts:
            msg = "exceeded the maximum number of attempts: %d" % stocker.TransactionsDownloader.config.configMaxAttepmts
            logger.critical(msg)
            raise Exception(msg)
        
        f = open(path, 'wb')
        f.write(conn.read())
        f.close()
	
	
    print "all done"
    logger.info("END")



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




