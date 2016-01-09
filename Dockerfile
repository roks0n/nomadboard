FROM python:3.5

ENV PYTHONPATH=/home/nomadboard/code
ENV NOMADBOARD_DJANGO_SETTINGS_MODULE nomadboard.settings

RUN apt-get update && \
    apt-get install -y libxml2 libpq5 libevent-2.0-5 libxslt1.1 python3-pip python3.4-dev && \
    apt-get clean

# Install Node.js
RUN apt-get install -y nodejs-legacy nodejs npm

# Install Python packages.
RUN pip3 install -U setuptools==18.3.1 distribute==0.7.3 wheel==0.24.0 pip==7.1.2

ADD requirements.txt /tmp/requirements.txt
RUN pip install --use-wheel -r /tmp/requirements.txt

WORKDIR /home/nomadboard/code
ADD . /home/nomadboard/code
