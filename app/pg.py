import psycopg2
import psycopg2.extras
import os
from models import PubMedModel


class PGDatabase:
    """
    A class for interacting with a PostgreSQL database synchronously.
    This class utilizes the psycopg2 library to establish a connection.

    Methods:
    - setup_connection: Sets up a database connection.
    - close_connection: Closes the database connection.
    - post_papers: Posts papers to the database
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PGDatabase, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._DB_CONN_INFO = "dbname='{database}' user='{user}' password='{password}' host='{host}' port='{port}'".format(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT', default=5432)
        )
        self.connection = None
        print(f"PG Instance Created")

    def setup_connection(self):
        self.connection = psycopg2.connect(self._DB_CONN_INFO)

    def close_connection(self):
        if self.connection:
            self.connection.close()

    def post_papers(self, papers: list[PubMedModel]):
        """
        Posts parsed PubMed papers
        """
        try:
            if self.connection is None:
                self.setup_connection()
            with self.connection.cursor() as cursor:
                psycopg2.extras.execute_batch(cursor, """
                    INSERT INTO pub_med_papers(pmid, title, abstract, full_text, authors)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (pmid) DO NOTHING
                    """, [(paper.pmid, paper.title, paper.abstract, paper.full_text, paper.authors) for paper in
                          papers])
                self.connection.commit()
        except Exception as error:
            print(f"Error posting papers: {error}")
            # Optionally rollback on error
            self.connection.rollback()
