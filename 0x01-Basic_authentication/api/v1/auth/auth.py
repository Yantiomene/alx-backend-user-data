#!/usr/bin/env python3
"""Class template for all Authentication system
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """Class template for authentication
    """
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """Method to exclude paths for the authentication
        Return:
          - Boolean
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Method used to create the authentication header
        Return:
          - String
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method used to return the current login user
        Return:
          - TypeVar('User')
        """
        return None
