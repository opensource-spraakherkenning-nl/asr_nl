import sys
import asr_nl.asr_nl
import clam.clamservice
application = clam.clamservice.run_wsgi(asr_nl.asr_nl)
