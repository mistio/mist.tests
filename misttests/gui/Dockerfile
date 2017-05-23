FROM ubuntu:14.04

RUN apt-get update -y
RUN apt-get install -y wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update -y
RUN apt-get install -y python
RUN apt-get install -y xvfb
RUN apt-get install -y google-chrome-stable

ENV TEST_SETTINGS_OVERRIDE ""
ENV MIST_DIR /mnt/mist.core
ENV OUTFILE ""
ENV STOP "--stop"
ENV TAGS ""
ENV TEST_TYPE "pr"
ENV PREP_ENV ""
ENV XVFB_NUM 1
ENV SED_REGEX "\/mnt\/mist\.core"
WORKDIR /mnt/mist.core
ENTRYPOINT ( Xvfb :$XVFB_NUM -screen 0 1280x1024x16 & ) && cat bin/cloudpy | sed "s/$SED_REGEX/\/mnt\/mist\.core/g" | python - src/mist/core/tests/gui/prepare_env.py -- $PREP_ENV -k $STOP $TAGS $OUTFILE src/mist/core/tests/gui/$TEST_TYPE/features/
