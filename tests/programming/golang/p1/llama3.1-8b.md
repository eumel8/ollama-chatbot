111s
Here is a simple Go program that lists all Pods in a Kubernetes cluster using the kubernetes-go-client library. This example uses the clientset obtained from a ConfigLoader.
```go
package main

import (
	"context"
	"fmt"
	k8s "github.com/eumel8/kubernetes/go-client/clientset/versioned"
)

func main() {
	// Create a new clientset for the given cluster
	clientset, err := k8s.NewForConfig(context.TODO())
	if err != nil {
		fmt.Println(err)
		return
	}

	// Get all pods in the current namespace
	pods, err := clientset.CoreV1().Pods("default").List(context.TODO(), metav1.ListOptions{})
	if err != nil {
		fmt.Println(err)
		return
	}

	// Print each pod's name and namespace
	for _, pod := range pods.Items {
		fmt.Printf("%s (%s)\n", pod.Name, pod.Namespace)
	}
}
```
Thanks for asking!
