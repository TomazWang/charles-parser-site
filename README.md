# Charles Parser

A simple parser that parses Chales session file (in json fromat, .chlsj file) in to readable files.


## Requirements

- Python 3.6+
- pip 9.+

## Install

1. Clone the repo
2. Create a  virtual environment with virtualenv

  ```bash
  # in the repo folder
  $ virtualenv -p python3.6 venv
  ```

3. Activate the virtual environment

```bash
# in the repo folder
$ cd /path/to/new/virtual/environment/bin
$ source activate 
```

4. Install all modual from requirements.txt

```bash
# in the repo folder
$(venv) pip install --upgrade -r requirements.txt
```

5. Run the app on localhost

```bash
# in the repo folder
$(venv) venv/bin/python3 app.py
```

## Migrates to another host
1. Change the `ROOT_URL` in app.py
2. Run the app.
