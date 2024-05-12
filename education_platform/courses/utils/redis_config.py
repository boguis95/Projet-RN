import redis
from datetime import timedelta

def get_redis_connection():
    return redis.StrictRedis(host='localhost', port=6379, db=0)

def set_key_with_expiration(key, value, expiration_time_in_minutes):
    r = get_redis_connection()
    r.setex(key, timedelta(minutes=expiration_time_in_minutes), value)

def refresh_key_expiration(key, new_expiration_time_in_minutes):
    r = get_redis_connection()
    r.expire(key, timedelta(minutes=new_expiration_time_in_minutes))
