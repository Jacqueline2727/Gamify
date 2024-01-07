def initialize():
  global cur_hedons, cur_health #hedons and health of the user
  global estimated_health, estimated_hedons #estimated hedons and health
  global cur_time # current time
  #last activity and its duration - used for running health calculations
  global last_activity, last_activity_duration
  #star activity
  global cur_star_activity, cur_star
  #number of stars offered
  global num_stars
  #last finished with running or carrying textbooks
  global last_finished
  #when the last star was offered
  global last_star_time
  # if the user is bored with stars
  global bored_with_stars
  #list for the times when stars were offered
  global L

  L = []
  estimated_health = 0
  estimated_hedons = 0
  cur_hedons = 0
  cur_health = 0

  last_star_time = 0
  cur_star = None
  cur_star_activity = None
  num_stars = 0
  bored_with_stars = False

  last_activity = None
  last_activity_duration = 0

  cur_time = 0
  last_finished = -1000
  first_star = 0


def perform_activity(activity, duration):
  '''Add hedons and health for the activity performed'''
  global last_start_time, last_activity, last_activity_duration
  global cur_time
  global cur_hedons, cur_health
  global estimated_health, estimated_hedons
  global last_finished
  estimate_hedons_delta(activity, duration)
  estimate_health_delta(activity, duration)
  if activity == "running":
    last_finished = cur_time + duration
    cur_hedons += estimated_hedons
    cur_health += estimated_health
  elif activity == "textbooks":
    last_finished = cur_time + duration
    cur_hedons += estimated_hedons
    cur_health += estimated_health
  elif activity == "resting":
    cur_hedons += estimated_hedons
    cur_health += estimated_health
  else:
    cur_hedons = cur_health
    cur_health = cur_health
  if last_activity == "running":
    temp= last_activity_duration
  else:
    temp = 0
  last_activity = activity
  last_activity_duration = duration + temp
  cur_time += duration


def get_cur_hedons():
  '''Return current hedons'''
  return cur_hedons


def get_cur_health():
  '''Return current health'''
  return cur_health


def star_can_be_taken(activity):
  '''Return if a star can be taken'''
  global bored_with_stars
  global L, cur_time
  global first_star
  global num_stars
  global cur_star_activity
  if bored_with_stars:
    return False
  else:
    if num_stars > 2 and (L[-1] - L[-3]) < 120:
      bored_with_stars = True
      return False
    else:
      if cur_time == last_star_time and cur_star_activity == activity:
        return True
      else:
        return False


def offer_star(activity):
  '''Offer a star for activity'''
  global cur_time, L
  global last_star_time
  global cur_star_activity
  global num_stars
  num_stars += 1
  last_star_time = cur_time
  cur_star_activity = activity
  L.append(cur_time)


def most_fun_activity_minute():
  '''Return the activity that would give the most hedons'''
  estimate_hedons_delta("running", 1)
  run = estimated_hedons
  estimate_hedons_delta("textbooks", 1)
  text = estimated_hedons
  estimate_hedons_delta("resting", 1)
  rest = estimated_hedons
  max_hedons = max(run, text, rest)
  if max_hedons == run:
    return "running"
  elif max_hedons == text:
    return "textbooks"
  else:
    return "resting"


def is_tired():
  '''Return if the user is tired'''
  global last_finished
  global cur_time
  if cur_time - last_finished < 120:
    return True
  else:
    return False


def estimate_hedons_delta(activity, duration):
  '''Estimate the hedons the user will get for an activity'''
  global tired
  global estimated_hedons
  tired = is_tired()
  star = star_can_be_taken(activity)
  if activity == "running":
    if tired and not star:
      estimated_hedons = duration * -2
    elif tired and star:
      if duration <= 10:
        estimated_hedons = 1 * duration
      else:
        estimated_hedons = 10 + (-2 * (duration - 10))
    elif not tired and not star:
      if duration <= 10:
        estimated_hedons = 2 * duration
      else:
        estimated_hedons = 20 + (-2 * (duration - 10))
    else:
      if duration <= 10:
        estimated_hedons = 5 * duration
      else:
        estimated_hedons = 50 + (-2 * (duration - 10))
  elif activity == "textbooks":
    if tired and not star:
      estimated_hedons = duration * -2
    elif tired and star:
      if duration <= 10:
        estimated_hedons = 1 * duration
      else:
        estimated_hedons = 10 + (-2 * (duration - 10))
    elif not tired and not star:
      if duration <= 20:
        estimated_hedons = 1 * duration
      else:
        estimated_hedons = 20 + (-1 * (duration - 20))
    else:
      if duration <= 10:
        estimated_hedons = 4 * duration
      elif duration <= 20:
        estimated_hedons = 40 + (duration - 10)
      else:
        estimated_hedons = 40 + 10 + (-1 * (duration - 20))
  elif activity == "resting":
    estimated_hedons = 0
  else:
    estimated_hedons = 0


def estimate_health_delta(activity, duration):
  '''estimate the health points the user will get for an activity'''
  global estimated_health, last_activity_duration, last_activity
  if activity == "running":
    if last_activity == "running":
      if last_activity_duration + duration > 180:
        if 180-last_activity_duration>0:
          estimated_health = (180 - last_activity_duration) * 3 + (
            duration - (180 - last_activity_duration))
        else:
          estimated_health = duration
      else:
        estimated_health = (duration * 3)
    else:
      if duration <= 180:
        estimated_health = duration * 3
      else:
        estimated_health = 180 * 3 + (duration - 180)
  elif activity == "textbooks":
    estimated_health = 2 * duration
  elif activity == "resting":
    estimated_health = 0
  else:
    estimated_health = 0


if __name__ == '__main__':
  initialize()
