from app import app,SocketIO

if __name__ == '__main__':
    SocketIO.run(app)

    #Gunicorn and WSGI server (Web Server Gateway Interface) are used 
    # to serve the Flask application in production.