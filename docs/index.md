# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs help` - Print this help message.

## Project layout

	arduino_due/    			# Not used (replaced by ADS1115).
	
	config/						# Supervisor, nginx, cron, raspbian configuration files
		dev/
		prod/  			
	
	docs/						# Not used (replaced by chaudiere-wiki.git)
	
	hardware/					# Fritzing and schematic design files
	
	install/					# installation scripts (Shell)
		hardware.sh				# Configure raspbian modules
		install-system.sh		# apt-get update upgrade install python virtualenv...
		install-chaudiere.sh	# Create venv, configure nginx supervisor and cron, start server
	
	logger/						# Logger config for python scripts
	
	sensor/						# Interface with temperature and current sensors
		get_watt.py				# Retrieve current sensor values (i2c via ADS1115)
		get_temp.py				# Retrieve temperature sensor values from DS18b20 (1wire)
		create_data.py			# Call get_watt.py and get_temp.py and create record in Chaudiere database
		...						# Other python scripts not used anymore (arduino due)
	
	gui.sh						# Shell script to launch Chromium for local display
	mkdocs.yml					# xxx

	
	
	
	
	
	