'''
This file runs the application using Flask.
'''

from src import (
        app, db,
        create_database_if_not_exists
)


with app.app_context():
    create_database_if_not_exists()
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3000)

