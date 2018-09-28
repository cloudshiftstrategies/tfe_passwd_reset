# tfe_passwd.py

This tool is designed to change a users password for terraform enterprise

## Installation

		pip3 install -r requirments.txt


## example usage

		tfe_passwd.py joe_user update joes_old_pass joes_new_pass
		tfe_passwd.py joe_user verify joes_new_pass


	```
	usage: tfe_passwd.py [-h] [-v | -q]
											 [--loglvl {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
											 [--logfile LOGFILE] [--logfmt LOGFMT]
											 {update,validate} ...

	Manages a Terraform Enterprise user's password

	optional arguments:
		-h, --help            show this help message and exit
		-v, --verbose         Increse logging output
		-q, --quiet           Decrease logging output

	Available subcommands:
		{update,validate}
			update
			validate

	logging:
		Detailed control of logging output

		--loglvl {DEBUG,INFO,WARNING,ERROR,CRITICAL}
													Set explicit log level
		--logfile LOGFILE     Ouput log messages to file
		--logfmt LOGFMT       Log message format
	```
