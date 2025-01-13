
from flask import request, render_template, make_response

from server.webapp import flaskapp, cursor
from server.models import Book

from azure.cosmos import CosmosClient, exceptions

import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@flaskapp.route('/')
def index():
    name = request.args.get('name')
    author = request.args.get('author')
    read = bool(request.args.get('read'))

    if name:
        cursor.execute(
            "SELECT * FROM books WHERE name LIKE '%" + name + "%'"
        )
        books = [Book(*row) for row in cursor]

    elif author:
        cursor.execute(
            "SELECT * FROM books WHERE author LIKE '%" + author + "%'"
        )
        books = [Book(*row) for row in cursor]

    else:
        cursor.execute("SELECT name, author, read FROM books")
        books = [Book(*row) for row in cursor]

    return render_template('books.html', books=books)


client = CosmosClient.from_connection_string(os.environ.get("DB_CONNECTION_STRING"))
database = client.get_database_client(os.environ.get("DATABASE_NAME"))
container = database.get_container_client(os.environ.get("CONTAINER_NAME"))

@flaskapp.route("/test")
def cosmos_test():
    test_id = request.args.get('test_id')
    sec_id = request.args.get('sec_id')

    cursor.execute(f"SELECT * FROM c WHERE c.testId = '{test_id}' AND c.secId = '{sec_id}'")
    return [Book(*row) for row in cursor]
    # return list(container.query_items(query=query, enable_cross_partition_query=True))