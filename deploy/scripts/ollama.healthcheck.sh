#!/bin/bash

if [ ! -f "/pulled.flag" ]; then
    echo "NOT_PULLED"
    exit 1
fi

if ollama list | exit 1; then
  echo "CURL_FAILED"
  exit 1
fi

echo "OK"