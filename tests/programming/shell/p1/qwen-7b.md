109s
To search for YAML files in a folder using Bash and replace `.spec.replicas: 1` with `0`, you can use the following commands:

1. First, list all the YAML files in the folder:
```bash
find folder_with_yaml_files -name "*.yaml"
```
Replace "folder_with_yaml_files" with your actual folder path.

2. Next, use sed to replace `.spec.replicas: 1` with `0` for each YAML file:
```bash
for yaml_file in $(find folder_with_yaml_files -name "*.yaml")); do
    sed -i 's/.spec.replicas:.*/\.spec.replicas: 0/g' $yaml_file
done
```
This command iterates over the found YAML files and uses sed to replace `.spec.replicas: 1` with `0`. Finally, it performs this operation for each file.

Remember to replace "folder_with_yaml_files" with your actual folder path.
