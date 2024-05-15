# CS 338 Project: Toronto Auto Theft Database
![Python build result](https://github.com/ZhengQ2/cs338_project/actions/workflows/python-app.yml/badge.svg)

# Project Member:
Zheng Qiu
Frank Zheng
Shuqi Chang




# 1. Install Dependencies

## 1.1. MySQL
This project hosts its MySQL database on a remote server. Therefore, no MySQL related dependencies are required.

## 1.2. Install Python
This project is required using Python. A version of 3.8 or above is recommanded. To install Python, visit the [Python website](https://www.python.org/downloads/).

## 1.3. Install Python Dependencies
This package has several dependencies that need to be installed. To install them, run the following command:

```bash
pip install -r requirements.txt
```

# 2. Running the code
It is planned to use click to create a command line interface for the project. However, this is not currently implemented within this deadline. We have a basic loader script that can be run to load the data into the database. This loader script will then check if all entries are loaded into it.
To run the loader script, run the following command:

```bash
python impl.py
```