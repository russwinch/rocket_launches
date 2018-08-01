from launches import create_app

app = create_app()

def check_required_folders():
    folders = ['logs',
               'launches/static/rocket_images'
               ]

if __name__ == '__main__':
    app.run(debug=True) #, use_reloader=False)
