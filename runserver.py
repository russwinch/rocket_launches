"""Run this file to launch the app server."""
from launches import create_app

app = create_app()


if __name__ == '__main__':
    app.run(debug=True) #, use_reloader=False)
