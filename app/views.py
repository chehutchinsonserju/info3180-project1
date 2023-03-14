"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask.helpers import send_from_directory

from app.forms import AddPropertyForm
from app.models import Property


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/properties/create', methods=["GET", "POST"])
def create():
    form = AddPropertyForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Save property data to database
        title = form.title.data
        description = form.description.data
        bedrooms = form.bedrooms.data
        bathrooms = form.bathrooms.data
        price = form.price.data
        location = form.location.data
        type = form.type.data
        photo = form.photo.data
        photo_upload = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_upload))

        property_model = Property(
            title=title,
            description=description,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            price=price,
            location=location,
            type=type,
            photo=photo_upload
        )

        db.session.add(property_model)
        db.session.commit()

        flash('Property successfully saved', 'success')
        return redirect(url_for('properties'))

    return render_template('addproperty.html', form=form)


@app.route('/properties')
def properties():
    properties = Property.query.all()
    return render_template("propertydisplay.html", properties=properties)


@app.route("/property/<property_id>")
def view(property_id):
    prop = Property.query.filter_by(id=property_id).first()

    if prop.photo is not None:
        img_url = url_for('get_image', filename=prop.photo)
    else:
        img_url = None

    return render_template("viewaproperty.html", prop=prop, photo_url=img_url)


@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


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
