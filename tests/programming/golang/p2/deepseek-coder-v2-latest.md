works! But this model runs out of the test spec because it has 8.9 GB size.
Result:

```go
package main

import (
        "context"
        "fmt"
        "k8s.io/client-go/kubernetes"
        "k8s.io/client-go/tools/clientcmd"
        "k8s.io/client-go/util/homedir"
        "log"
        "path/filepath"
        metav1 "k8s.io/apimachinery/pkg/apis/meta/v1" // Correct import for metav1
)

func main() {
        // Load kubeconfig file from default location or specified path
        var kubeconfig string
        if home := homedir.HomeDir(); home != "" {
                kubeconfig = filepath.Join(home, ".kube","kubeadm.config")
        } else {
                log.Fatal("Unable to find kubeconfig file")
        }

        // Build the config from the kubeconfig file
        config, err := clientcmd.BuildConfigFromFlags("", kubeconfig)
        if err != nil {
                log.Fatalf("Error building kubeconfig: %s", err)
        }

        // Create the clientset
        clientset, err := kubernetes.NewForConfig(config)
        if err != nil {
                log.Fatalf("Error creating clientset: %s", err)
        }

        // List all pods in all namespaces
        pods, err := clientset.CoreV1().Pods("").List(context.TODO(), metav1.ListOptions{})
        if err != nil {
                log.Fatalf("Error listing pods: %s", err)
        }

        // Print pod names
        fmt.Println("Listing all Pods in the cluster:")
        for _, pod := range pods.Items {
                fmt.Printf("Pod Name: %s, Namespace: %s\n", pod.Name, pod.Namespace)
        }
}
```
