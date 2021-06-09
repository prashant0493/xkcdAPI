"""data access and storage layer, resolves storage requests by creating custom sql statements based on inputs"""

from typing import List, Dict
from commons.db_con_helper import get_sql_db_connection


def build_upsert_sql_query(
    table_name: str,
    keys_: List,
    value_set_: List
) -> str:
    """Builds sql query based to insert or update.

    Args:
        table_name (str): table under consideration for sql query.
        keys_ (list): list of keys query refers to.
        value_set_ (list): list of values query stores (required for insert and update statements.)

    Returns:
        query (str): complete sql query

    Example -

    INSERT INTO xkcdDB.comics(num, month, link, year, news, safe_title, transcript, alt, img, title, day)
                      VALUES (11, "11", "11", "11", "11", "11", "11", "11", "11", "11", "11"),
                             (33, "11", "99", "99", "99", "99", "99", "99", "99", "99", "99"),
    ON DUPLICATE KEY UPDATE
                        month= VALUES(month),
                        link=VALUES(link),
                        year=VALUES(year),
                        news=VALUES(news),
                        safe_title=VALUES(safe_title),
                        transcript=VALUES(transcript),
                        alt=VALUES(alt),
                        img=VALUES(img),
                        title=VALUES(title),
                        day=VALUES(day);

    """

    def update_clause(keys: List) -> str:
        """
        Args:
            keys (list):

        Returns:
            formatted string for update clause in sql
        """

        if keys:
            clause = ",".join([f"{key_}=VALUES({key_})" for key_ in keys_])
            return " ON DUPLICATE KEY UPDATE " + clause
        return ""

    def get_values(values: list) -> str:
        """
        Args:
            values (list):

        Returns:
            formatted string of values to be inserted
        """

        fmtd_values = ""
        for val in values:
            fmtd_values = fmtd_values + str(val) + ","

        return fmtd_values.rstrip(",")

    sql = f"INSERT INTO {table_name} ({','.join(keys_)}) VALUES {get_values(value_set_)} {update_clause(keys_)};"

    return sql


def upsert_comics(comics: List[Dict]) -> None:
    """
    Bulk inserts values into `comics` table, updates on duplicate key.
    Args:
        comics (list):
    """

    if not comics:
        print("[ WARNING ] nothing to upsert")
        exit()

    key_set = tuple(comics[0].keys())
    value_set = [tuple(comic.values()) for comic in comics]

    connection = get_sql_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = build_upsert_sql_query(
                "xkcdDB.comics",
                key_set,
                value_set
            )
            cursor.execute(sql)
            connection.commit()
    finally:
        connection.close()
