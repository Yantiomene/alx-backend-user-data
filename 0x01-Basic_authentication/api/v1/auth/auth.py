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
        if not path or not excluded_paths:
            return True
        if path in excluded_paths or (path + '/') in excluded_paths:
            return False
        for excluded_path in excluded_paths:
            if excluded_path[-1] == '*' and \
               path.startswith(excluded_path[:-1]):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Method used to create the authentication header
        Return:
          - String
        """
        if not request or not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method used to return the current login user
        Return:
          - TypeVar('User')
        """
        return None
