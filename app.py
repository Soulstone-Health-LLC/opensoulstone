'''
This file runs the application using Flask.
'''

from src import app


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3000)
