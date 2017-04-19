#!/bin/bash
if [ -z $PYTHONPATH ]; then
    export PYTHONPATH=/vol/tensusers/eyilmaz/FAME/webservice/oral_history
else
    export PYTHONPATH=/vol/tensusers/eyilmaz/FAME/webservice/oral_history:$PYTHONPATH
fi
clamservice -d oral_history
