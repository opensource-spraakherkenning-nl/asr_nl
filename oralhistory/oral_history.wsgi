import sys
import oralhistory.oral_history
import clam.clamservice
application = clam.clamservice.run_wsgi(oralhistory.oral_history)
