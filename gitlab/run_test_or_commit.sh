#!/bin/bash

echo "Executing: $*"
eval "$*"
exit_code=$?

if [ $exit_code -eq 0 ]
then
  echo "Tests run successufully. Returning code $exit_code"
else
  echo "Let's commit!"
  chmod 600 /tests2/gitlab_runner_id_rsa
  eval `ssh-agent -s`
  ssh-add /tests2/gitlab_runner_id_rsa
  ssh-keyscan 104.196.122.66 >> ~/.ssh/known_hosts
  git config --global user.name "mistio-gitlab"
  git config --global user.email gitlab.ops.mist.io@gmail.com
  git clone git@104.196.122.66:mistio/mist.test.logs.git /logs
  mkdir "/logs/mist.core/$CI_BUILD_ID"
  cp /var/log/*-std* "/logs/mist.core/$CI_BUILD_ID"
  cp /var/log/js_console.log "/logs/mist.core/$CI_BUILD_ID"
  cp /var/log/rabbitmq/* "/logs/mist.core/$CI_BUILD_ID"
  cp /var/log/supervisord.log "/logs/mist.core/$CI_BUILD_ID"
  cp /var/log/error* "/logs/mist.core/$CI_BUILD_ID"
  cd /logs
  git add "mist.core/$CI_BUILD_ID"
  git commit -m "Logs for build $CI_BUILD_ID"
  git push origin master
  echo "Pushed logs and other stuff to https://gitlab.ops.mist.io/mistio/mist.test.logs/tree/master/mist.core/$CI_BUILD_ID"
fi
exit $exit_code
