# Chaudiere wiki

* [https://chaudiere-wiki.readthedocs.io/en/latest/](https://chaudiere-wiki.readthedocs.io/en/latest/)

## Commands

* `python main.py` - run flask app in console (debug mode)
* `sudo supervisorctl status`
* `sudo supervisorctl start all` - gunicorn & sensor deamon
* `sudo service nginx start / stop` - serve web app
* `python manager.py database init_all` - Create all databases
* `python manager.py users create` - Create admin user

## Project layout

	arduino_due/                # Not used (replaced by ADS1115).
	
	config/                     # Supervisor, nginx, cron, raspbian configuration files
		dev/
		prod/  			
	
	hardware/                   # Fritzing and schematic design files
	
	install/                    # installation scripts (Shell)
		hardware.sh	            # Configure raspbian modules
		install-system.sh       # apt-get update upgrade install python virtualenv...
		install-chaudiere.sh    # Create venv, configure nginx supervisor and cron, start server
	
	logger/                     # Logger config for python scripts
	
	sensor/                     # Interface with temperature and current sensors
		get_watt.py             # Retrieve current sensor values (i2c via ADS1115)
		get_temp.py             # Retrieve temperature sensor values from DS18b20 (1wire)
		create_data.py          # Call get_watt.py and get_temp.py and create record in Chaudiere database
		...                     # Other python scripts not used anymore (arduino due)
	
	gui.sh                      # Shell script to launch Chromium for local display
	
	mkdocs.yml                  # Mkdocs configuration
	docs/                       # Markdown wiki pushed to readthedocs

	flask_app/                  
		app/                    # Flask package
		scripts/                # Python scripts to process asynchronous tasks
			archive_minute.py   # called every minute by cron
			process_phase.py    # called every minute by cron
		manager.py              # Command Line Interface (production)
		cli_stuff.py            # Command Line Interface (dev / debug)
		config.py               # Environnement variables configuration
		db_api.py               # database API called by external script create_data.py
		main.py                 # To run Flask app in debug mode (python3 main.py)
		wsgi_gunicorn.py        # To run Flask app in production mode
		requirements.txt        # List of python packages (pip3 install -r requirements.txt) 
		send_email_sms.py       # Script for alerts tasks
		util.py                 # Datetime utilities

## Flask app package layout

	flask_app/					
		app/					
			__init__.py                 # create_app() and set_config()
			constantes.py               # Constantes used for charts and database
			admin/                      # Admin Blueprint
				forms.py
				system_info.py
				views.py
			views/						
				charts/                 # charts Blueprint
					views.py
					charts.py
					history_form.py
				auth.py                 # Auth Blueprint
				webapi.py               # webapi Blueprint (retrieve charts data)
				monitor.py
			helpers/                    # not used
			models/
			static/
				favicon.ico
				js/
					custom_highstock.js
			templates/
	
