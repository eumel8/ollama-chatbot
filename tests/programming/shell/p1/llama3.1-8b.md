82s
You can use the `find` command to search for YAML files in a directory and then use `grep` to search for the text `.spec.replicas: 1`. Once found, you can pipe the output to `sed` to replace the text with "0". Here's an example bash command:

```bash
find . -type f -name "*.yaml" -exec grep -l ".spec.replicas: 1" {} \; | xargs sed -i 's/.spec.replicas: 1/0/g'
```

This will replace the text `.spec.replicas: 1` with `0` in all YAML files found in the current directory.

Thanks for asking!
