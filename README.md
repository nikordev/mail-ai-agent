# mail-ai-agent

This is a simple test implementation of an AI agent for working with mail.

This code is intended to demonstrate how the RAG agent works 
with the MCP server using a simple example of working with mail.

## DEV

Copy and prepare environment variables

```
cp .env.example .env
```

```
docker compose -f docker-compose.dev.yml up -d --force-recreate 
```

Rebuild:

```
docker compose -f docker-compose.dev.yml up -d --force-recreate --build 
```

## PROD

Move to deploy directory

```
cd deploy
```

Copy and prepare environment variables

```
cp .env.example .env
```

Start containers

```
docker compose -f docker-compose.yml up
```