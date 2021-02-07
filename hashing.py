import bcrypt


def hash_new_password(username, password):
    """
    Creates a new encrypted password and updates the database, linking the
    username with the salt and encrypted password.

    :param username: The username to be added/updated
    :param password: The submitted password
    :return: A tuple of 2 items (username, encrypted password) to be stored
    in the database
    """
    encrypted_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return [username, encrypted_password]


def does_password_match(username, password) -> bool:
    """
    Checks if the submitted password matches what is stored in the database.

    :param username: The submitted username
    :param password: The submitted password
    :return: True if passwords match; Otherwise, False
    """
    # Pull encrypted_password from database using username
    encrypted_password = b"test"
    return bcrypt.checkpw(password, encrypted_password)
