FROM python:3.11-bullseye
MAINTAINER mist.io <support@mist.io>

RUN set -x && \
    apt-get update -yq && \
    apt-get -yq --no-install-recommends install \
        ca-certificates \
        bison \
        lynx \
        curl \
        wget \
        xvfb \
        unzip \
        libgconf-2-4 \
        ffmpeg \
        vim \
        jq \
        less \
        socat \
        x11vnc \
    && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
    apt-get update -y && \
    apt-get -y install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

ARG CHROMEDRIVER_VERSION=108.0.5359.71
RUN curl -SLO "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin && \
    rm chromedriver_linux64.zip

# Install latest version of GNU parallel
# RUN (wget -O - pi.dk/3 || curl pi.dk/3/ || fetch -o - http://pi.dk/3) | bash

#Install latest tmux
RUN git clone https://github.com/tmux/tmux.git && cd tmux && sh autogen.sh && ./configure && make && mv tmux /usr/bin/

RUN pip install git+https://github.com/mverteuil/pytest-ipdb.git#egg=pytest-ipdb

COPY container/requirements.txt /mist.tests/requirements.txt
RUN pip install --no-cache-dir -r /mist.tests/requirements.txt

COPY . /mist.tests/
WORKDIR /mist.tests/

RUN pip install -e .

ENV DISPLAY=:1.0
