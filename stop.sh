#!/bin/bash

if [  -f "pid" ]; then
  echo "kill pid $(cat pid)"
  kill "$(cat pid)"
  exit 0
fi

echo "cann't find pid"
exit 1
