#!/usr/bin/env python3
""" Session Exp auth class
"""
from api.v1.auth.session_auth import SessionAuth
from flask import request
from models.user import User
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class
    """

    def __init__(self):
        """ Init method
        """
        if not os.getenv("SESSION_DURATION") or not \
           int(os.getenv("SESSION_DURATION")):
            self.session_duration = 0

        self.session_duration = int(os.getenv("SESSION_DURATION"))

    def create_session(self, user_id: str = None) -> str:
        """ Create a session_id based on user_id
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {}
        session_dict["user_id"] = user_id
        session_dict["created_at"] = datetime.now()
        self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Return the user_id based on the session_id
        """
        if not session_id:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            return None
        if "created_at" not in self.user_id_by_session_id[session_id]:
            return None
        if self.user_id_by_session_id[session_id]["created_at"] + \
           timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return self.user_id_by_session_id[session_id]["user_id"]
