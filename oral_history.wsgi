import sys
#sys.path.append("/vol/tensusers/eyilmaz/FAME/webservice/oral_history")
import fame_align
import clam.clamservice
application = clam.clamservice.run_wsgi(fame_align)
