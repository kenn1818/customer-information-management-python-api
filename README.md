# [Customer Information Management API]

## :cloud: Build Setup

## install dependencies

## install python
**MacOS Users**
1. `brew install python`
2. `python --version`, to check your python is installed successfully

**Windows Users**
1. Download installer from offical website: https://www.python.org/downloads/windows/  (choosing depends on your OS)
2. Install python by execute the installer
3. Set up your path environment variables
  a. Open the Start menu and start the Run app.
  b. Type sysdm.cpl and click OK. This opens the System Properties window.
  c. Navigate to the Advanced tab and select Environment Variables.
  d. Under System Variables, find and select the Path variable.
  e. Click Edit.
  f. Select the Variable value field. Add the path to the python.exe file preceded with a semicolon (;). For example, in the image below, we have added ";C:\Python34."
  g. Click OK and close all windows.
4. `python --version`, to check your python is installed successfully

**By setting this up, you can execute Python scripts like this: `Python script.py`**

## install flask framework
1. `pip install flask`

## install sqlite3
1. `pip install sqlite3`

### Running API locally @ localhost:5000
1. `cd api`
2. `python api.py`
