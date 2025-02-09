41s
Thanks for asking!

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
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
      - image: nginx:latest
        name: nginx
        ports:
        - containerPort: 8080
      - environment:
          - name: NGINX_PORT
            value: 8080
        - environment:
          - name: NGINX_HOST
            value: <your_nginx_server_ip_address>
      - ports:
      - - containerPort: 80
        name: webserver
        port: 80
  metadata:
    annotations:
      app.kubernetes.io/metadata:
        name: nginx
```
