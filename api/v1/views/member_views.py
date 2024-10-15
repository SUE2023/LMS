#!/usr/bin/env python3
""" objects that handle all default RestFul API actions for Members"""
from models.Member import Member
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user

# Managing Library Members: handles registering, updating, and deleting library members

@app.route('/members', methods=['GET'])
def view_members():
    """Retrives all members"""
    members = Member.query.all()
    return render_template('member/members.html', members=members)

@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    """Adds new member"""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_member = Member(name=name, email=email)
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('view_members'))
    return render_template('member/add_member.html')
   
@app_views.route('/member/<member_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/member/put_member.yml', methods=['PUT'])
def put_member(member_id):
    """Updates a member"""
    member = storage.get(Member, mebmer_id)

    if not mebmer:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(mebmer, key, value)
    storage.save()
    return make_response(jsonify(member.to_dict()), 200)
