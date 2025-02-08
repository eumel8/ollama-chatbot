78s
```yaml
# High Secure Deployment Manifest YAML for Nginx

apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-high-security
  labels:
    app: nginx
    security: high

spec:
  replicas: 1 # Ensure there's only one instance running securely
  selector:
    matchLabels: # Match the deployment to the labels set earlier
      app: nginx
  template:
    metadata:
      # No need to expose additional ports here
    spec:
      containers:
        - name: nginx-high-security-container # Container label for easy identification
          image: nginx:latest # Use the latest Nginx image
          ports:
            - containerPort: 8080 # Expose port 8080 on the container

# Thanks for asking!
