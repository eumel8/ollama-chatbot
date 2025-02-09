3 correction, wont work (external traffic 1xcloudflare.com)

```go
package main

import (
        "context"
        "fmt"
        "log"
        "k8s.io/api/core/v1"
        "k8s.io/client-go/kubernetes"
        "k8s.io/client-go/rest"
        "k8s.io/client-go/tools/clientcmd"
)

func main() {
        // Load configuration from a local kube config file
        config, err := rest.InClusterConfig()
        if err != nil {
                config, err = clientcmd.BuildConfigFromFlags("", "/path/to/.kube/config")
                if err != nil {
                        log.Fatal(err)
                }
        }

        // Create a Kubernetes client using the loaded configuration
        client, err := kubernetes.NewForConfig(config)
        if err != nil {
                log.Fatal(err)
        }

        // List pods with options
        pods, err := client.CoreV1().Pods("").List(context.TODO(), v1.PodListOptions{})
        if err != nil {
                log.Fatal(err)
        }

        for _, pod := range pods.Items {
                fmt.Printf("%s/%s\n", pod.Namespace, pod.Name)
        }
}
```

