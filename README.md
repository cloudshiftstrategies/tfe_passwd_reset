# tfe_passwd.py

This tool is designed to change a users password for terraform enterprise

## Installation

		pip3 install -r requirments.txt


## example usage

### Change joe_user's password to a specific string

	$ tfe_passwd.py joe_user update joes_old_pass --newpass joes_new_pass
	Changing password for username: joe_user at https://app.terraform.io
	SUCCESS: Changed password for user: joe_user to joes_new_pass

### Change joe_user's password to a random string

	$ tfe_passwd.py joe_user update joes_old_pass --random
	Changing password for username: joe_user at https://app.terraform.io
	SUCCESS: Changed password for user: joe_user to KXZJXJC354

### Validate joes_user's password

	$ tfe_passwd.py validate joe_user KXZJXJC354
	SUCCESS: Login for: joe_user Succeeded

## Get help output

	$ tfe_passwd.py -h
	$ tfe_passwd.py update -h
	$ tfe_passwd.py validate -h
