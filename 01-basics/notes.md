# Docker Basics: My Notes

Simple notes on what I learned, plus the hands-on steps I actually did.

---

## 1. What is a container?

A container is a **box that holds your app and everything the app needs to run** (code, libraries, settings).

Because everything is inside the box, the app runs the **same way everywhere**: your laptop, a friend's laptop, a server, the cloud. No more "it works on my machine" problems.

> Think of it like a lunch box: the food (app) and the spoon, salt and napkin (libraries and settings) are all packed together.

---

## 2. Containers vs Virtual Machines (VMs)

Both keep apps separated from each other, but they work differently.

| | Virtual Machine | Container |
|---|---|---|
| What it has | A full operating system of its own | Shares the host's OS kernel |
| Size | Gigabytes (~2 GB or more) | Megabytes (Ubuntu image is ~22-78 MB) |
| Startup | Minutes | Seconds |
| Isolation | Very strong | Good, but lighter |
| Portability | Needs a compatible hypervisor | Runs anywhere Docker runs |
| Management | Heavier | Easier and faster |

**Simple way to remember:**
- VM = a separate **house** with its own foundation.
- Container = an **apartment** in one building. Everyone shares the foundation (kernel), but each has a locked door.

### Why are containers lightweight?
- They **don't carry a full operating system**. They borrow the host's kernel.
- They only include what the app needs, nothing extra.

### What a container shares with the host
- **Kernel and system calls**: the host handles CPU, memory and I/O requests.
- **Network stack**: connectivity comes from the host.
- **Files (optional)**: only if you connect them with a bind mount or volume.

### How a container stays isolated
- **Namespaces**: each container gets its own private view of processes, network, files and hostname.
- **cgroups**: put limits on how much CPU, memory and I/O a container can use.

> On Windows and Mac, Docker Desktop quietly runs a small Linux VM in the background, because containers need a Linux kernel.

---

## 3. What is Docker?

- **Containerization** is the idea (packing apps into containers).
- **Docker** is the tool that does it. With Docker you can:
  1. **Build** an image
  2. **Run** the image as a container
  3. **Push** the image to a registry (like Docker Hub) to share it

---

## 4. Docker architecture (who does what)

<img width="1009" height="527" alt="image" src="https://github.com/user-attachments/assets/5ea48be5-ea8d-45e5-949a-4278942922dc" />


| Part | Plain meaning |
|---|---|
| **Docker Client** | What I type commands into (`docker build`, `docker run`) |
| **Docker Daemon (dockerd)** | The brain. Builds images, runs containers, manages networks and volumes. If it stops, Docker stops. |
| **Docker Desktop** | Easy installer for Windows/Mac/Linux. Includes the daemon, client and Compose. |
| **Dockerfile** | A text file with the recipe steps to build an image |
| **Image** | A read-only template (the recipe result). Built in layers. |
| **Container** | A running copy of an image |
| **Registry** | A store for images (Docker Hub is the public one) |

**Image vs container:** image is the recipe, container is the cooked dish. One image can make many containers.

**Layers:** every line in a Dockerfile creates a layer. If I change something and rebuild, Docker only rebuilds the changed layers, so builds are fast.

---

## 5. Docker lifecycle (3 commands to remember)

| Command | What it does |
|---|---|
| `docker build` | Dockerfile → image |
| `docker run` | image → running container |
| `docker push` | image → registry (share it) |

---

## 6. Install check

After installing Docker Desktop, make sure it is running, then test:

```bash
docker --version
docker run hello-world
```

If it prints "Hello from Docker!", everything is working.

**On Linux, if you see "permission denied":**
```bash
sudo systemctl status docker          # is the daemon running?
sudo systemctl start docker           # start it
sudo usermod -aG docker <your-user>   # allow my user to run docker
```
Then log out and log back in.

---

## 7. Hands-on 1: Hello World

Folder: `01-basics/hello-world/`

**app.py**
```python
print("Hello, World from Docker!")
```

**Dockerfile**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```

**What each line means**
- `FROM`: the base image (Python already installed)
- `WORKDIR`: the folder inside the container
- `COPY`: copy my file into the image
- `CMD`: the command that runs when the container starts

**Build and run**
```bash
docker build -t hello-world-py:1.0 .
docker run --rm hello-world-py:1.0
```

Output: `Hello, World from Docker!`

**What does `docker run --rm` do?**
It creates a container from the image, runs it, and **deletes the container** when it finishes. Without `--rm`, the stopped container stays on my machine.

---

## 8. Hands-on 2: Dockerfile basics

Folder: `01-basics/dockerfile-basics/`

**app.py**
```python
import os

name = os.getenv("APP_NAME", "Docker learner")
print(f"Hello, {name}!")
print("Python is running inside a container.")
```

- `os.getenv("APP_NAME", "Docker learner")` reads an **environment variable** called `APP_NAME`. If it is not set, it uses the default `"Docker learner"`.
- An **environment variable** is a value given to the program from outside, so I can change behavior without editing the code.

**Dockerfile**
```dockerfile
FROM python:3.12-slim

ARG APP_VERSION=1.0
ENV APP_NAME="Srinivas"

WORKDIR /app
COPY app.py .

RUN echo "Building version ${APP_VERSION}"

CMD ["python", "app.py"]
```

**.dockerignore**
```
__pycache__/
*.pyc
.git
.env
```

**Build and run**
```bash
docker build -t dockerfile-basics:1.0 .
docker run --rm dockerfile-basics:1.0
docker run --rm -e APP_NAME="DevOps" dockerfile-basics:1.0
docker build --build-arg APP_VERSION=2.0 -t dockerfile-basics:2.0 .
```

**Dockerfile instructions cheat table**

| Instruction | Plain meaning | Example |
|---|---|---|
| `FROM` | Starting image | `FROM python:3.12-slim` |
| `WORKDIR` | Working folder inside the container | `WORKDIR /app` |
| `COPY` | Copy files from my PC into the image | `COPY app.py .` |
| `RUN` | Run a command while **building** | `RUN echo "hi"` |
| `ENV` | Variable available while the container **runs** | `ENV APP_NAME="Srinivas"` |
| `ARG` | Variable available only while **building** | `ARG APP_VERSION=1.0` |
| `CMD` | Default command when the container starts | `CMD ["python", "app.py"]` |

**Key points**
- `ARG` = build time only. `ENV` = also available at run time.
- `-e` at run time **overrides** `ENV` from the Dockerfile.
- `.dockerignore` keeps unwanted files out of the image.

---

## 9. Optional: Ubuntu-based Dockerfile (for learning `apt`)

The original example used Ubuntu. It works, but the image is bigger (~467 MB vs ~120 MB for `python:3.12-slim`).

```dockerfile
FROM ubuntu:24.04
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 && \
    rm -rf /var/lib/apt/lists/*

COPY app.py .
ENV NAME="Srinivas"
CMD ["python3", "app.py"]
```

Improvements over the basic version:
- Pin the version (`ubuntu:24.04`, not `latest`) so builds stay the same.
- Install packages **before** copying code, so Docker reuses the cache when only code changes.
- Clean the apt cache to keep the image small.

---

## 10. Push my image to Docker Hub

1. Create an account at hub.docker.com (the username is lowercase).
2. Log in from the terminal (use an access token as the password if asked):
   ```bash
   docker login
   ```
3. Tag the image with my username:
   ```bash
   docker tag hello-world-py:1.0 <username>/hello-world-py:1.0
   ```
4. Push:
   ```bash
   docker push <username>/hello-world-py:1.0
   ```
5. Test like a stranger would:
   ```bash
   docker rmi <username>/hello-world-py:1.0
   docker run --rm <username>/hello-world-py:1.0
   ```

Shortcut: build with the final name directly.
```bash
docker build -t <username>/hello-world-py:1.0 .
```

**Rules**
- Public images are visible to everyone. Never put passwords, keys or `.env` files inside.
- Use version tags (`1.0`, `2.0`) instead of only `latest`.

---

## 11. Push my work to GitHub

```bash
git add .
git commit -m "add basics notes"
git push
```

Commits stay on my computer (in the hidden `.git` folder) until I run `git push`.

---

## 12. Commands I used

```bash
docker build -t name:tag .          # build an image
docker run --rm name:tag            # run, then delete the container
docker run -e KEY=value name:tag    # run with an environment variable
docker images                       # list images
docker ps -a                        # list all containers
docker tag name:tag user/name:tag   # add a Docker Hub name
docker push user/name:tag           # upload to Docker Hub
docker login                        # sign in to Docker Hub
```

---

## 13. Errors I hit and the fix

| Problem | Fix |
|---|---|
| `&&` or `{a,b}` errors in the terminal | I was in PowerShell. Use Git Bash, or the PowerShell version of the commands. |
| `requested access to the resource is denied` on push | Image name must start with my Docker Hub username, and I must be logged in. |
| `code: command not found` | In VS Code: `Ctrl + Shift + P` → "Shell Command: Install 'code' command in PATH". |
| Dockerfile saved as `Dockerfile.txt` | It must have **no extension**. |
| Docker commands fail | Docker Desktop is not running. Start it first. |

---


## Next

- Image layers and caching
- `02-networking-volumes`: bridge network and volumes labs
