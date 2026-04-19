#!/bin/bash

/bin/ollama serve &
pid=$!
sleep 5
ollama pull llama3
ollama pull nomic-embed-text
touch /pulled.flag
wait $pid