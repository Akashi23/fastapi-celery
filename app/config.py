import os

REDIS_STORE: str

if not bool(os.getenv('DOCKER')): # if running example without docker
    REDIS_STORE = "redis://:password123@localhost:6379/0"

else: # running example with docker
    REDIS_STORE = "redis://:password123@redis:6379/0"
