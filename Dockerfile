FROM proycon/lamachine:core
LABEL maintainer="Maarten van Gompel <proycon@anaproy.nl>"
LABEL description="A LaMachine installation with the webservice Automatic Speech Recognition for Dutch"

# Set this to the *public* domain you want to access this service on,
# HTTPS should be handled by your own reverse proxy, LaMachine does
# not provide one! If not set, you can only access over localhost
ARG BASE_URL=""

# You can set this to 'development' if you want the latest development version rather than the latest stable release
ARG VERSION="stable"

# Replace this with your name:
ARG MAINTAINER="Maarten van Gompel"
ARG MAINTAINER_MAIL="proycon@anaproy.nl"

# By default, there is no authentication on the service,
# which is most likely not what you want. You can connect
# your own Oauth2/OpenID Connect authorization using the following build parameters:
ARG OAUTH_AUTH_URL=""
#^-- example for clariah: https://authentication.clariah.nl/Saml2/OIDC/authorization
ARG OAUTH_TOKEN_URL=""
#^-- example for clariah https://authentication.clariah.nl/OIDC/token
ARG OAUTH_USERINFO_URL=""
#^--- example for clariah: https://authentication.clariah.nl/OIDC/userinfo
ARG OAUTH_CLIENT_ID=""
ARG OAUTH_CLIENT_SECRET=""
#^-- always keep this private

# (See https://github.com/proycon/LaMachine/tree/master/docs/service#openid-connect for
# extra documentation on authentication
# - the oauth client id and client secret must be registered with/provider by your
#   authentication provider
# - the callback URL to register with the authentication provider, for the asr_nl
#   webservice,  will be https://your.domain/asr_nl/login)

VOLUME ["/data"]

RUN lamachine-config version "$VERSION" &&\
    if [ -n "$BASE_URL" ]; then lamachine-config lm_base_url "$BASE_URL" && lamachine-config force_https yes; fi &&\
    lamachine-config maintainer_name "$MAINTAINER" &&\
    lamachine-config maintainer_mail "$MAINTAINER_MAIL" &&\
    if [ -n "$OAUTH_AUTH_URL" ]; then lamachine-config oauth_auth_url "$OAUTH_AUTH_URL"; fi &&\
    if [ -n "$OAUTH_TOKEN_URL" ]; then lamachine-config oauth_token_url "$OAUTH_AUTH_URL"; fi &&\
    if [ -n "$OAUTH_USERINFO_URL" ]; then lamachine-config oauth_userinfo_url "$OAUTH_USERINFO_URL"; fi &&\
    if [ -n "$OAUTH_CLIENT_ID" ]; then lamachine-config oauth_client_id "$OAUTH_CLIENT_ID"; fi &&\
    if [ -n "$OAUTH_CLIENT_SECRET" ]; then lamachine-config oauth_client_secret "$OAUTH_CLIENT_SECRET"; fi &&\
    lamachine-config shared_www_data yes &&\
    lamachine-config move_share_www_data yes &&\
    lamachine-add python-core &&\
    lamachine-add labirinto &&\
    lamachine-add kaldi_nl &&\
    lamachine-add asr_nl &&\
    lamachine-update

ENTRYPOINT [ "/usr/local/bin/lamachine-start-webserver", "-f" ]
