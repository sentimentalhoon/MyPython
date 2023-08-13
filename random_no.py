from fastapi import FastAPI

api = FastAPI()

@api.get('/random_number')

def random_no():
    import random
    
    val_random_number = random.randint(1, 100000000000)
    
    return val_random_number
