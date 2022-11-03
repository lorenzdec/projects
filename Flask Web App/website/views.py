from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

# define this is a blueprint of our application
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])  #the below function whenever you go to /
@login_required #flask login decorator to make sure you can only access this when logged in
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short.', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    # request comes in as data parameter so we must use json
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id: #make sure this is a note owned by the user
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({}) #we just have to return something, so lets return an empty json object

