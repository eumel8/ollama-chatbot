You can use `kubectl get pods --all-namespaces -o json | jq '.items[] | select(.status.phase != "Running" and .status.phase != "Completed")'` to list all Pods whose status is not Running or Completed. This command filters the output of `kubectl get pods` using `jq`, a JSON processor, to only include Pods that are in non-Running and non-Completed states.

Thanks for asking!
