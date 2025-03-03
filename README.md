This is a web app for searching and cataloging books using the Google Books API.\
Currently only supports ISBN 13.

This app can also be accessed on PythonAnywhere at:\
[https://kpm.pythonanywhere.com](https://kpm.pythonanywhere.com)

The app uses a model-view-controller design pattern, where user searches for a book using the google API,
that book is then sent back to the server and added to the database, then the data from the data base
is sent back to the user and displayed on their dashboard. Users can also delete books in their catalog.
the init file creates the server, app.py is a wrapper for starting the server using the python3 command,
db.py handles creating the database, auth.py handles registering users and user logon and logoff functions, 
and dashboard.py handles displaying information on the user's web browser.  

to run (macOS/linux):\
python3 app.py

usage:\
app.py [-h] [--debug]

NOTE:\
The command "python3 app.py" does NOT work on Windows, instead use:\
python app.py

default user:\
username: admin\
password: password

by Keith McDade for CUNY School of Professional Studies, IS 211 Software Programming II, Prof. Alain Ledon
