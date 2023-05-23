## Installation

- With lagrange-cli as the current work directory

 ```
 git clone git@github.com:lagrangedao/lagrange-cli.git
 cd lagrange-cli
 pip install .
 ```

## Usage

### Clone Lagrange Repo
- Clones provided Lagrange repo into current directory
```
lag clone https://lagrangedao.org/<type>/<wallet_address>/<name>
```
### Add Files
- Add files to be comitted
```
lag add file1 file2 file3 ...
```
- To add all files in current directory and subdirectories
```
lag add .
```

### Remove Added Files
- Removes added files
```
lag remove file1 file2 file3 ...
```

### Commit Files
- Commit added files to be pushed
```
lag commit -m "commit message"
```
### Push Dataset
- Push comitted files to designated dataset
```
lag clone https://lagrangedao.org/<type>/<wallet_address>/<name>
```

### Config Commands
Set API Token
```
lag config --api-token <TOKEN>
```

