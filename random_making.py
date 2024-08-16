import random


# 각 변수 생성
prey_params = [
    random.randrange(0, 1500),  # preyx
    random.randrange(0, 800),   # preyy
    random.randrange(5, 50),    # preywidth
    random.randrange(5, 50),    # preyheight
    random.randrange(4, 10),    # preyspeed
    random.randrange(1, 100),  # preyd_angle
    random.randrange(1, 100),   # preyrotating
    random.randrange(500, 2000),  # preylife
    random.uniform(1, 3)        # preyreproduce
]

hunter_params = [
    random.randrange(0, 1500),  # hunterx
    random.randrange(0, 800),   # huntery
    random.randrange(5, 50),    # hunterwidth
    random.randrange(5, 50),    # hunterheight
    random.randrange(4, 10),    # hunterspeed
    random.randrange(1, 100),  # hunterd_angle
    random.randrange(1, 100),   # hunterrotating
    random.randrange(500, 2000),  # hunterlife
    random.uniform(1, 3)        # hunterreproduce
]

grass_params = [
    random.randrange(200, 500),   # grassnum
    random.randrange(1,10)/1000   # grasstime
]

numbers = [
    random.randrange(1,10),        # preynum
    random.randrange(1,5)         # hunterhum
]

# 파일에 저장
with open("./NSS/GetRandom.txt", 'w') as file:
    params = prey_params + hunter_params + grass_params + numbers
    message = ' '.join(map(str, params))
    file.write(message)
