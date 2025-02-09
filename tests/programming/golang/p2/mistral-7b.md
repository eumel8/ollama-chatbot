3 correction, still wrong. (external traffic cloudfare dns-over-https)

```go
package main

import (
        "context"
        "fmt"
        corev1 "k8s.io/api/core/v1"
        metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
        clientsetscheme "k8s.io/client-go/kubernetes/scheme"
        "k8s.io/client-go/rest"
        "k8s.io/client-go/tools/clientcmd"
)

var scheme = clientsetscheme.SchemeBuilder.AddAPISchemes(nil).Build()

func main() {
        // Replace "path/to/your/serviceaccount.json" with the path to your service account token file
        config, err := rest.InClusterConfig()
        if err != nil {
                config, err = buildConfigFromFlags("path/to/your/serviceaccount.json")
                if err != nil {
                        fmt.Println(err.Error())
                        os.Exit(1)
                }
        }

        config.Wrap scheme.CODECS.DecodingReferenceResolver

        clientset, err := kubernetes.NewForConfig(config)
        if err != nil {
                fmt.Println(err.Error())
                os.Exit(1)
        }

        coreV1 := clientset.CoreV1()

        pods, err := coreV1.List(context.TODO(), metav1.ListOptions{})
        if err != nil {
                fmt.Println(err.Error())
                os.Exit(1)
        }

        for _, pod := range pods.Items {
                fmt.Printf("Name: %s\n", pod.ObjectMeta.Name)
                fmt.Printf("Namespace: %s\n", pod.ObjectMeta.Namespace)
                fmt.Println()
        }
}

func buildConfigFromFlags(restConfigOverrides string) (*rest.Config, error) {
        config := rest.CopyConfigFromKubeconfig(&kubernetes.Config{})
        return config.ClientConfig().ToRESTConfig(), nil
}
```
