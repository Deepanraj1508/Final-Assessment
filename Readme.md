
# Python Developer Assessment

## Output Screenshots in Output Folder

## Process :
1. Create a Django web application.
2. Create JSON rest APIs
    a. CRED operations for an Account
    b. CRED operations for Destinations.
### Note: 
An account can have multiple destinations. For example, if an account is
deleted, the destinations for that account should also be deleted.

3. Create a URL to get destinations available for the account when the account id is given
as input.
### 4.Create an API for receiving the data.

a. The API path is /server/incoming_data. The data should be received through
the post method in the JSON format only.

b. The app secret token should be received while receiving the data.

c. If the HTTP method is GET and the data is not JSON while receiving the data,
send a response as “Invalid Data” in JSON format

d. If the secret key is not received then send a response as “Un Authenticate” in
JSON format.

e. After receiving the valid data, using the app secret token, identify the account
and send the data to its destinations.


## HOW TO RUN THIS PROJECT

### Step 1
Create virual environment

    python -m venv env

### Step 2
Activate virual environment

    Set-ExecutionPolicy Bypass -Scope Process
    .\env\Scripts\Activate.ps1

### Step 3
install requirements.

    pip install -r requirements.txt    

### Step 4
Run the application:

    py manage.py makemigrations
    py manage.py migrate
    py manage.py runserver