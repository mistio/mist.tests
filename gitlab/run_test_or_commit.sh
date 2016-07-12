#!/bin/bash

echo "Executing: $*"
eval "$*"
exit_code=$?

if [ $exit_code -eq 0 ]
then
  echo "Tests run successufully. Returning code $exit_code"
else
  echo "Let's commit!"
  chmod 600 /gitlab_id_rsa
  eval `ssh-agent -s`
  ssh-add /gitlab_id_rsa
  ssh-keyscan gitlab.ops.mist.io >> ~/.ssh/known_hosts
  git config --global user.name "mistio-gitlab"
  git config --global user.email gitlab.ops.mist.io@gmail.com
  git clone git@gitlab.ops.mist.io:mistio/mist.test.logs.git /logs
  mkdir -p "/logs/$MIST_TEST_LOG_DIR"
  cp /var/log/*-std* "/logs/$MIST_TEST_LOG_DIR"
  cp /var/log/js_console.log "/logs/$MIST_TEST_LOG_DIR"
  cp /var/log/rabbitmq/* "/logs/$MIST_TEST_LOG_DIR"
  cp /var/log/supervisord.log "/logs/$MIST_TEST_LOG_DIR"
  cp /var/log/error* "/logs/$MIST_TEST_LOG_DIR"
  cd /logs
  git add "$MIST_TEST_LOG_DIR"
  git commit -m "Logs for build $CI_BUILD_ID"
  git push origin master
  echo "Pushed logs and other stuff to https://gitlab.ops.mist.io/mistio/mist.test.logs/tree/master/$MIST_TEST_LOG_DIR"
  if [ $MAYDAY -eq 1 ]; then
    /core.env/bin/ipython tests/check_last_build.py
  fi
fi
exit $exit_code
