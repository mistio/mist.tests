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
        chromium \
        libgconf-2-4 \
        libav-tools \
        vim \
        jq \
        x11vnc && \
    apt-get -t jessie-backports -y --no-install-recommends install ffmpeg && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

ARG CHROMEDRIVER_VERSION=2.27
RUN curl -SLO "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin && \
    rm chromedriver_linux64.zip

RUN git clone https://github.com/commixon/gmail && \
    cd gmail && python setup.py install

COPY requirements.txt /mist.tests/requirements.txt
RUN pip install --no-cache-dir -r /mist.tests/requirements.txt

COPY . /mist.tests/
WORKDIR /mist.tests/

RUN pip install -e .

RUN ln -s /mist.tests/container/xvfb-chromium /usr/bin/xvfb-chromium && \
    ln -s /mist.tests/container/xvfb-chromium /usr/bin/chromium-browser && \
    ln -s /mist.tests/container/xvfb-chromium /usr/bin/google-chrome && \
    ln -s /mist.tests/container/vnc_server.sh /usr/bin/vnc && \
    ln -s /mist.tests/container/start_test_env.sh /test_env.sh

ENV DISPLAY=:1.0
