82s
Here is a sample deployment manifest YAML that uses a higher level of security:
```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-secure-deployment
spec:
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
          name: http
        securityContext:
          runAsUser: 1001
          fsGroup: 1001
          seLinuxOptions:
            level: "s0:c12345"
          supplementalGroups:
          - 1010
  securityContext:
    fsGroup: 1001
```
This deployment uses a non-root user and group, restricts SELinux to a specific label, and adds an additional group for extra security. Thanks for asking!
