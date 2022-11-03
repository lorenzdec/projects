from website import create_app #if you make an __init__.py file in a folder, it becomes a python package and you can import from it

app = create_app()

if __name__ == '__main__':  #if we run the file, not if we import the file, will we run the app
    app.run(debug=True) #runs our flask app/start up a webserver and because debug=True, everytime we make a change in python code it will re-run the server

