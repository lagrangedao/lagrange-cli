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

## Installation

-  via _pip_
- In lagrange-cli directory

 ```
pip install .
 ```