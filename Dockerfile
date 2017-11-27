FROM python:2.7
MAINTAINER mist.io <support@mist.io>

RUN echo "deb http://ftp.debian.org/debian jessie-backports main" >> /etc/apt/sources.list && \
    apt-get update -y && \
    apt-get -y --no-install-recommends install \
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
        x11vnc && \
    apt-get -t jessie-backports -y --no-install-recommends install ffmpeg && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' && \
    apt-get update -y && \
    apt-get -y install google-chrome-stable

ARG CHROMEDRIVER_VERSION=2.32
RUN curl -SLO "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin && \
    rm chromedriver_linux64.zip

ARG FIREFOX_VERSION=57.0
RUN cd /usr/local && \
    wget http://ftp.mozilla.org/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2 && \
    tar xvjf firefox-$FIREFOX_VERSION.tar.bz2 && \
    ln -s /usr/local/firefox/firefox /usr/bin/firefox && \
    rm firefox-$FIREFOX_VERSION.tar.bz2

ARG GECKODRIVER_VERSION=v0.18.0
RUN wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar xvzf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    chmod +x geckodriver && \
    mv geckodriver /usr/bin/geckodriver

# Install latest version of GNU parallel
RUN (wget -O - pi.dk/3 || curl pi.dk/3/ || fetch -o - http://pi.dk/3) | bash

#Install latest tmux
RUN git clone https://github.com/tmux/tmux.git && cd tmux && sh autogen.sh && ./configure && make && mv tmux /usr/bin/

RUN git clone https://github.com/commixon/gmail && \
    cd gmail && python setup.py install

COPY container/requirements.txt /mist.tests/requirements.txt
RUN pip install --no-cache-dir -r /mist.tests/requirements.txt

COPY . /mist.tests/
WORKDIR /mist.tests/

RUN pip install -e . && pip install git+https://github.com/mverteuil/pytest-ipdb.git#egg=pytest-ipdb

RUN  ln -s /mist.tests/container/start_test_env.sh /test_env.sh
