INTRO
Almost all Word Press websites use plugins. These plugins are stored in a specified location, inside the file system that Word Press is installed on. This program is designed to be shown where the plugins are stored, and then pull the plugins meta data. This metadata is then stored in report.txt

RUNNING THE CODE
After running the code, a File Dialog GUI will appear and request the directory that the plugins are stored. Test Plugins have been supplied if you do not have access to a file system with wordpress installed. 

If there are more PHP files in a given plugin's directory, it will display all the php files in the given directory, and number them. The user will then be asked to enter the number of the correct plugin.

After the code has ran through ever plugin within the directory, report.txt will be updated.