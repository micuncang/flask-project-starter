#!/bin/bash

if [  -f "pid" ]; then
  cat pid | xargs echo 'kill pid'
  cat pid | xargs kill
  exit 0
fi

echo "cann't find pid"
exit 1
