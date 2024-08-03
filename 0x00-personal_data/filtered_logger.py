#!/usr/bin/env python3
""" 0x00. Personal Data """
import re
from typing import List
import logging
import os
import mysql.connector


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """ Filter data """
    for field in fields:
        regex = f"{field}=[^{separator}]*"
        message = re.sub(regex, f"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Filter data """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Filter data """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filter data """
        org = super().format(record)
        return filter_datum(self.fields, self.REDACTION, org, self.SEPARATOR)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """ Filter data """
    log = logging.getLogger("user_data")
    log.setLevel(logging.INFO)
    log.propagate = False
    sh = logging.StreamHandler()
    sh.setFormatter(RedactingFormatter(PII_FIELDS))
    log.addHandler(sh)
    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Filter data
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME") or "root"
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD") or ""
    host = os.getenv("PERSONAL_DATA_DB_HOST") or "localhost"
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    conn = mysql.connector.connect(
        user=username, password=password, host=host, database=db_name
    )

    return conn


def main() -> None:
    """ Filter data """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    log = get_logger()
    for row in cursor:
        data = []
        for desc, value in zip(cursor.description, row):
            pair = f"{desc[0]}={str(value)}"
            data.append(pair)
        row_str = "; ".join(data)
        log.info(row_str)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
