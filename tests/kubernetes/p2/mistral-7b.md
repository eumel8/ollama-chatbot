120s
 Here is a high-secure Deployment manifest YAML for Kubernetes to run the latest nginx image and expose port 8080:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 8080
        securityContext:
          runAsUser: 1001
          capabilities:
            drop: ALL
          seLinuxOptions:
            type: container
      imagePullSecrets:
      - name: cosignwebhook
      serviceAccountName: default-service-account
      nodeSelector:
        beta.kubernetes.io/os: linux
      tolerations:
      - operator: Exists
        effect: NoSchedule
        tolerationSeconds: 300
```

