from flask import request, abort, jsonify

from . import app,db
from .models import *
from .jsonformatter import get_dishdetails_data, get_servery_data

def create_or_get_relationship(dishdetails,user):
  relationship = db.session.query(DishDetailsAndUserRelationship).filter(
    DishDetailsAndUserRelationship.user == user,
    DishDetailsAndUserRelationship.dishdetails == dishdetails).scalar()

  if relationship is None:
    print user,dishdetails
    relationship = DishDetailsAndUserRelationship(user=user,dishdetails=dishdetails)
    db.session.add(relationship)
    db.session.commit()

  return relationship    


@app.route('/api/dishdetails/<int:dishdetails_id>/vote/<vote_type>')
def vote(dishdetails_id,vote_type):
  if vote_type not in ("up","down","none"):
    abort(404)

  user = users.current_user()
  dishdetails = db.session.query(DishDetails).get(dishdetails_id)


  if user is None:
    abort(403)

  relationship = create_or_get_relationship(dishdetails,user)

  update_score_on_vote_removal(relationship)

  relationship.vote_type = vote_type
  
  update_score_on_vote_addition(relationship)

  db.session.commit()

  result = {"new_score": relationship.dishdetails.score}

  return jsonify(result)

def update_score_on_vote_removal(old_vote):
  dishdetails = old_vote.dishdetails
  if old_vote.vote_type == "up":
    dishdetails.score -= 1
  elif old_vote.vote_type == "down":
    dishdetails.score += 1

def update_score_on_vote_addition(new_vote):
  dishdetails = new_vote.dishdetails
  if new_vote.vote_type == "up":
    dishdetails.score += 1
  elif new_vote.vote_type == "down":
    dishdetails.score -= 1  


@app.route('/api/dishdetails/<int:dishdetails_id>')
def get_dishdetails(dishdetails_id):
  dishdetails = db.session.query(DishDetails).get(dishdetails_id)
  return jsonify(get_dishdetails_data(dishdetails))

@app.route('/api/dishdetails/<int:dishdetails_id>/reviews')
def get_dishdetails_reviews(dishdetails_id):
  dishdetails = db.session.query(DishDetails).get(dishdetails_id)
  print dishdetails.reviews
  return jsonify(get_dishdetails_data(dishdetails))