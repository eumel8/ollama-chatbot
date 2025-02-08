98s

You can use the `find` command combined with `grep -rl` to search for YAML files containing ".spec.replicas: 1" and then pipe this output into `sed` to perform the replacement. Here's a simple command:

```
find . -name "*.yaml" -exec grep -lr '.spec.replicas: 1' {} \; | xargs sed -i 's/.spec.replicas: 1/.spec.replicas: 0/g'
```

This command searches all YAML files (`*.yaml`) in the current directory and its subdirectories for lines containing ".spec.replicas: 1", replaces them with ".spec.replicas: 0" within those files.

Thanks for asking!
