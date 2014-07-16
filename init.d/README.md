I used chmod to make the script executable:

sudo chmod +x /etc/init.d/ampabooks

I can start the ampabooks program with this command:

sudo /etc/init.d/ampabooks start

...and stop it again with this one:

sudo /etc/init.d/ampabooks stop

In order to make the program run on start up, it's necessary to run this command:

sudo update-rc.d ampabooks defaults
