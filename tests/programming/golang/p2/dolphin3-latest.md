3 correction,  wont work, no external traffic

```go
package main

import (
        "context"
        "fmt"
        "os"

        "k8s.io/client-go/kubernetes"
        "k8s.io/client-go/rest"
)

func main() {
        config, err := rest.InClusterConfig()
        if err != nil {
                fmt.Printf("InClusterConfig failed: %v\n", err)
                os.Exit(1)
        }
        clientset, err := kubernetes.NewForConfig(config)
        if err != nil {
                fmt.Printf("Failed to create clientset: %v\n", err)
                os.Exit(1)
        }

        pods, err := clientset.CoreV1().Pods("default").List(context.TODO())
        if err != nil {
                fmt.Printf("Error listing pods: %v\n", err)
                os.Exit(1)
        }

        for _, pod := range pods.Items {
                fmt.Println(pod.Name)
        }
}
```

