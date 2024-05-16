#!/usr/bin/env python3
"""
Module for filtering log data
"""
import re
import logging
from typing import List, Tuple
import os
import mysql.connector
from mysql.connector import connection


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """
    Returns the log message obfuscated.

    Args:
        fields (List[str]): representing all fields to obfuscate.
        redaction (str): representing the field will be obfuscated.
        message (str): A string representing the log line.
        separator (str): A string representing by which character
        is separating all fields in the log line.

    Returns:
        str: The obfuscated log message.
    """
    pattern = f'({"|".join(fields)})=.*?(?={separator}|$)'
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with the specified fields to redact
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record and redact sensitive information
        """
        record.msg = filter_datum(self.fields,
                                  self.REDACTION,
                                  record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


PII_FIELDS: Tuple[str, ...] = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    """
    Create and configure a logger named 'user_data'.

    The logger will only log up to logging.INFO level and
    will not propagate messages to other loggers.
    It will have a StreamHandler with RedactingFormatter as formatter.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))

    logger.addHandler(handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """
    Connect to a secure database and return a MySQLConnection object.

    Environment variables for database credentials:
    - PERSONAL_DATA_DB_USERNAME (default: 'root')
    - PERSONAL_DATA_DB_PASSWORD (default: '')
    - PERSONAL_DATA_DB_HOST (default: 'localhost')
    - PERSONAL_DATA_DB_NAME

    Returns:
        connection.MySQLConnection: Connector to the database.
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def main() -> None:
    """
    Main function that retrieves all rows in the users table
    and displays each row under a filtered format.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()

    for row in cursor:
        message = "; ".join([f"{key}={value}" for key, value in row.items()])
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
