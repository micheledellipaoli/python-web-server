from flask import Flask


# "app" is an instance of the Flask class, which works as our web application
# "__name__" is the name of the application’s package. This is needed so that Flask knows where to look for resources, such as templates and files.
app = Flask(__name__)

# "route" is a decorator useful to tell Flask what URL triggers our function (called web_server)
@app.route("/")
def web_server():
    # the function "web_server()" returns the message we want to display in the user’s browser. The default content type is HTML.
    return '''<html>
                <head>
                    <title>Laboratorio 1 - Michele Delli Paoli</title>
                </head>
                <body>
                    <h1>Benvenuto!</h1>
                    <br>
                    <h2>Questo è il mio primo Web Server sviluppato in Python.</h2>
                </body>
            </html>'''

def main():
    app.run(debug=True, host='0.0.0.0')

if __name__ == "__main__":
    main()