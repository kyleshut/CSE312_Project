# CSE312_Project
A Flask web app built as the final project for [CSE 312](cse312.com) at the University at Buffalo.<br><br>
Users should be able to utilize the following features:
- User login/registration with secure authentication
- See the list of all users currently logged in
- Send direct messages to other users
- Be notified when they receive a direct message
- Share multimedia content (images) in the gallery
- Interact in real time via cookie clicker

### Login/Registration
Navigate to the [site](http://cse312-05.dcsl.buffalo.edu) to login/register. After successfully registering and logging in, your information will be saved for the length of your session, allowing you to refresh/close the browser and login with one click rather than inputting your credentials again. Once logged in, you will see the navigation page and any personal notes you've left for yourself.

### Online User List
Once logged in, you'll see the navigation page where you can navigate between the pages of the site. Also on this page is a list of the currently online users.

### Direct Messages
From the navigation page, select the DM Room button to direct message other users. The page will list all currently online users. Type in a user's name, type a message and hit submit to send a direct message. When receiving a message, you will receive an alert with the text of the message sent to you.

### Multimedia
To share multimedia content (images), select the upload button from the navigation page. On this page, you can upload images in .png, .jpg, and .jpeg formats. Once you've uploaded your image, navigate to the gallery page to see your image.

### Real Time Interactions
From the navigation page, click the Interaction room button to go to a cookie clicker. Press the buttonas much or as little as you like and the value will update for you and all users on the webpage.

## Demo
[Live Site](http://cse312-05.dcsl.buffalo.edu)

## Technology
- [Python 3.8](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - a [WSGI](https://wsgi.readthedocs.io/en/latest/) web application framework
- [MongoDB](https://www.mongodb.com/) - a document-based distributed database platform
- [PyMongo](https://pymongo.readthedocs.io/en/stable/) - a Python library distribution for working with MongoDB
- [bcrypt](https://pypi.org/project/bcrypt/) - a library for hashing information

## Team
[Anthony Morales](https://github.com/AnthonyLMorales) | [Andrew Qu](https://github.com/Qu-Andrew) | [Kyle Shuttleworth](https://github.com/kyleshut) | [Hollis Pauquette](https://github.com/pauquette)
