3 correction (wont work, no external traffic)

```go
package main

import (
        "context"
        "fmt"
        "log"

        k8s "k8s.io/client-go/kubernetes"
        metav1 "k8s.io/apimachinery/pkg/apis/meta/v1" // Import metav1 package correctly
)

func main() {
        config, err := k8s.InClusterConfig()
        if err != nil {
                log.Fatal(err)
        }

        clientset, err := k8s.NewForConfig(config)
        if err != nil {
                log.Fatal(err)
        }

        namespace := "your-namespace"

        pods, err := clientset.CoreV1().Pods(namespace).List(context.TODO(), metav1.ListOptions{})
        if err != nil {
                fmt.Printf("Error listing pods: %v\n", err)
                return
        }

        for _, pod := range pods.Items {
                fmt.Printf("%s/%s/%s\n", pod.Namespace, pod.Name, pod.Status.Phase)
        }
}
```
