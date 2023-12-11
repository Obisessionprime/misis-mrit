FROM python:3.9
ARG WORKSPACE=/Users/vigovskij/misis/mrit/misis-mrit

COPY ${WORKSPACE}/src /ansible_runner/

WORKDIR /ansible_runner

RUN python3 -m pip install .

