#!/bin/bash
if [ -z $PYTHONPATH ]; then
    export PYTHONPATH=/vol/tensusers/eyilmaz/FAME/webservice/fame_align
else
    export PYTHONPATH=/vol/tensusers/eyilmaz/FAME/webservice/fame_align:$PYTHONPATH
fi
clamservice -d fame_align
