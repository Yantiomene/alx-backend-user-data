#!/usr/bin/env python3
"""Basic Auth class
"""
from api.v1.auth.auth import Auth
import base64


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
