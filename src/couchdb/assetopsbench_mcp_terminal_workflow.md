# AssetOpsBench MCP System --- Terminal Workflow Reference

## 1. Start CouchDB (Docker)

Run once:

``` bash
docker compose -f src/couchdb/docker-compose.yaml up -d
```

Verify:

``` bash
curl http://localhost:5984/
```

Expected response:

``` json
{"couchdb":"Welcome","version":"3.x.x"}
```

------------------------------------------------------------------------

# 2. Open Multiple Terminals (or Tabs)

On Mac Terminal:

New tab:

    ⌘ + T

You will need **6 terminals**.

------------------------------------------------------------------------

# 3. Start MCP Servers

Each terminal runs **one server**.

### Terminal 1 --- Utilities MCP

``` bash
uv run utilities-mcp-server
```

### Terminal 2 --- IoT MCP

``` bash
uv run iot-mcp-server
```

### Terminal 3 --- FMSR MCP

``` bash
uv run fmsr-mcp-server
```

### Terminal 4 --- TSFM MCP

``` bash
uv run tsfm-mcp-server
```

### Terminal 5 --- Work Order MCP

``` bash
uv run wo-mcp-server
```

------------------------------------------------------------------------

# 4. Run the LLM Workflow

Open another terminal.

Run:

``` bash
uv run plan-execute "What assets are at site MAIN?"
```

This command will:

1.  Call the LLM (WatsonX)
2.  Query MCP servers
3.  Retrieve data from CouchDB
4.  Return results

------------------------------------------------------------------------

# 5. Architecture Overview

    plan-execute
         │
         ▼
    LLM Backend (WatsonX / LiteLLM)
         │
         ▼
    MCP Servers
     ├─ utilities
     ├─ iot
     ├─ fmsr
     ├─ tsfm
     └─ workorder
         │
         ▼
    CouchDB (Docker)

------------------------------------------------------------------------

# 6. Stopping Servers

Press:

    Ctrl + C

in each terminal.

------------------------------------------------------------------------

# 7. Helpful Checks

### See running containers

``` bash
docker ps
```

### See running MCP processes

``` bash
ps aux | grep mcp
```

### Check CouchDB

``` bash
curl http://localhost:5984/_all_dbs
```

------------------------------------------------------------------------

# 8. Important Notes

-   You **do NOT need to activate `.venv`** because you use:

``` bash
uv run
```

-   Each MCP server **runs continuously** and waits for requests.
-   The `plan-execute` command **uses the running servers**.

------------------------------------------------------------------------

# 9. Minimal Terminal Layout

    Terminal 1  utilities-mcp-server
    Terminal 2  iot-mcp-server
    Terminal 3  fmsr-mcp-server
    Terminal 4  tsfm-mcp-server
    Terminal 5  wo-mcp-server
    Terminal 6  plan-execute
