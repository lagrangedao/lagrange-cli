## Installation

- With lagrange-cli as the current work directory

 ```
 git clone git@github.com:lagrangedao/lagrange-cli.git
 cd lagrange-cli
 pip install .
 ```

## Usage

### Clone Dataset
- Clones provided dataset into current directory
```
swan clone https://lagrangedao.org/datasets/<dataset_name>
```
### Add Files
- Add files to be comitted
```
swan add file1 file2 file3 ...
```
- To add all files in current directory and subdirectories
```
swan add .
```

### Remove Added Files
- Removes added files
```
swan remove file1 file2 file3 ...
```

### Commit Files
- Commit added files to be pushed
```
swan commit -m "commit message"
```
### Push Dataset
- Push comitted files to designated dataset
```
swan clone https://lagrangedao.org/datasets/<dataset_name>
```

### Config Commands
Set API Token
```
swan config --api-token <TOKEN>
```

