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
$ docker pull proycon/asr_nl
```

Run the container as follows:

```
$ docker run -v /path/to/your/data:/data -p 8080:80 proycon/asr_nl
```
Ensure that the directory you pass is writable.

Assuming you run locally, the web interface can then be accessed on ``http://127.0.0.1:8080/``.

If you want to deploy this service on your own infrastructure, you will want to set some of the environment variables
defined in the `Dockerfile` when running the container, most notably the ones regarding authentication, as this is by
default disabled and as such *NOT* suitable for production deployments.
