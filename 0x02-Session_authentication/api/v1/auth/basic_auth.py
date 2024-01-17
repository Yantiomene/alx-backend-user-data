#!/usr/bin/env python3
"""Basic Auth class
"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic Authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract the Base64 part of the Authorization header
        Return:
          - The Base64 part of the header
        """
        if not authorization_header or \
           not isinstance(authorization_header, str) or \
           not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """ Decode the Base64 string
        Return:
          - The decoded string
        """
        if not base64_authorization_header or \
           not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_string = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(base64_string)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """ Extract user email and password
        Return:
          - (email, password)
        """
        if not decoded_base64_authorization_header or \
           not isinstance(decoded_base64_authorization_header, str) or \
           ':' not in decoded_base64_authorization_header:
            return None, None
        email = decoded_base64_authorization_header.split(':')[0]
        pawd = decoded_base64_authorization_header.split(':')[1:]
        pawd = ":".join(pawd)
        return email, pawd

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Return the User instance based on his email and password
        Return:
          - User instance
        """
        if not user_email or type(user_email) is not str:
            return None
        if not user_pwd or type(user_pwd) is not str:
            return None

        try:
            users = User.search({"email": user_email})
            if not users:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the User instance for a request
        Return:
          - User instance
        """
        try:
            auth_header = self.authorization_header(request)
            base64_string = self.extract_base64_authorization_header(
                auth_header)
            decoded_string = self.decode_base64_authorization_header(
                base64_string)
            email, pawd = self.extract_user_credentials(decoded_string)
            user = self.user_object_from_credentials(email, pawd)
            return user
        except Exception:
            return None
