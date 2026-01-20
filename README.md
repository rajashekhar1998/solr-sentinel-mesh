# Solr Sentinel Mesh

**Solr Sentinel Mesh** is a distributed coordination layer designed to retrofit High Availability (HA) and automated failover onto legacy Apache Solr clusters without introducing the operational complexity of ZooKeeper.

It eliminates the Single Point of Failure (SPOF) inherent in independent Solr node deployments by implementing a peer-to-peer **SWIM Gossip Protocol**.

## 🏗 The Problem: Legacy Fragility

Enterprise Solr environments often scale to 100+ independent nodes ("User-Managed" mode). In these legacy configurations:

* **No Central Coordination:** Nodes are unaware of one another.
* **Fragile Clients:** Frontend applications rely on static IPs. If a node fails, the application errors out.
* **Zombie Nodes:** Standard load balancers fail to detect "gray failures"—nodes that accept TCP connections but are unresponsive due to JVM Garbage Collection (GC) pauses or disk I/O saturation.

## 🛡 The Solution: Partitioned Mesh Topology

We introduce a **Sentinel** agent on every node using the **Sidecar Pattern**.

1. **The Sentinel Proxy (Port 8984):** Intercepts traffic and performs "Deep Health Checks" on the local Solr instance (Port 8983).
2. **Failover Groups:** Nodes are logically partitioned into groups (e.g., "Sister Stores"). A node in `Group A` will **only** failover to other peers in `Group A`, preventing split-brain routing across mismatched datasets.
3. **SWIM Gossip Protocol:** Nodes exchange health information via UDP. This allows the cluster to detect failures in  time, regardless of cluster size.

## ⚡ Key Features

* **Zero-Copy Streaming:** Uses `httpx` and `asyncio` to stream large Solr JSON responses (10MB+) without buffering them in memory, ensuring <2ms latency overhead.
* **Split-Brain Recovery:** Prioritizes Availability (AP). In the event of a network partition, nodes operate independently and reconcile automatically when connectivity is restored.
* **Deep Metric Inspection:** Queries Solr's JMX/Metrics API to detect:
* `solr.jvm.memory.heap.usage` > 90%
* `solr.core.request_times.p99` > 2000ms


* **Timeline Visualization:** Includes tooling to generate HTML Gantt charts of cluster state transitions during incidents.

## 📂 Project Structure

solr-sentinel-mesh/
├── src/
│   └── solr_sentinel/
│       ├── mesh/           # SWIM Protocol (UDP Transport, Membership State)
│       ├── proxy/          # FastAPI Data Plane (Smart Routing Logic)
│       ├── monitors/       # Async Solr Metrics Poller
│       └── observability/  # Structured Logging & Tracing
├── tools/
│   └── visualize_timeline.py # Log analyzer (Generates HTML reports)
├── config/
│   └── settings.yaml       # Group ID and Peer Seeds
├── docker-compose.yml      # Local simulation of a 2-node failover group
└── README.md

## 🚀 Quick Start (Simulation)

This project includes a Docker Compose configuration that simulates a **Failover Group** with two nodes (Primary and Secondary) to demonstrate the resilience patterns locally.

### 1. Start the Mesh

```bash
docker-compose up --build

```

*This starts 2 Solr nodes (ports 8983, 8993) and 2 Sentinel Sidecars (ports 8984, 8994).*

### 2. Verify Normal Operation

Query the Primary Node via the Sentinel Proxy.

```bash
curl "http://localhost:8984/solr/admin/info/system"
# Response: 200 OK (Served by Node 1)

```

### 3. Trigger a Failover

Simulate a "Zombie Node" failure by pausing the Solr container (Sentinel remains up).

```bash
docker pause solr-node-1

```

### 4. Observe Automatic Recovery

Within ~2 seconds, the Sentinel on Node 1 will detect the failure via metrics/timeout, mark itself as `SUSPECT`, and gossip this state. Subsequent requests are transparently routed to Node 2.

```bash
curl "http://localhost:8984/solr/admin/info/system"
# Response: 200 OK (Served by Node 2 - Check headers for X-Served-By)

```

## 📊 Observability & Timelines

Distributed systems are notoriously difficult to debug. We solve this by enforcing **Structured Causal Logging**.

To generate a timeline report of the failover event:

```bash
python tools/visualize_timeline.py --log-file=sentinel.json --output=report.html

```

## 🛠 Configuration

Configuration is managed via environment variables.

| Variable | Description | Example |
| --- | --- | --- |
| `SENTINEL_NODE_ID` | Unique Identity | `server-prod-01` |
| `SENTINEL_GROUP_ID` | **Critical:** Defines the failover boundary | `inventory-shard-a` |
| `SENTINEL_SOLR_PORT` | Local Solr Port | `8983` |
| `SENTINEL_PROXY_PORT` | Sentinel Listening Port | `8984` |
| `SENTINEL_PEERS` | Seed nodes for gossip bootstrap | `192.168.1.5:7946` |

## 📦 Deployment Options

### Docker / Kubernetes

Run as a sidecar container sharing the `localhost` network namespace with Solr.

### Bare Metal / Legacy

For environments without Docker, compile a standalone binary using PyInstaller:

```bash
pyinstaller --onefile --name sentinel src/solr_sentinel/main.py
# Copy./dist/sentinel to /usr/local/bin/

```

## 📜 License

MIT