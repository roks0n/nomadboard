FROM ubuntu:trusty

WORKDIR /home/nomadboard/code

RUN apt-get -qq update && \
    apt-get upgrade -y && \
    apt-get install -y software-properties-common curl && \
    apt-get clean

RUN useradd -ms /bin/bash nomad

# Install Node
RUN add-apt-repository ppa:chris-lea/node.js && \
   apt-get update && \
    apt-get install -y nodejs libfontconfig python build-essential && \
    apt-get clean && \
    npm install npm@2.7.0 -g

# Install dependencies
ADD package.json /home/nomadboard/code/package.json
RUN npm install

ADD Gruntfile.js /home/nomadboard/code/Gruntfile.js
ADD .jshintrc /home/nomadboard/code/.jshintrc

RUN npm run-script grunt
