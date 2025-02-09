61s
To list all Pods in a Kubernetes cluster that are neither Running nor Completed, you can use `kubectl get pods -A` and filter the results accordingly.

The command `-A` stands for all namespaces. If you want to exclude completed pods, you can add an additional label or condition with `--selector=<status>` where `<status>` is "notRunning".

For example:

```bash
kubectl get pods -A --selector=status=notRunning
```

This will give you a list of Pods that are either Pending (initial state) or have been stopped and are not Running.
