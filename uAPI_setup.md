# ERIGrid 2.0 JRA3 - Universal API Setup 

## Requirements

- any UNIX/Linux-based system

## Steps


### Transports

The following transports, i.e., lab-coupling tools are currently supported:

- VILLASnode
- JaNDER
- Lablink

Please follow their detailed individual instructions below.

These instructions expose the universal API, as defined in [specification](https://github.com/ERIGrid2/JRA-3.1-api) at `http://localhost:8080`.


#### 1. VILLASnode

##### 1. Configuration

- Create a new directory for the VILLASnode configuration:
    - `mkdir -p /home/erigrid/tws1/villas`
    - `cd /home/erigrid/tws1/villas`

- Create a `node.conf` file with the following contents:
    - `nano node.conf`

```conf
http = {
	port = 8080
}

nodes = {
	api_node = {
		type = "api"

		in = {
			signals = (
				{ name = "sig1", type = "float", unit = "V" },
				{ name = "sig2", type = "float", unit = "A" },
				{ name = "sig3", type = "float", unit = "A" }
			)
		}
	}

	signal_node = {
		type = "signal"

		signal = "mixed"
		values = 5
		rate = 1
	}

	udp_node = {
		type = "socket",
        layer = "udp",

		in = {
			signals = (
				{ name = "sig1", type = "float", unit = "V" },
				{ name = "sig2", type = "float", unit = "A" },
				{ name = "sig3", type = "float", unit = "A" }
			)
            
            address = "*:12000"
		}
        
        out = {
            address = "name-of-remote-peer:12000"
        }
	}
}

paths = (
	{
		in = [
			# "signal_node",
			"api_node"
		],
		out = [
			"udp_node"
		]
		hooks = (
			"print"
		)
	},
	{
		in = [
			"udp_node"
		]
		out = [
			"api_node"
		]
		hooks = (
			"print"
		)
	}
)
```

##### 2. Run

- Start the VILLASnode transport with the new configuration file:
    - `docker run --privileged --volume /home/erigrid/tws1/villas/node.conf:/etc/villas/node.conf registry.git.rwth-aachen.de/acs/public/villas/node  -- /etc/villas/node.conf`


#### 2. JaNDER
1. Install Ubuntu on your machine.
2. Run the following commands to set up Docker on your machine and clone the necessary files:

```
# Update machine
$ sudo apt update -y
$ sudo apt upgrade -y
# Remove previous Docker releases
$ sudo apt-get remove docker docker-engine docker.io containerd runc
# Install Docker and required packages
$ sudo apt-get install ca-certificates curl gnupg lsb-release
$ sudo mkdir -m 0755 -p /etc/apt/keyrings
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
$ echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
# Clone the software repository
$ git clone https://github.com/ERIGrid2/JRA-3.1-JaNDER-API.git
$ cd JRA-3.1-JaNDER-API
$ mkdir - p files/cert
```

> NOTE: The above steps assume that the user has administrative privileges on the machine. If not, some of the commands may require sudo privileges.

3. Next, you'll need to upload the `ca.pem`, `XX.pem`, and `XX-key.pem` certificates to the `files/cert` directory. If you don't have these certificates, please contact RSE, and they will generate them for you.
4. Modify the `.env` file by changing the value of the `NAMESPACE` field to either the name you want to use during experiments (e.g., `demo4`) or the name of your organization if you are running local tests. CAUTION: This field is case sensitive. The default value for `NAMESPACE` is `RSE`, but in the following example, the `${NAMESPACE}` variable is used. Additionally, change the value of the `HOST_NAME_RI` field to `localhost` (`HOST_NAME_RI=localhost`).

```
JANDER_VERSION=1.1.0
PROTOCOL=HTTPS
SERVICE_NAME=JaNDER
PORT_RI=9479
HOST_NAME_RI=localhost
PORT_WEB=8080
NAMESPACE=${NAMESPACE}
REMOTE_ADDRESS=https://ec2-54-72-205-227.eu-west-1.compute.amazonaws.com/redis
```

5. Open the `docker-compose.yaml` file and rename the file at lines 24 and 27 with the name of your organization's certificates, i.e.,

```
secrets:
  # main org certificate
  main-cert:
    file: files/cert/ca.pem
  # your org certificate
  org-cert:
    file: files/cert/RSE.pem --> ${NAME_INSTITUTION}.pem
  # main org key
  org-key:
    file: files/cert/RSE-key.pem --> ${NAME_INSTITUTION}-key.pem
```

6. You can now build your Docker Compose by running the following command:

```
$ sudo docker compose up - d --build
```


## Testing & Validation
### JaNDER
If the build process is successful, running the command `sudo docker ps` should give you the following output:
bash

```
CONTAINER ID   IMAGE                          COMMAND                  CREATED         STATUS         PORTS                                                                                  NAMES
b54374fe0af7   jra-31-jander-api-ri-service   "./entrypoint_redisR…"   4 minutes ago   Up 7 seconds   0.0.0.0:6379->6379/tcp, :::6379->6379/tcp, 0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   rse
ubuntu@ubuntu-20:~/JRA-3.1-JaNDER-API$ sudo docker logs b54374fe0af7
```

This output shows that the JaNDER API services are running correctly. The PORTS column shows that port 6379 and 8080 are mapped to 0.0.0.0 (i.e., all network interfaces) on the host machine.

### With the command line
- Get all available channels
    - `curl -X GET http://localhost:8080/channels`

- Get node configuration
    - `curl -v http://localhost:8080/api/v2/universal/api_node/config`
     
- Get list of signals provided by the node
    - `curl -v http://localhost:8080/api/v2/universal/api_node/signals`
     
- Get current value of a signal by its ID
    - `curl -v http://localhost:8080/api/v2/universal/api_node/signal/ramp/state`

- To set values - check the python scripts
