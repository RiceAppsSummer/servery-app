from flask import request, abort , jsonify
from datetime import datetime

from . import app
from .util import current_rice_time, parse_to_rice_time
from .models import *

from .jsonformatter import get_servery_data, get_dishdetails_data


@app.route('/api/serveries')
def get_serveries():
  # Query SQL for all serveries
  # returns servery NAME, IMAGE, and LOCATION
  serveries = db.session.query(Servery).all()

  result = {"serveries": [get_servery_data(servery) for servery in serveries]}
  return jsonify(result)

 

@app.route('/api/serveries/<int:servery_id>')
def get_servery(servery_id):
  # Query for all data for specific servery
  # retrieves actual servery
  servery = db.session.query(Servery).get(servery_id) 

  servery_data = get_servery_data(servery)


  return jsonify(servery_data)

@app.route('/api/serveries/<int:servery_id>/menu')
def get_menu(servery_id):
  servery = db.session.query(Servery).get(servery_id)

  if request.args.get("date"):
    date = parse_to_rice_time(request.args.get("date")).date()
  else:
    date = current_rice_time.date()

  meal = request.args.get("meal")
  if not meal:
    meal = 'both'

  if meal == "both":
    query_meals = ["lunch","dinner"]
  else:
    query_meals = [meal]

  menu = {"lunch": [], "dinner": []}

  def meal_type_query(meal_type):
      return db.session.query(Meal).join(Meal.mealtime).filter(
              Meal.date ==date,
              MealTime.meal_type==meal_type,
              MealTime.servery == servery)

  for meal_type in query_meals:
    meal = meal_type_query(meal_type).first()
    if meal:
        menu[meal_type] = map(lambda x: get_dishdetails_data(x.dishdetails),meal.dishes)
  

  return jsonify(menu)


def find_next_meals(date,time):
  """
  Finds the next type of meal for the given day and then returns a list containing the MealTime for every servery
  """

  day_of_the_week = date.weekday()

  # I first find one MealTime that is closest in time
  time_filter = db.and_(MealTime.day_of_the_week == day_of_the_week,MealTime.end_time >= time,MealTime.meal_type != 'breakfast')
  coming_mealtimes = db.session.query(MealTime).filter(time_filter).order_by(MealTime.start_time) 
  first_mealtime = coming_mealtimes.first()


  if first_mealtime is None:
    return find_next_meals(date + datetime.timedelta(1),datetime.time())


  # Then I get all mealtimes of that day and type
  equivalent_mealtime_filter = db.and_(
    MealTime.day_of_the_week == first_mealtime.day_of_the_week,
    MealTime.meal_type == first_mealtime.meal_type)

  all_meals_at_time = db.session.query(MealTime).filter(equivalent_mealtime_filter)

  return all_meals_at_time,date


@app.route('/api/serveries/next_meals')
def get_next_meals():
  """
  Queries the database for the next possible meal.
  """

  now = current_rice_time()
  
  next_mealtimes,next_meal_date = find_next_meals(now.date(),now.time())



  def process_mealtime(mealtime):
    meal = db.session.query(Meal).filter(Meal.mealtime == mealtime,Meal.date == next_meal_date).first()
    
    dishes = meal.dishes

    return {
      "servery": get_servery_data(mealtime.servery),
      "dishes": map(lambda x: get_dishdetails_data(x.dishdetails),dishes),
      "meal_type": mealtime.meal_type
    }


  result = {
    "day": next_meal_date,
    "meals": map(process_mealtime,next_mealtimes)
  }

  return  jsonify(result)