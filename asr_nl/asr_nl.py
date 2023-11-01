#!/usr/bin/env python
#-*- coding:utf-8 -*-

###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- Service Configuration File (Template) --
#       by Maarten van Gompel (proycon)
#       Centre for Language and Speech Technology / Language Machines
#       Radboud University Nijmegen
#
#       https://proycon.github.io/clam
#
#       Licensed under GPLv3
#
###############################################################

#Consult the CLAM manual for extensive documentation

#If we run on Python 2.7, behave as much as Python 3 as possible
from __future__ import print_function, unicode_literals, division, absolute_import

from clam.common.parameters import *
from clam.common.formats import *
from clam.common.converters import *
from clam.common.viewers import *
from clam.common.data import *
from clam.common.digestauth import pwhash
from clam.common.formats import WaveAudioFormat, OggAudioFormat, MP3AudioFormat
import clam
import sys
import os
from base64 import b64decode as D

REQUIRE_VERSION = "3.1.2"

CLAMDIR = clam.__path__[0] #directory where CLAM is installed, detected automatically
WEBSERVICEDIR = os.path.dirname(os.path.abspath(__file__)) #directory where this webservice is installed, detected automatically

# ======== GENERAL INFORMATION ===========

# General information concerning your system.


#The System ID, a short alphanumeric identifier for internal use only
SYSTEM_ID = "asr_nl"
#System name, the way the system is presented to the world
SYSTEM_NAME = "Automatic Transcription of Dutch Speech Recordings"

SYSTEM_VERSION = "0.6.1" #also adapt in setup.py and codemeta.json

#An informative description for this system (this should be fairly short, about one paragraph, and may not contain HTML)
SYSTEM_DESCRIPTION = "This webservice uses automatic speech recognition to provide the transcriptions of recordings spoken in Dutch. You can upload and process only one file per project. For bulk processing and other questions, please contact Henk van den Heuvel at h.vandenheuvel@let.ru.nl."

SYSTEM_AUTHOR = "Emre Yilmaz, Maarten van Gompel"

SYSTEM_AFFILIATION = "Centre for Language and Speech Technology, Radboud University"

SYSTEM_URL = "https://github.com/opensource-spraakherkenning-nl/asr_nl"

SYSTEM_EMAIL = "henk.vandenheuvel@ru.nl"

INTERFACEOPTIONS = "disableliveinput"

#Load external configuration file
loadconfig(__name__)


#Amount of free memory required prior to starting a new process (in MB!), Free Memory + Cached (without swap!). Set to 0 to disable this check (not recommended)
REQUIREMEMORY = 100

#Maximum load average at which processes are still started (first number reported by 'uptime'). Set to 0 to disable this check (not recommended)
#MAXLOADAVG = 10.0

#Minimum amount of free diskspace in MB. Set to 0 to disable this check (not recommended)
#DISK = '/dev/sda1' #set this to the disk where ROOT is on
#MINDISKSPACE = 100

#The amount of diskspace a user may use (in MB), this is a soft quota which can be exceeded, but creation of new projects is blocked until usage drops below the quota again
#USERQUOTA = 100

#The secret key is used internally for cryptographically signing session data, in production environments, you'll want to set this to a persistent value. If not set it will be randomly generated.
#SECRET_KEY = 'mysecret'

# ======== WEB-APPLICATION STYLING =============

#Choose a style (has to be defined as a CSS file in clam/style/ ). You can copy, rename and adapt it to make your own style
STYLE = 'classic'

# ======== ENABLED FORMATS ===========

#In CUSTOM_FORMATS you can specify a list of Python classes corresponding to extra formats.
#You can define the classes first, and then put them in CUSTOM_FORMATS, as shown in this example:

#class MyXMLFormat(CLAMMetaData):
#    attributes = {}
#    name = "My XML format"
#    mimetype = 'text/xml'


class CTMFormat(CLAMMetaData):
    attributes = {}
    name = "Conversation Time Marked File"
    mimetype = "text/plain"

class MP4AudioFormat(CLAMMetaData):
    attributes = {}
    name ="MP4 Audio File"
    mimetype = 'audio/mpeg'
    schemaorg_type = "AudioObject"

class FlacAudioFormat(CLAMMetaData):
    attributes = {}
    name ="Flac Audio File"
    mimetype = 'audio/flac'
    schemaorg_type = "AudioObject"

CUSTOM_FORMATS = [ CTMFormat, MP4AudioFormat ]

# ======= INTERFACE OPTIONS ===========

#Here you can specify additional interface options (space separated list), see the documentation for all allowed options
#INTERFACEOPTIONS = "inputfromweb" #allow CLAM to download its input from a user-specified url

# ======== PREINSTALLED DATA ===========

#INPUTSOURCES = [
#    InputSource(id='sampledocs',label='Sample texts',path=ROOT+'/inputsources/sampledata',defaultmetadata=PlainTextFormat(None, encoding='utf-8') ),
#]

# ======== PROFILE DEFINITIONS ===========

#Define your profiles here. This is required for the project paradigm, but can be set to an empty list if you only use the action paradigm.


PROFILES = [
    Profile(
        InputTemplate('InputWavFile',WaveAudioFormat,"Wav file",
            #StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'), #note that encoding is required if you work with PlainTextFormat
            #StringParameter(id='author',name='Author',description="The author's name", maxlength=100),
            #InputSource(id='sampledoc', label="Sample Document", path=ROOT+'/inputsources/sampledoc.txt', metadata=PlainTextFormat(None, encoding='utf-8',language='en')),
            #CharEncodingConverter(id='latin1',label='Convert from Latin-1',charset='iso-8859-1'),
            #MP3toWaveConverter(id='mp3conv',label='Convert from MP3 File using sox'),
            #OggtoWaveConverter(id='oggconv',label='Convert from OGG File using sox'),
            extension='.wav',
            #filename='filename.txt',
            multi=True #set unique=True if the user may only upload a file for this input template once. Set multi=True if you the user may upload multiple of such files
        ),
        #------------------------------------------------------------------------------------------------------------------------
        OutputTemplate('Transcription',PlainTextFormat,'Automatic transcription of the input recording',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".wav",
            extension='.txt', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        ),
        OutputTemplate('TranscriptionCTM',CTMFormat,'Automatic transcription of the input recording with timestamps (CTM)',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".wav",
            extension='.ctm', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        ),
        OutputTemplate('TranscriptionCTM',CTMFormat,'Automatic transcription of the input recording with timestamps (CTM) and speaker diarisation',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".wav",
            extension='.ctm.spk', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        ),
        OutputTemplate('TranscriptionXML', XMLFormat,'Automatic transcription of the input recording (full data) (AudioDoc XML)',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".wav",
            extension='.xml', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        )
    ),
    #------------------------------------------------------------------------------------------------------------------------
    Profile(
        InputTemplate('InputMP3File',MP3AudioFormat,"MP3 file",
            #StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'), #note that encoding is required if you work with PlainTextFormat
            #StringParameter(id='author',name='Author',description="The author's name", maxlength=100),
            #InputSource(id='sampledoc', label="Sample Document", path=ROOT+'/inputsources/sampledoc.txt', metadata=PlainTextFormat(None, encoding='utf-8',language='en')),
            #CharEncodingConverter(id='latin1',label='Convert from Latin-1',charset='iso-8859-1'),
            #MP3toWaveConverter(id='mp3conv',label='Convert from MP3 File using sox'),
            #OggtoWaveConverter(id='oggconv',label='Convert from OGG File using sox'),
            extension='.mp3',
            #filename='filename.txt',
            multi=True #set unique=True if the user may only upload a file for this input template once. Set multi=True if you the user may upload multiple of such files
        ),
        #------------------------------------------------------------------------------------------------------------------------
        OutputTemplate('Transcription',PlainTextFormat,'Automatic transcription of the input recording',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".mp3",
            extension='.txt', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        ),
        OutputTemplate('TranscriptionCTM',CTMFormat,'Automatic transcription of the input recording with timestamps (CTM)',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".mp3",
            extension='.ctm', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        ),
        OutputTemplate('TranscriptionCTM',CTMFormat,'Automatic transcription of the input recording with timestamps (CTM) and speaker diarisation',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".mp3",
            extension='.ctm.spk', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        ),
        OutputTemplate('TranscriptionXML', XMLFormat,'Automatic transcription of the input recording (full data) (AudioDoc XML)',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".mp3",
            extension='.xml', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        )
    ),
    #------------------------------------------------------------------------------------------------------------------------
    Profile(
        InputTemplate('InputOggFile',OggAudioFormat,"Ogg file",
            #StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'), #note that encoding is required if you work with PlainTextFormat
            #StringParameter(id='author',name='Author',description="The author's name", maxlength=100),
            #InputSource(id='sampledoc', label="Sample Document", path=ROOT+'/inputsources/sampledoc.txt', metadata=PlainTextFormat(None, encoding='utf-8',language='en')),
            #CharEncodingConverter(id='latin1',label='Convert from Latin-1',charset='iso-8859-1'),
            #MP3toWaveConverter(id='mp3conv',label='Convert from MP3 File using sox'),
            #OggtoWaveConverter(id='oggconv',label='Convert from OGG File using sox'),
            extension='.ogg',
            #filename='filename.txt',
            multi=True #set unique=True if the user may only upload a file for this input template once. Set multi=True if you the user may upload multiple of such files
        ),
        #------------------------------------------------------------------------------------------------------------------------
        OutputTemplate('Transcription',PlainTextFormat,'Automatic transcription of the input recording',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".ogg",
            extension='.txt', #set an extension or set a filename:
            multi=True
        ),
        OutputTemplate('TranscriptionCTM',CTMFormat,'Automatic transcription of the input recording with timestamps (CTM)',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".ogg",
            extension='.ctm', #set an extension or set a filename:
            multi=True
        ),
        OutputTemplate('TranscriptionCTM',CTMFormat,'Automatic transcription of the input recording with timestamps (CTM) and speaker diarisation',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".ogg",
            extension='.ctm.spk', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        ),
        OutputTemplate('TranscriptionXML', XMLFormat,'Automatic transcription of the input recording (full data) (AudioDoc XML)',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".ogg",
            extension='.xml', #set an extension or set a filename:
            multi=True
        )
    ),
    Profile(
        InputTemplate('InputMP4File',MP4AudioFormat,"MP4 file",
            #StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'), #note that encoding is required if you work with PlainTextFormat
            #StringParameter(id='author',name='Author',description="The author's name", maxlength=100),
            #InputSource(id='sampledoc', label="Sample Document", path=ROOT+'/inputsources/sampledoc.txt', metadata=PlainTextFormat(None, encoding='utf-8',language='en')),
            #CharEncodingConverter(id='latin1',label='Convert from Latin-1',charset='iso-8859-1'),
            #MP3toWaveConverter(id='mp3conv',label='Convert from MP3 File using sox'),
            #OggtoWaveConverter(id='oggconv',label='Convert from OGG File using sox'),
            extension='.mp4',
            #filename='filename.txt',
            multi=True #set unique=True if the user may only upload a file for this input template once. Set multi=True if you the user may upload multiple of such files
        ),
        #------------------------------------------------------------------------------------------------------------------------
        OutputTemplate('Transcription',PlainTextFormat,'Automatic transcription of the input recording',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".mp4",
            extension='.txt', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        ),
        OutputTemplate('TranscriptionCTM',CTMFormat,'Automatic transcription of the input recording with timestamps (CTM)',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".mp4",
            extension='.ctm', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        ),
        OutputTemplate('TranscriptionCTM',CTMFormat,'Automatic transcription of the input recording with timestamps (CTM) and speaker diarisation',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".mp4",
            extension='.ctm.spk', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        ),
        OutputTemplate('TranscriptionXML', XMLFormat,'Automatic transcription of the input recording (full data) (AudioDoc XML)',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".mp4",
            extension='.xml', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        )
    ),
    Profile(
        # Note: M4A and MP4 are exactly the same
        InputTemplate('InputM4AFile',MP4AudioFormat,"M4A file",
            #StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'), #note that encoding is required if you work with PlainTextFormat
            #StringParameter(id='author',name='Author',description="The author's name", maxlength=100),
            #InputSource(id='sampledoc', label="Sample Document", path=ROOT+'/inputsources/sampledoc.txt', metadata=PlainTextFormat(None, encoding='utf-8',language='en')),
            #CharEncodingConverter(id='latin1',label='Convert from Latin-1',charset='iso-8859-1'),
            #MP3toWaveConverter(id='mp3conv',label='Convert from MP3 File using sox'),
            #OggtoWaveConverter(id='oggconv',label='Convert from OGG File using sox'),
            extension='.m4a',
            #filename='filename.txt',
            multi=True #set unique=True if the user may only upload a file for this input template once. Set multi=True if you the user may upload multiple of such files
        ),
        #------------------------------------------------------------------------------------------------------------------------
        OutputTemplate('Transcription',PlainTextFormat,'Automatic transcription of the input recording',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".m4a",
            extension='.txt', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        ),
        OutputTemplate('TranscriptionCTM',CTMFormat,'Automatic transcription of the input recording with timestamps (CTM)',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".m4a",
            extension='.ctm', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        ),
        OutputTemplate('TranscriptionCTM',CTMFormat,'Automatic transcription of the input recording with timestamps (CTM) and speaker diarisation',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".m4a",
            extension='.ctm.spk', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        ),
        OutputTemplate('TranscriptionXML', XMLFormat,'Automatic transcription of the input recording (full data) (AudioDoc XML)',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".m4a",
            extension='.xml', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        )
    ),
    Profile(
        InputTemplate('InputFlacFile',FlacAudioFormat,"Flac file",
            #StaticParameter(id='encoding',name='Encoding',description='The character encoding of the file', value='utf-8'), #note that encoding is required if you work with PlainTextFormat
            #StringParameter(id='author',name='Author',description="The author's name", maxlength=100),
            #InputSource(id='sampledoc', label="Sample Document", path=ROOT+'/inputsources/sampledoc.txt', metadata=PlainTextFormat(None, encoding='utf-8',language='en')),
            #CharEncodingConverter(id='latin1',label='Convert from Latin-1',charset='iso-8859-1'),
            #MP3toWaveConverter(id='mp3conv',label='Convert from MP3 File using sox'),
            #OggtoWaveConverter(id='oggconv',label='Convert from OGG File using sox'),
            extension='.flac',
            #filename='filename.txt',
            multi=True #set unique=True if the user may only upload a file for this input template once. Set multi=True if you the user may upload multiple of such files
        ),
        #------------------------------------------------------------------------------------------------------------------------
        OutputTemplate('Transcription',PlainTextFormat,'Automatic transcription of the input recording',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".flac",
            extension='.txt', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        ),
        OutputTemplate('TranscriptionCTM',CTMFormat,'Automatic transcription of the input recording with timestamps (CTM)',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".flac",
            extension='.ctm', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        ),
        OutputTemplate('TranscriptionCTM',CTMFormat,'Automatic transcription of the input recording with timestamps (CTM) and speaker diarisation',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".flac",
            extension='.ctm.spk', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        ),
        OutputTemplate('TranscriptionXML', XMLFormat,'Automatic transcription of the input recording (full data) (AudioDoc XML)',
            SetMetaField('encoding','utf-8'), #note that encoding is required if you work with PlainTextFormat
            removeextension=".flac",
            extension='.xml', #set an extension or set a filename:
            #filename='filename.stats',
            multi=True
        )
    ),

]

# ======== COMMAND ===========

#The system command for the project paradigm.
#It is recommended you set this to small wrapper
#script around your actual system. Full shell syntax is supported. Using
#absolute paths is preferred. The current working directory will be
#set to the project directory.
#
#You can make use of the following special variables,
#which will be automatically set by CLAM:
#     $INPUTDIRECTORY  - The directory where input files are uploaded.
#     $OUTPUTDIRECTORY - The directory where the system should output
#                        its output files.
#     $TMPDIRECTORY    - The directory where the system should output
#                        its temporary files.
#     $STATUSFILE      - Filename of the .status file where the system
#                        should output status messages.
#     $DATAFILE        - Filename of the clam.xml file describing the
#                        system and chosen configuration.
#     $USERNAME        - The username of the currently logged in user
#                        (set to "anonymous" if there is none)
#     $PARAMETERS      - List of chosen parameters, using the specified flags

#set variables only if they're not yet defined (in the external configuration)
try:
    SCRATCHDIRECTORY
except NameError:
    SCRATCHDIRECTORY=ROOT+'/scratch/'
try:
    RESOURCEDIRECTORY #This will be the Kaldi_NL directory typically
except NameError:
    RESOURCEDIRECTORY=ROOT+'/resources/'

COMMAND = WEBSERVICEDIR + "/wrapper.sh $STATUSFILE $INPUTDIRECTORY $OUTPUTDIRECTORY "+SCRATCHDIRECTORY+" "+WEBSERVICEDIR+" "+RESOURCEDIRECTORY+" $PARAMETERS"

#Or if you only use the action paradigm, set COMMAND = None

# ======== PARAMETER DEFINITIONS ===========

#The global parameters (for the project paradigm) are subdivided into several
#groups. In the form of a list of (groupname, parameters) tuples. The parameters
#are a list of instances from common/parameters.py

PARAMETERS =  [
    ('Model selection', [
        ChoiceParameter(id='topic',name='Topic',description='This recording contains', default='OH', choices=[('GN','daily conversations'),('OH','oral history interviews'),('PR','parliament talks'),('BD','Belgian Dutch')], paramflag=''),
        #BooleanParameter(id='createlexicon',name='Create Lexicon',description='Generate a separate overall lexicon?'),
        #ChoiceParameter(id='casesensitive',name='Case Sensitivity',description='Enable case sensitive behaviour?', choices=['yes','no'],default='no'),
        #StringParameter(id='author',name='Author',description='Sign output metadata with the specified author name',maxlength=255),
    ] )
]


# ======= ACTIONS =============

#The action paradigm is an independent Remote-Procedure-Call mechanism that
#allows you to tie scripts (command=) or Python functions (function=) to URLs.
#It has no notion of projects or files and must respond in real-time. The syntax
#for commands is equal to those of COMMAND above, any file or project specific
#variables are not available though, so there is no $DATAFILE, $STATUSFILE, $INPUTDIRECTORY, $OUTPUTDIRECTORY or $PROJECT.

ACTIONS = [
    #Action(id='multiply',name='Multiply',parameters=[IntegerParameter(id='x',name='Value'),IntegerParameter(id='y',name='Multiplier'), command=sys.path[0] + "/actions/multiply.sh $PARAMETERS" ])
    #Action(id='multiply',name='Multiply',parameters=[IntegerParameter(id='x',name='Value'),IntegerParameter(id='y',name='Multiplier'), function=lambda x,y: x*y ])
]


# ======== DISPATCHING (ADVANCED! YOU CAN SAFELY SKIP THIS!) ========

#The dispatcher to use (defaults to clamdispatcher.py), you almost never want to change this
#DISPATCHER = 'clamdispatcher.py'

#DISPATCHER_POLLINTERVAL = 30   #interval at which the dispatcher polls for resource consumption (default: 30 secs)
#DISPATCHER_MAXRESMEM = 0    #maximum consumption of resident memory (in megabytes), processes that exceed this will be automatically aborted. (0 = unlimited, default)
#DISPATCHER_MAXTIME = 0      #maximum number of seconds a process may run, it will be aborted if this duration is exceeded.   (0=unlimited, default)
#DISPATCHER_PYTHONPATH = []        #list of extra directories to add to the python path prior to launch of dispatcher

#Run background process on a remote host? Then set the following (leave the lambda in):
#REMOTEHOST = lambda: return 'some.remote.host'
#REMOTEUSER = 'username'

#For this to work, the user under which CLAM runs must have (passwordless) ssh access (use ssh keys) to the remote host using the specified username (ssh REMOTEUSER@REMOTEHOST)
#Moreover, both systems must have access to the same filesystem (ROOT) under the same mountpoint.
