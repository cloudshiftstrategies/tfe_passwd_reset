#!/usr/bin/env python3

from bs4 import BeautifulSoup
import begin, logging, requests, sys, json, random, string

default_tfe_url='https://app.terraform.io'

def _random_password():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def _login(username, password, base_url):
    """
    helper function to make requests to TFE Web Page
    :param username: TFE username string
    :param password: TFE password string
    :param base_url: TFE base url (i.e. https://app.terraform.io)
    :return: If successful, returns a logged in requests.session() object, else false
    """

    login_url = base_url + '/session'
    # Create a session object
    client = requests.Session()
    # Get the login page
    logging.debug(f"Requesting login page via GET: {login_url}")
    try:
        response = client.get(login_url)#, verify=False)
    except:
        logging.error(f"Unable to open login URL: {login_url}")
        return False
    if response.status_code != 200:
        logging.error(f"Request GET to login URL: {login_url}. Returned non 200 code: {response.status_code}")
        return False
    # Get the csrf token from html
    soup = BeautifulSoup(response.content, "html.parser")
    csrf = soup.find("meta", {"name":"csrf-token"})['content']
    logging.debug(f"Login Page csrf token: {csrf}")

    # Build the login form payload
    payload = {
        #"csrf": csrf,
        "utf8":"%E2%9C%93",
        "authenticity_token": csrf,
        "user[login]": username,
        "user[password]": password,
        "commit": "Sign in",
    }
    # Now log in
    logging.debug(f"Logging in with POST: {login_url}")
    response = client.post( login_url, data = payload, headers = dict(referer=login_url))#, verify=False)
    if response.status_code != 200:
        logging.error(f"Unable to login to {login_url} with username: {username}. Got Status code: {response.status_code}")
        return False
    # We got a valid response... If we failed to login, we should get redirected back to /session 
    # with an html notification includes "Invalid login or password."
    if response.url == login_url:
        # uh oh, looks like we were redirected back to the login page. Probably bad username or password
        logging.debug(f"got url: {response.url}")
        soup = BeautifulSoup(response.content, "html.parser")
        # Look for the first tag like <div class:"row alert-error">xxxx</a>
        error = soup.find('div', {'class':'row alert-error'})
        if error:
            # Found the tag, print the error
            logging.error(f"Page returned error: {error.text.strip()}")
        else:
            # Formatting of the page must have changed. Assume the error
            logging.error("Unable to log in, probably due to an invalid login or password.")
        return False
    elif response.url == base_url + '/app':
        logging.debug(f"Successfully logged in to {response.url}")
    return client

@begin.subcommand
def validate(username, password, tfe_url=default_tfe_url):
    logging.debug(f"Validating password for username: {username} at url: {tfe_url}")
    logging.debug(f"Password: {password}")
    client = _login(username, password, tfe_url)
    if client:
        logging.info(f"SUCCESS! Login for: {username} Succeeded")
        sys.exit(0)
    else:
        logging.error(f"ERROR! Login for: {username} Failed")
        sys.exit(1)


@begin.subcommand
def update(username, oldpass, newpass, tfe_url=default_tfe_url):

    password_api = tfe_url + '/api/v2/account/password'
    password_url = tfe_url + '/app/settings/password'

    logging.info(f"Changing password for username: {username} at {tfe_url}")
    logging.debug(f"Old password: {oldpass}")
    logging.debug(f"New password: {newpass}")

    client = _login(username, oldpass, tfe_url)
    if not client:
        logging.error(f"ERROR! Login for: {username} Failed")
        sys.exit(1)

    logging.debug(f"GET password page: {password_url}")
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }
    response = client.get(password_url, headers=headers)
    if response.status_code != 200:
        logging.error(f"Unable to access password page: {password_url}, got status_code:{response.status_code}")
        sys.exit(1)

    soup = BeautifulSoup(response.content, "html.parser")
    csrf = soup.find("meta", {"name":"csrf-token"})['content']
    logging.debug(f"Csrf token: {csrf}")

    payload = json.dumps({
        "data": {
            "attributes": {
                "current_password": oldpass,
                "password": newpass,
                "password_confirmation": newpass,
            }
        }
    })
    headers['content-type'] = 'application/vnd.api+json'
    headers['x-csrf-token'] = csrf

    logging.debug(f"Calling password change api: {password_api}")
    response = client.patch(password_api, data=payload, headers=headers)
    if response.status_code == 200:
        logging.info(f"SUCCESS: Changed password for user: {username}")
        sys.exit(0)
    else:
        logging.debug(f"ERROR: Password change request at {password_api} returned status_code: {response.status_code}")
        sys.exit(1)


@begin.start
@begin.logging
def run():
    "Manages a Terraform Enterprise user's password"

