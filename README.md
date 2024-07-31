# CS 338 Project: Toronto Auto Theft Database

# Project Member:
- Zheng Qiu
- Frank Zheng
- Shuqi Chang
- Annie Ni
- John Hao

# 1. Install Dependencies

## 1.1. Clone the Repository
To clone the repository, run the following command:

```bash
git clone https://github.com/ZhengQ2/cs338_project.git
```

## 1.2. MySQL
This project hosts its MySQL database on a remote server. Therefore, no MySQL related dependencies are required.

## 1.3. Install Python
This project is required using Python. A version of 3.8 or above is recommanded. To install Python, visit the [Python website](https://www.python.org/downloads/).

## 1.4. Install Python Dependencies
This package has several dependencies that need to be installed. To install them, run the following command:

```bash
pip install -r requirements.txt
```
(try `pip3` if the above does not work)

# 2. Running the code
It is planned to use click to create a command line interface for the project. However, this is not currently implemented within this deadline. We have a basic loader script that can be run to load the data into the database. This loader script will then check if all entries are loaded into it.
Data is currently loaded and the connection will be set automatically.
To run the script, run the following command:

```bash
python database_app.py
```
(try `python3` if the above does not work)

It will prompt for user name and password, enter "owner" for both. Password has a secure input panel, so no feedback will be provided until you click enter to confirm password.

# 3. Interacting with the database
The database would first ask for register. Enter "n" to skip this step.
    enter a valid SIN, username and password to register.

It would ask for username and password.
    The defaute accounts are: owner/owner and police/police with corresponding permissions.

Then, you are able to select the following options if the role is police:
    1. List neighborhoods where the number of events is greater than or equal to a specified threshold.
    2. Count the types of outcome for all events.
    3. Rank all communities in terms of the average price of vehicles that got stolen.
    4. Check the latest events captured in the dataset.
    5. Check insurance payments for vehicles that got stolen. 
    6. Check police resposible for handled events.

If the account role is owner, then only option 1, 3, 4 will be avaliable.

Enter the number of the option you want to select. (i.e., 1)
Enter other will exit the program.

For option 1, you will be asked to enter a threshold number, enter any integer to continue.