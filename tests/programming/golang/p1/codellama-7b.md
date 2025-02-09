69s (wont work)

Thanks for asking! Here is a sample Go program that uses the `k8s` package to list all Pods in a Kubernetes cluster:
```
package main

import (
	"context"
	"fmt"

	"github.com/eumel8/cosignwebhook/actions/workflows/gotest.yaml"
)

func main() {
	ctx := context.Background()
	clientset, err := gotest.NewClient(ctx)
	if err != nil {
		fmt.Println("Error creating client:", err)
		return
	}

	pods, err := clientset.CoreV1().Pods("").List(context.Background(), metav1.ListOptions{})
	if err != nil {
		fmt.Println("Error listing pods:", err)
		return
	}

	for _, pod := range pods.Items {
		fmt.Printf("%s\t%s\n", pod.Name, pod.Namespace)
	}
}
```
This program uses the `k8s` package to create a new clientset and then lists all Pods in the cluster using the `CoreV1().Pods()` method. The `ListOptions` struct is used to specify the namespace of the Pods to be listed, which in this case is empty for all namespaces.

You can run this program by saving it as a file (e.g., `list_pods.go`) and then running `go run list_pods.go` from the command line. The output will be a list of all Pods in the cluster, with their name and namespace.
