140s

To write a Go program that lists all Pods in a Kubernetes cluster, you can use the client-go library which is the official Go client for Kubernetes. Here's an example:

```go
package main

import (
	"context"
	"fmt"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

func main() {
	// Use the current context in kubeconfig
	config, err := clientcmd.GetConfig("", clientcmd.Options{})
	if err != nil {
		panic(err.Error)
	}

	// Create a clientset using the config
	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		panic(err.Error)
	}

	// Get all pods in all namespaces
	pods, err := clientset.CoreV1().Pods("").List(context.TODO(), metav1.ListOptions{})
	if err != nil {
		panic(err.Error)
	}
	
	fmt.Println("Listing pods with their IPs:")
	for _, pod := range pods.Items {
		fmt.Printf("%s\n", *pod.Name)
	}
}
```

This program connects to your Kubernetes cluster using the `kubeconfig` file and lists all Pods in all namespaces.

Thanks for asking!
