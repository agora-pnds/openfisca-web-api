FROM debian:unstable
# MAINTAINER OpenFisca Team <contact@openfisca.fr>
RUN apt-get update && apt-get upgrade -y
RUN apt-get install --no-install-recommends -y git python-babel python-isodate python-numpy python-pastedeploy python-pip python-scipy python-tz python-weberror python-webob
RUN pip install -e git+https://github.com/etalab/biryani.git@biryani1#egg=Biryani1
RUN pip install -e git+https://github.com/openfisca/openfisca-core.git#egg=OpenFisca-Core
RUN pip install -e git+https://github.com/openfisca/openfisca-france.git#egg=OpenFisca-France
RUN pip install -e git+https://github.com/openfisca/openfisca-web-api.git#egg=OpenFisca-Web-API

RUN apt-get install --no-install-recommends -y python-pastescript
RUN sed "s/host = 127.0.0.1/host = 0.0.0.0/" /src/openfisca-web-api/development.ini > /src/openfisca-web-api/development-local.ini
CMD paster serve /src/openfisca-web-api/development-local.ini
EXPOSE 2014
