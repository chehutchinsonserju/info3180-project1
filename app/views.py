"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

from app import app, db
from app.models import Property
from flask import render_template, request, redirect, url_for, flash
from .forms import AddPropertyForm

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

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

import os
from werkzeug.utils import secure_filename

def save_photo(photo):
    if not photo:
        return None

    filename = secure_filename(photo.filename)
    ext = filename.rsplit('.', 1)[1].lower()

    if ext not in {'jpg', 'jpeg', 'png', 'gif'}:
        return None

    filename = f"{os.urandom(24).hex()}.{ext}"
    photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename


@app.route('/properties/create', methods=['GET', 'POST'])
def addproperty():
    form = AddPropertyForm()
    if form.validate_on_submit():
        photo_path = save_photo(form.photo.data)
        new_property = Property(title=form.title.data, description=form.description.data, rooms=form.rooms.data, bathrooms=form.bathrooms.data, price=form.price.data, property_type=form.property_type.data, location=form.location.data, photo_path=photo_path)
        db.session.add(new_property)
        db.session.commit()
        flash('Property added successfully', 'success')
        return redirect(url_for('properties'))
    return render_template('addproperty.html', form=form)
