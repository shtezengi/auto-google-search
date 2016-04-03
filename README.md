===============================
Tool overview
===============================
This tool crawls google for user-inputted search terms, saves the first 20 results returned, 
and visits each of the result pages and store a configurable set of contents from them, and displays them to users.

===============================
Install local development tools
===============================
1) Download and install vagrant

2) Download and install virtual box

=================================================
Setup the project's virtual Linux machine locally
=================================================
1) cd to the projects root directory, where you can locate the "Vagrantfile" file

2) Run the vagrant powered linux CentOS virtual machine which will host the project by running the following command
in projects root where "Vagrantfile" exists
$ vagrant up --provider=virtualbox

3) ssh into the virtual host machine by running the following command
$ vagrant ssh

=========================================
Setup and Run the development environment
=========================================
1) After SSHing in projects virtual machine run the following command to create virtual python environment,
install the necessary python packages, update project's database, and update the project.
$ /vagrant/deploy/update.sh

2) Run the project using the following commands
$ cd /vagrant/src/
$ ./manage.py runserver 8011

3) Go back to your host machine (not the virtual machine) and locate your hosts file, and add the following line to it
192.168.19.19   autogooglesearch.local

4) Go to your browser and enter the following link in your browser
http://autogooglesearch.local:8011