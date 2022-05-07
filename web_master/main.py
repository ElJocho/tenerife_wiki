from website import create_app
from config import DATABASE_CONNECTION_URI

app = create_app(DATABASE_CONNECTION_URI)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)