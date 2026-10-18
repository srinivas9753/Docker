# Docker Learning

My hands-on journey learning Docker: notes, small experiments, and projects.

## Prerequisites
- Docker Desktop / Docker Engine
- Git

## Contents
| Folder | Topic | Status |
|---|---|---|
| 01-basics | Containers vs VMs, Dockerfile, build/run | ✅ Completed |
| 02-networking-volumes | Networks, volumes, bind mounts | ⏳ Planned |
| 03-compose | Docker Compose, multi-container apps | ⏳ Planned |
| 04-multi-stage-builds | Smaller, safer images | ⏳ Planned |
| projects | Real projects built with Docker | ⏳ Planned |

## How to run any example
```bash
cd <folder>
docker build -t <name>:1.0 .
docker run --rm <name>:1.0
```
Each folder has its own README with exact steps.

## Cheatsheet
See [cheatsheet.md](cheatsheet.md)

## Author
Srinivas, DevOps Engineer
