91s

I can provide you with an example Go program using the Kubernetes client-go library to list all pods in a Kubernetes cluster. First, make sure to set up your kubeconfig properly and install the necessary dependencies. Here's a simple snippet that you might use:

```go
package main

import (
    "context"
    "fmt"

    k8sio "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/tools/cache"
    "github.com/eumel8/cosignwebhook/pkg/client-go/util/retry"
)

func main() {
    // Set up the Kubernetes client
    config, err := k8sio.InstantiateConfig()
    if err != nil {
        panic(err)
    }

    clientset, err := k8sio.NewClientSetFromConfig(config)
    if err != nil {
        panic(err)
    }

    // List all pods in the default namespace
    pods, err := clientset.CoreV1().Pods("default").List(context.TODO())
    if err != nil {
        panic(err)
    }

    // Print out each Pod's name
    for _, pod := range pods.Items {
        fmt.Println(pod.Name)
    }
}

```

Remember to replace "default" with the namespace you're interested in listing pods from.

