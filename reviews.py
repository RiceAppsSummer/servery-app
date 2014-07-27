from flask import request, abort, jsonify

from . import app,db
from .models import *
from .jsonformatter import get_dishdetails_data, get_servery_data

@app.route('/api/reviews/<int:review_id>')
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
