#!/usr/bin/env python3
"""Regex ingeneering"""

from typing import List
import re
import logging
from os import environ
import mysql.connector

PII_FIELDS = ("name", "email", "password", "phone", "ssn")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Return the log message obfuscated"""
    for field in fields:
        message = re.sub("{}=.*?{}".format(field, separator),
                         "{}={}{}".format(field, redaction, separator),
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class to format and filter PII fields
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Init method """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filter value in incomming log records """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """ Return a logging.Logger object for personnal data handling """

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Set StreamHandler
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(streamHandler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Return a connector to the database """

    db_name = environ.get("PERSONAL_DATA_DB_NAME")
    host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")

    connector = mysql.connector.connection.MySQLConnection(database=db_name,
                                                           host=host,
                                                           user=username,
                                                           password=password)
    return connector


def main():
    """ Connect to db and retrieve all rows in the users """

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * from users;")
    fields = [desc[0] for desc in cursor.description]

    logger = get_logger()

    for row in cursor:
        str_row = ''.join(f'{field}={str(v)}; ' for v, field in
                          zip(row, fields))
        logger.info(str_row.strip())

    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
