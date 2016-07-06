""" The main pythonista.cloud application. Contains the basic logic for
pythonista.cloud. """

import os.path

import flask

from application import couchdb

localdir = os.path.abspath(os.path.dirname(__file__))
staticdir = os.path.join(localdir, "../static")

app = flask.Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """ Return the main page (from /site/main.html) for requests to the file
    root """
    return flask.send_file(os.path.join(staticdir, "main.html"))


@app.route("/", methods=["POST"])
def submit():
    """Allow submission of new packages via a POST request.

    This automatically raises intelligent-ish errors"""
    # Parse JSON of request
    data = flask.request.get_json(force=True, silent=True)
    if data is None:  # If data is none, it fails
        return flask.jsonify(**{
            "success": False,
            "error": {
                "type": "ValueError",
                "message": "Could not parse JSON"
            }
        })

    # Add to index
    try:
        info = couchdb.add_package(data)
    except Exception as e:
        return flask.jsonify(**{
            "success": False,
            "error": {
                "type": type(e).__name__,
                # HTTPError doesn't have a message, so return the status code.
                "message": str(e)
            }
        })

    # Report success
    return flask.jsonify(**{
        "success": True,
        "url": "http://db.pythonista.cloud/{}".format(info["name"]),
        "data": info
    })


@app.route("/<path:filepath>/")
def returnFile(filepath):
    """ Attempt to return files from site from their equivalent path at the
    root (/main.html -> /static/main.html) """
    joined = os.path.join(staticdir, filepath)
    print(joined)
    if os.path.isdir(joined):
        return flask.send_from_directory(joined, "index.html")
    else:
        return flask.send_from_directory(staticdir, filepath)
