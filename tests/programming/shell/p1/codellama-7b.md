78s
You can use the `grep` command to search for specific patterns in your YAML files, and then use the `-i` flag to perform case-insensitive matching. For example, to search for `.spec.replicas: 1` and replace it with `0`, you can use the following command:
```bash
grep -Ril .spec.replicas: 1 | xargs sed -i 's/.spec.replicas: 1/0/g'
```
This will search for `.spec.replicas: 1` in all files in the current directory and its subdirectories, and replace it with `0` in-place using the `sed` command. The `-i` flag tells `sed` to edit the file in place, so you don't have to worry about creating backup files or dealing with output redirection.

Thanks for asking!
