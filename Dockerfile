FROM python:2.7-stretch
MAINTAINER mist.io <support@mist.io>

RUN set -x && \
    apt-get update -yq && \
    apt-get -yq --no-install-recommends install \
        ca-certificates \
        curl \
        wget \
        xvfb \
        unzip \
        libgconf-2-4 \
        libav-tools \
        vim \
        jq \
        less \
        socat \
        x11vnc \
        ffmpeg \
    && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
    apt-get update -y && \
    apt-get -y install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

ARG CHROMEDRIVER_VERSION=2.45
RUN curl -SLO "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin && \
    rm chromedriver_linux64.zip

# Install latest version of GNU parallel
RUN (wget -O - pi.dk/3 || curl pi.dk/3/ || fetch -o - http://pi.dk/3) | bash

#Install latest tmux
RUN git clone https://github.com/tmux/tmux.git && cd tmux && sh autogen.sh && ./configure && make && mv tmux /usr/bin/

RUN pip install git+https://github.com/mverteuil/pytest-ipdb.git#egg=pytest-ipdb

COPY container/requirements.txt /mist.tests/requirements.txt
RUN pip install --no-cache-dir -r /mist.tests/requirements.txt

COPY . /mist.tests/
WORKDIR /mist.tests/

RUN pip install -e .

RUN ln -s /mist.tests/container/start_test_env.sh /test_env.sh

ENV DISPLAY=:1.0
