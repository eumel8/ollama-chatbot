178s

apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
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
          protocol: TCP
        securityContext:
          runAsUser: 1000
          runAsGroup: 3000
          fsGroup: 3000
          syscalls: ["exec", "exit", "fork", "killed", "mkdir", "open", "pipe", "read", "sched_getparam", "sched_setparam", "stat", "fstat", "isatty", "wait", "waitpid"]
        resources:
          limits:
            cpu: 200m
            memory: 128Mi
          requests:
            cpu: 50m
            memory: 64Mi
        volumeMounts:
        - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
          name: default-token-0sb6n
          readOnly: true
      imagePullSecrets:
      - name: default-token-0sb6n
