import sys
#sys.path.append("/vol/tensusers/eyilmaz/FAME/webservice/oral_history")
import oral_history
import clam.clamservice
application = clam.clamservice.run_wsgi(oral_history)
