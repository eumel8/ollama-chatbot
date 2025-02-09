130s
To search for YAML files in a folder and replace `.spec.replicas: 1` with `.spec.replicas: 0` using Bash, you can use the following command:

```bash
find . -name '*.yaml' | xargs yq r -j '.spec.replicas' | grep 1 | while read f; do yq w -j -i "$f" '.spec.replicas = 0'; done
```

However, this command will only print the new content and won't save it back to the file. To actually modify the files, you can use a loop like this:

```bash
find . -name '*.yaml' | while read f; do yq w -j -i "$f" '.spec.replicas = 0'; done
```

Thanks for asking!
