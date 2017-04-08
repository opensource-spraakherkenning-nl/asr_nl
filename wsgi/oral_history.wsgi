import sys
sys.path.append("/vol/tensusers/eyilmaz/FAME/webservice/fame_align")
import fame_align
import clam.clamservice
application = clam.clamservice.run_wsgi(fame_align)
