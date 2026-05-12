import datetime
import random

def suggest_optimal_slot(doctor_id):
    now = datetime.datetime.now()
    # Logic to reduce waiting time
    suggested_time = now + datetime.timedelta(hours=random.randint(1, 4))
    return suggested_time.strftime("%I:00 %p")