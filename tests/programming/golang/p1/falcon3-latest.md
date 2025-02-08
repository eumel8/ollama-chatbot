100s
```go
package main

import (
    "context"
    "fmt"

    "github.com/eumel8/cosignwebhook/pkg/kubeclient"
)

func main() {
    client, err := kubeclient.New()
    if err != nil {
        fmt.Println("Error creating Kubernetes client:", err)
        return
    }

    pods, err := client.ListPods(context.Background())
    if err != nil {
        fmt.Println("Error listing Pods:", err)
        return
    }

    for _, pod := range pods.Items {
        fmt.Printf("Pod: %s\n", pod.Name)
    }

    thanks for asking!
}
```

