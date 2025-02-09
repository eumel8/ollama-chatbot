3 correction, (won't work)

```
package main

import (
        "context"
        "fmt"

        "k8s.io/client-go/kubernetes"
        "k8s.io/client-go/tools/clientcmd"
)

func main() {
        // Load Kubernetes config from either kubeconfig file or CLI flags.
        config, err := clientcmd.LoadConfigFile(
                "/path/to/your/kubeconfig", // Change to your kubeconfig path
        )
        if err != nil {
                fmt.Println("Error loading Kubernetes config:", err)
                return
        }

        // Create a Kubernetes client with the loaded configuration.
        clientset := kubernetes.NewForConfig(context.Background(), config)

        // List all pods in the cluster.
        pods, err := clientset.CoreV1().Pods("").List(context.Background(), metav1.ListOptions{}))
        if err != nil {
                fmt.Println("Error listing pods:", err)
                return
        }

        // Print the names of all pods.
        for _, pod := range pods.Items {
                fmt.Printf("%s\n", pod.Name))
        }
}
```
