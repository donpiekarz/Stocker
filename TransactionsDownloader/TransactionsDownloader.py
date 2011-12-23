
# global
import sys
import os
import urllib2
from time import gmtime, strftime

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
    args = { "date" : strftime("%Y-%m-%d", gmtime()) }
    
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




if __name__ == "__main__":
    sys.exit(main())




