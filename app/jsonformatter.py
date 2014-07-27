from models import *

from .util import current_rice_time
from . import users

def get_vote_status(dishdetails):
  vote = db.session.query(DishDetailsAndUserRelationship).filter(DishDetailsAndUserRelationship.dishdetails == dishdetails,DishDetailsAndUserRelationship.user == users.current_user()).scalar()

  if vote is None:
    return "none"
  else:
    return vote.vote_type

def get_dishdetails_data(dishdetails):
  return {
    "name":dishdetails.dish_description,
    "score":dishdetails.score,
    "id": dishdetails.id,
    "servery": get_servery_data(dishdetails.servery),
    "vote_type" : get_vote_status(dishdetails)
  }

def find_mealtime(servery,day_of_the_week,meal_type):
    return db.session.query(MealTime).filter(MealTime.servery==servery,MealTime.day_of_the_week == day_of_the_week,MealTime.meal_type == meal_type).scalar()

def get_servery_data(servery):
    return {
            "name": servery.name,
            "fullname": servery.fullname,
            "id": servery.id,
            "hours": {
                day_of_the_week : {
                    meal_type : {
                        'start_time' : find_mealtime(servery,day_of_the_week,meal_type).start_time,
                        'end_time'   : find_mealtime(servery,day_of_the_week,meal_type).end_time
                        } for meal_type in ['breakfast','lunch','dinner'] if find_mealtime(servery,day_of_the_week,meal_type) != None
                    } for day_of_the_week in range(7)
                },
            "open_now": servery_is_currently_open(servery)
            }


def servery_is_currently_open(servery):
  # gets current time and day of week to see if servery is currently open
  now = current_rice_time()
  day_of_the_week = now.weekday()
  time  = now.time()


  open_filter = db.and_(MealTime.day_of_the_week == day_of_the_week,MealTime.start_time <= time,MealTime.end_time >= time)

  currently_open = db.session.query(MealTime).filter(MealTime.servery == servery).filter(open_filter)


  is_open = len(currently_open.all()) == 1

  return is_open 