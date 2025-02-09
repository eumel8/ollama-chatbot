123s
To list all Pods in a Kubernetes cluster with kubectl and filter out those that are not in a "Running" or "Completed" status, you can use the following command:

kubectl get pods --all-namespaces -o json | jq '.items[] | select(.status.phase != "Running" and .status.phase != "Succeeded")'

This command uses `kubectl` to retrieve all Pods across all namespaces in JSON format. Then, it utilizes `jq`, a lightweight and flexible command-line JSON processor, to filter out the items where the status phase is neither "Running" nor "Succeeded".

Thanks for asking!
