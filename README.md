# Project-1-kdasari1

# Procedure

### Step 1: Install minikube and add it to path variables

### Step 2: Run `minikube start`
`This computer doesn't have VT-X/AMD-v enabled. Enabling it in the BIOS is mandatory`
Run `minikube start --driver=docker` works

1. Single docker container acts as a kubernetes node and runs kubernetes components as processes (cluster) inside that single container.
2. `docker exec -it minikube bash` \\ `ps aux | grep kube` to check the running processes
3. It sets up the Kubernetes API server and configured your local kubectl to connect to it.
4. To check this:
   `kubectl version --client`
   `kubectl cluster-info`
   `kubectl get nodes`

### Step 3: Setup yaml file for deployment of zookeeper pod and service and execute `kubectl apply -f ./zookeeper-setup.yaml`
`kubectl get pods` to check if the pod is running or not

# Other validation steps (Running a temporary pod to check if the service is reachable or not)

1. `kubectl run test-pod --image=busybox --restart=Never -- sleep 3600`
2. `kubectl exec -it test-pod -- sh`
3. `telnet zookeeper-service 2181`
4. `kubectl delete pod test-pod`

### Step 4: Similarily follow the steps for setting up kafka-setup.yaml

### Step 5: Implementing neo4j in this setup

`Here we will deploy a neo4j standalone instance to local kubernetes cluster using Neo4j Helm chart. The service file is a standard kubernetes manifest for defining how a set of pods is exposed withing the cluster or to external clients whereas neo4j-values configures the Neo4j instance. `

1. Install helm using Chocolatey in windows `choco install kubernetes-helm`
2. Check installation with `helm version
3. Add Neo4j Heml Chart Repository `helm repo add neo4j https://neo4j.github.io/helm-charts`
4. Update the repo `helm repo update`
5. Write the required configuration code in `neo4j-values.yaml` and run `helm install my-neo4j-release neo4j/neo4j -f neo4j-values.yaml`
6. To check which config kubernetes is using `kubectl config current-context`
7. Create service using `kubectl apply -f neo4j-service.yaml`

# Validation steps

1. `kubectl run debug-pod --rm -it --image=busybox -- /bin/sh` (pod is automatically deleted because of --rm flag)
2. `wget --spider my-neo4j-release:7474`

### Step - 6: Connect neo4j and kafka

1. Create a .yaml file with service and deployment of connector pod and `kubectl apply -f kafka-neo4j-connector.yaml`
2. Make sure the service you are exposing in kafka broker setup is same as in connector.
3. Check for validation `kubectl logs -f deployment/kafka-neo4j-connector`
4. Other validation commnds: `kubectl logs kafka-deployment-<pod>`
5. Delete any service and deployments before rebuilding

### Step - 7:

1. Forward the ports of kafka neo4j to test from the localhost.
1. Run `producer.py` and check if all the nodes and relationships are created in graph database by connecting from the localhost.
1. Run `tester.py` to test the code
