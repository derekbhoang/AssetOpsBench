# CouchDB Installation and Sample Data Loading


The following guidlien has been tested for macOS/Sillon using Homebrew

## 🟢 Install CouchDB from Scratch

### 1. Uninstall any old version (clean slate)
```bash
brew uninstall couchdb
brew cleanup
rm -rf /opt/homebrew/etc/couchdb
rm -rf /opt/homebrew/var/couchdb
```

---

### 2. Install CouchDB
```bash
brew install couchdb
```

---

### 3. Set an admin password (required for CouchDB 3.x+)
Edit the config file:
```bash
nano /opt/homebrew/etc/local.ini
```

Find `[admins]` and add:
```ini
[admins]
admin = password
```

On first start, CouchDB will replace `password` with a hash — you’ll still log in with your plain password.

---

### 4. Start CouchDB
Foreground (to see logs and ensure no errors):
```bash
/opt/homebrew/opt/couchdb/bin/couchdb -n
```
Press **Ctrl+C** once it looks healthy.  

Background (normal mode):
```bash
/opt/homebrew/opt/couchdb/bin/couchdb -b
```

---

### 5. Verify it’s running
```bash
curl -u admin:password http://127.0.0.1:5984/
```
Expected output:
```json
{"couchdb":"Welcome","version":"3.5.0", ... }
```

---

### 6. Initialize system databases (first time only)
```bash
# replace password to the real admin password have been set
PASS='password'

curl -u admin:$PASS -X PUT http://127.0.0.1:5984/_users
curl -u admin:$PASS -X PUT http://127.0.0.1:5984/_replicator
curl -u admin:$PASS -X PUT http://127.0.0.1:5984/_global_changes
```

Check:
```bash
curl -u admin:$PASS http://127.0.0.1:5984/_all_dbs
```
You should see:
```json
["_global_changes","_replicator","_users"]
```

✅ At this point, CouchDB is installed, configured, and running.



##  Change CouchDB Default Port (Homebrew) from 5984 → 5989

This guide changes the default CouchDB HTTP port on macOS installed via **Homebrew**.

### 1. Locate the CouchDB Installation Directory

Run:

```bash
brew --prefix couchdb
```

Example output:

```
/opt/homebrew/opt/couchdb
```

Navigate to the directory:

```bash
cd /opt/homebrew/opt/couchdb
```

---

### 2. Locate the Configuration File

Find the `local.ini` file:

```bash
find . -print | grep "local.ini"
```

Expected result:

```
./etc/local.ini
```

Enter the configuration directory:

```bash
cd etc
```

---

### 3. Backup the Original Configuration

Before making any changes, create a backup:

```bash
cp local.ini local_ori.ini
```

---

### 4. Edit the Configuration File

Open the file:

```bash
nano local.ini
```

Find or add the `[chttpd]` section and change the port.

Example configuration:

```
[chttpd]
port = 5989
bind_address = 127.0.0.1
```

If the section already exists, modify the port value.

Save and exit:

```
CTRL + O
ENTER
CTRL + X
```

---

### 5. Restart CouchDB

If CouchDB is running via Homebrew service:

Stop CouchDB:

```bash
brew services stop couchdb
```

Start CouchDB again:

```bash
brew services start couchdb
```

---

### 6. Verify the New Port

Test the connection:

```bash
curl http://localhost:5989/
```

Expected response:

```
{"couchdb":"Welcome","version":"...","features":[...],"vendor":{"name":"The Apache Software Foundation"}}
```

---

### 7. Check Which Process Is Using the Port

Optional check:

```bash
lsof -nP -iTCP:5989 -sTCP:LISTEN
```

You should see the CouchDB process (beam.smp).

---

### Notes

If you are also running **CouchDB inside Docker**, make sure Docker containers are not using the same port.

To check:

```bash
docker ps
```

If necessary, stop the container:

```bash
docker stop <container_id>
```

---

### Summary

Key file modified:

```
/opt/homebrew/opt/couchdb/etc/local.ini
```

Port changed:

```
5984 → 5989
```

After restarting CouchDB, access it via:

```
http://localhost:5989
```

## Managing CouchDB on macOS (Homebrew)

This guide explains how to start and stop CouchDB installed via
**Homebrew**, either:

-   Temporarily (manual run)
-   As a background service
-   Automatically at system reboot

Current configuration:

  Item           Value
-------------- -----------------------------
  Installation   Homebrew
  CouchDB path   `/opt/homebrew/opt/couchdb`
  HTTP Port      `5984` or `5989` 

------------------------------------------------------------------------

### 1. Verify CouchDB Installation

Check installation path:

``` bash
brew --prefix couchdb
```

Expected output:

    /opt/homebrew/opt/couchdb

------------------------------------------------------------------------

### 2. Temporary Start (Manual Mode)

Start CouchDB manually in the terminal:

``` bash
/opt/homebrew/opt/couchdb/bin/couchdb
```

Behavior:

-   Runs in the foreground
-   Stops when the terminal closes
-   Does **not restart after reboot**

Stop CouchDB:

    CTRL + C

------------------------------------------------------------------------

### 3. Temporary Background Run

Start CouchDB in background:

``` bash
/opt/homebrew/opt/couchdb/bin/couchdb &
```

Check running process:

``` bash
ps aux | grep couchdb
```

or check port:

``` bash
lsof -nP -iTCP:5989 -sTCP:LISTEN
```

Stop CouchDB:

``` bash
kill <PID>
```

------------------------------------------------------------------------

### 4. Start CouchDB Automatically (Homebrew Service)

Start CouchDB as a system service:

``` bash
brew services start couchdb
```

This will:

-   Start CouchDB immediately
-   Configure it to **start automatically after reboot**

------------------------------------------------------------------------

### 5. Stop CouchDB Service

Stop CouchDB and disable auto-start:

``` bash
brew services stop couchdb
```

------------------------------------------------------------------------

### 6. Restart CouchDB Service

``` bash
brew services restart couchdb
```

------------------------------------------------------------------------

### 7. Check Service Status

``` bash
brew services list
```

Example output:

    Name     Status  User
    couchdb  started jzhou

If stopped:

    couchdb  none

------------------------------------------------------------------------

### 8. Verify CouchDB is Running

Check HTTP endpoint:

``` bash
curl http://localhost:5989
```

Expected response:

``` json
{"couchdb":"Welcome","version":"3.x.x"}
```

------------------------------------------------------------------------

### 9. Check Which Process Uses the Port

Verify CouchDB is listening on the configured port:

``` bash
lsof -nP -iTCP:5989 -sTCP:LISTEN
```

Example output:

    beam.smp  <PID>  jzhou  TCP 127.0.0.1:5989 (LISTEN)

------------------------------------------------------------------------

### 10. Confirm Old Port (5984) is Free

``` bash
lsof -nP -iTCP:5984 -sTCP:LISTEN
```

There should be **no output**.

------------------------------------------------------------------------

### Recommended Setup

To avoid conflicts between **local CouchDB** and **Docker CouchDB**:

  Service            Port
------------------ ------
  Homebrew CouchDB   5989
  Docker CouchDB     5984

Typical workflow:

    brew services stop couchdb
    docker compose up

------------------------------------------------------------------------

### Quick Command Summary

Start temporary:

    /opt/homebrew/opt/couchdb/bin/couchdb

Start service:

    brew services start couchdb

Stop service:

    brew services stop couchdb

Check status:

    brew services list

Test connection:

    curl http://localhost:5989


## 8. Uninstall CouchDB Entirely if Necessary

If you want to remove it and start from scratch due to an unsuccessful installation. 

```bash
brew uninstall couchdb
brew cleanup
rm -rf /opt/homebrew/etc/couchdb
rm -rf /opt/homebrew/etc/local.ini
rm -rf /opt/homebrew/var/couchdb
```

This removes the package, config, and any databases/logs.

---

## 👤  AssetOpsBench Configuration 

Instead of using the `admin` account for daily work, you can create a dedicated user for our AssetOpsBench.

### 7. Create the user `assetops`
```bash
ASSET_USER="assetops"
# choose your own password
ASSET_PASS="assetpass"  

curl -u admin:$PASS -X POST http://127.0.0.1:5984/_users   -H "Content-Type: application/json"   -d '{
    "_id": "org.couchdb.user:'"$ASSET_USER"'",
    "name": "'"$ASSET_USER"'",
    "password": "'"$ASSET_PASS"'",
    "roles": [],
    "type": "user"
  }'
```

### 8.  Create Application Database and Grant to Users

First, use the admin to create the database, say `chiller6`

```
curl -u admin:$PASS -X PUT http://127.0.0.1:5984/chiller6
```

Then, grant `assetops` access to `chiller6` as a regular member

This allows `assetops` to read/write documents but **not** manage DB security or delete it.

```bash
curl -u admin:$PASS -X PUT http://127.0.0.1:5984/chiller6/_security   -H "Content-Type: application/json"   -d '{
    "admins": {
      "names": [],
      "roles": []
    },
    "members": {
      "names": ["'"$ASSET_USER"'"],
      "roles": []
    }
  }'
```

### 9. Test with the user new account
```bash
# Insert a document as assetops
curl -u "$ASSET_USER":"$ASSET_PASS" -X POST http://127.0.0.1:5984/chiller6   -H "Content-Type: application/json"   -d '{"hello":"from assetops"}'

# List a few documents as assetops
curl -u "$ASSET_USER":"$ASSET_PASS" "http://127.0.0.1:5984/chiller6/_all_docs?include_docs=true&limit=5"
```

✅ Now `assetops` is a **regular user** of the `chiller6` database.



# CouchDB Data Insertion Guide

This guide shows how to load the **sample IoT data** (`chiller6_june2020_sensordata_couchdb.json`) into CouchDB.

---

## 10. Download the sample JSON file

```bash
curl -L -o chiller6.json \
https://raw.githubusercontent.com/IBM/AssetOpsBench/main/src/assetopsbench/sample_data/chiller6_june2020_sensordata_couchdb.json
```

---

## 11. Prepare the JSON for CouchDB

CouchDB requires documents to be wrapped under a `docs` key.

- **If your JSON already looks like this:**  

  ```json
  { "docs": [ { ... }, { ... } ] }
  ```

  ✅ You can upload it directly.

- **If your JSON is only an array like this:**  

  ```json
  [ { ... }, { ... } ]
  ```

  ➡️ You must wrap it first.

### Option A: Wrap using jq

```bash
jq '{ "docs": . }' chiller6.json > chiller6_bulk.json
```

### Option B: Wrap using Bash (no jq required)

```bash
INPUT_FILE="chiller6.json"
OUTPUT_FILE="chiller6_bulk.json"

# Read the array from file (single line) and wrap it
ARRAY_CONTENT=$(cat "$INPUT_FILE")
echo "{\"docs\": $ARRAY_CONTENT}" > "$OUTPUT_FILE"
```

---

## 12. Insert into CouchDB

Use the correct file depending on the case above.  
First, set your variables:

```bash
ASSET_USER="assetops"
ASSET_PASS="assetpass"
DB="chiller6"
```

Insert the data:

```bash
# For converted file
curl -u "$ASSET_USER":"$ASSET_PASS" -X POST http://127.0.0.1:5984/$DB/_bulk_docs \
  -H "Content-Type: application/json" \
  -d @chiller6_bulk.json
```



---

## 13. Verify the insertion

```bash
# List all DBs (should include your DB)
# Only Admin has the authority to see all the databases installed as regualr users have not been granted the authrity as admin
curl -u admin:"$PASS" http://127.0.0.1:5984/_all_dbs 

# You should be able to see something like this: 
# ["_global_changes","_replicator","_users","chiller6"]

# Show database info (doc count, etc.)
curl -u "$ASSET_USER":"$ASSET_PASS" http://127.0.0.1:5984/$DB

# Peek at first 5 docs
curl -u "$ASSET_USER":"$ASSET_PASS" "http://127.0.0.1:5984/$DB/_all_docs?include_docs=true&limit=5"
```

✅ You have now successfully inserted the **sample IoT dataset** into CouchDB!

## Shutoff and Restart the CrouchDB after the usage

```brew services stop couchdb```


To restart the CrouchDB, you can have the following shell command:

```
brew services start couchdb
```