
# Docker Stop & Management Cheat Sheet

This guide summarizes common commands to stop Docker containers or Docker services.

---

# 1. Stop a Specific Container

First list running containers:

```bash
docker ps
```

Example output:

```
CONTAINER ID   IMAGE      NAME
abc123         couchdb    my-couchdb
```

Stop a container by **name**:

```bash
docker stop my-couchdb
```

or by **container ID**:

```bash
docker stop abc123
```

---

# 2. Stop All Running Containers

Stop every running container:

```bash
docker stop $(docker ps -q)
```

Explanation:

- `docker ps -q` lists IDs of running containers
- `docker stop` stops them

---

# 3. Stop Containers from Docker Compose

If the containers were started with **Docker Compose**:

Stop and remove containers:

```bash
docker compose down
```

Older syntax:

```bash
docker-compose down
```

If you only want to **stop containers but keep them**:

```bash
docker compose stop
```

Example for a specific compose file:

```bash
docker compose -f src/couchdb/docker-compose.yaml down
```

---

# 4. Stop Docker Desktop (Mac)

### Option A – From Menu

1. Click the **Docker whale icon** in the macOS menu bar

2. Choose **Quit Docker Desktop**

   How to Shut Off Rancher Desktop (UI Method)

   This guide explains the simplest way to stop Rancher Desktop and all Kubernetes containers from the macOS UI.

   ---

   ### Step 1: Locate Rancher Desktop in the macOS Menu Bar

   At the **top of your Mac screen**, find the application menu labeled:

   ```
   Rancher Desktop
   ```

   This menu appears when the Rancher Desktop application is running.

   ---

   ### Step 2: Quit Rancher Desktop

   Click:

   ```
   Rancher Desktop → Quit Rancher Desktop
   ```

   Or use the keyboard shortcut:

   ```
   Command (⌘) + Q
   ```

   This will stop:

   - The local **Kubernetes cluster (k3s)**
   - All **k8s_* containers**
   - The **container runtime**

   ---

   ### Step 3: Verify Everything Stopped

   Open Terminal and run:

   ```bash
   docker ps
   ```

   Expected result:

   ```
   Cannot connect to the Docker daemon
   ```

   This confirms Rancher Desktop and the container runtime are stopped.

   ---

   ### Optional: Restart Rancher Desktop

   To start it again:

   1. Open **Applications**
   2. Click **Rancher Desktop**

   Or run:

   ```bash
   open -a "Rancher Desktop"
   ```

   ---

   ### Notes

   Stopping Rancher Desktop will immediately stop all containers started by its Kubernetes environment.  
   This is safe and commonly used when debugging local services or port conflicts.

### Option B – From Terminal

```bash
killall Docker
```

---





# 5. Verify Docker Status

Check running containers:

```bash
docker ps
```

If nothing appears, all containers are stopped.

---

# 6. Useful Debugging Commands

View running containers:

```bash
docker ps
```

View all containers:

```bash
docker ps -a
```

View logs of a container:

```bash
docker logs <container_name>
```

Enter a running container:

```bash
docker exec -it <container_name> bash
```

Check container ports:

```bash
docker port <container_name>
```

---

# Quick Summary

Stop one container

```bash
docker stop <container>
```

Stop all containers

```bash
docker stop $(docker ps -q)
```

Stop compose stack

```bash
docker compose down
```

Stop Docker Desktop

```bash
killall Docker
```
