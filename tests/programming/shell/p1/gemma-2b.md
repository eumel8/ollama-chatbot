23s
Thanks for asking!

Sure, here's the answer to your question:

Search all YAML files in the folder with bash and replace `.spec.replicas: 1` with `0` using the following command:

```bash
find . -name "*.yaml" -exec sed -i "s/\.spec\.replicas: 1/ \.spec\.replicas: 0/g" {} \;
```
