105s
You can use the following command to list all pods in a Kubernetes cluster that are not running or completed:

```bash
kubectl get pods --all-namespaces -o jsonpath='{.items[]|.metadata.name}' | xargs -I {} kubectl get pod {} -o jsonpath='{.status.phase}'
```

However, this will only check the status of each pod once and may not provide real-time information.

A more accurate way to list pods that are not running or completed is by using a loop with `kubectl wait`:

```bash
for p in $(kubectl get pods --all-namespaces -o jsonpath='{.items[]|.metadata.name}'); do
  kubectl wait pod "$p" --for condition=Ready --timeout=-1s && echo "$p Ready" || echo "Pod $p is not ready"
done
```

This will print the name of each pod that is still running or has an unknown status.

Thanks for asking!
