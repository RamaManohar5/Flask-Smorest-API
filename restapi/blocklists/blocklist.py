"""
    blocklist.py

    this file contains the blocklist of JWT tokens. it will be imported by app and the logout resource,  
    so that tokens can be added to the blocklist then the user logout.

"""

BLOCKLIST = set()