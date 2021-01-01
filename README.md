# Airport Manager

Airport Manager is a software for managing flights in a airport. It can be used by users to get information about needed flight and admins for adding, deleting and updating list of flights.

## Installation

Use following command to get files

```bash
git clone https://github.com/Yaqubov/airport_manager.git
```

After, install packages with:

```bash
pip install requirements.txt
```

## Usage

Firstly, the flask server should be run to use services.

```bash
python3 server.py
```
For using app as admin, following command should be executed

NOTE!! Admin **username:** *root* **password:** *toor*

```bash
python3 client.py --admin
```

Command to use app as user

```bash
python3 client.py
```