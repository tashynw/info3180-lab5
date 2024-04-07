"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_file, send_from_directory
from app.models import Movie
from app.forms import MovieForm
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


@app.route('/api/v1/movies', methods=["POST"])
def movies():
    form = MovieForm()
    if form.validate_on_submit():
        file = form.poster.data
        filename = secure_filename(file.filename)

        file.save(os.path.join(
            app.config["UPLOAD_FOLDER"], filename
        ))

        movie = Movie(
            title=form.data["title"], description=form.data["description"], poster=filename)
        db.session.add(movie)
        db.session.commit()

        return jsonify({
            "message": "Movie Successfully added",
            "title": form.data["title"],
            "poster": filename,
            "description": form.data["description"]
        })
    else:
        errors = form_errors(form)
        return jsonify({
            "errors": errors
        }), 400


@app.route('/api/v1/movies', methods=["GET"])
def add_movies():
    # GET
    movies = db.session.execute(db.select(Movie)).scalars().all()
    return jsonify({
        "movies": [{"id": m.id, "title": m.title, "description": m.description, "poster": m.poster} for m in movies]
    })


@app.route('/api/v1/posters/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use


def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            )
            error_messages.append(message)

    return error_messages


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
