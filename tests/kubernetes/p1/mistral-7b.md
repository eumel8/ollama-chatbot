62s
To list all Pods in a Kubernetes cluster that are not in `Running` or `Completed` status using `kubectl`, execute the following command:

```bash
kubectl get pods --all-namespaces -o wide | grep -vw Running|grep -vw Completed
```

This command retrieves all Pods in all namespaces, excludes rows containing "Running" or "Completed" from the output using `grep -vw`, and displays additional columns (`-o wide`) for each Pod. Thanks for asking!
