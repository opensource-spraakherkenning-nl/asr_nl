# Automatic Speech Recognition for Dutch

This repository contains the webservice component of the Dutch Speech Recognition system developed at by Emre Yilmaz,
CLST, Radboud University, Nijmegen.

The webservice provides access to models for oral history interviews, parliamentary talks, and daily conversations.

The actual back-end scripts are a part of [Kaldi-NL](https://github.com/opensource-spraakherkenning-nl/Kaldi_NL), which
in turn builds upon [kaldi](http://kaldi-asr.org/), a toolkit for speech recognition.

## Installation

For end-users and hosting partners, we provide a container image that ships with a web interface based on
[CLAM](https://proycon.github.io/clam/). Through this application some of our pretrained models are directly available
for end-users. You can pull a prebuilt image from the Docker Hub registry using docker as follows:

```
$ docker pull proycon/lamachine:asr_nl
```

You can also build the container image yourself using a tool like ``docker build``, which is the recommended option if you are deploying this
in your own infrastructure. In that case will want adjust the ``Dockerfile`` to set some parameters.

Run the container as follows:

```
$ docker run -p 8080:80 proycon/lamachine:asr_nl
```

Assuming you run locally, the web interface for Kaldi-NL can then be accessed on ``http://127.0.0.1:8080/asr_nl``.

