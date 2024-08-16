import threading

def make_random():

    import random

    # 각 변수 생성
    prey_params = [
        random.randrange(0, 1500),  # preyx
        random.randrange(0, 800),   # preyy
        random.randrange(5, 50),    # preywidth
        random.randrange(5, 50),    # preyheight
        random.randrange(4, 10),    # preyspeed
        random.randrange(1, 30),  # preyd_angle
        random.randrange(1, 100),   # preyrotating
        random.randrange(500, 2000),  # preylife
        random.uniform(1, 3)        # preyreproduce
    ]

    hunter_params = [
        random.randrange(0, 1500),  # hunterx
        random.randrange(0, 800),   # huntery
        random.randrange(10, 100),    # hunterwidth
        random.randrange(10, 100),    # hunterheight
        random.randrange(4, 10),    # hunterspeed
        random.randrange(1, 30),  # hunterd_angle
        random.randrange(1, 100),   # hunterrotating
        random.randrange(500, 2000),  # hunterlife
        random.uniform(1, 3)        # hunterreproduce
    ]

    grass_params = [
        random.randrange(200, 500),   # grassnum
        1/500 #random.randrange(1,10)/1000   # grasstime
    ]

    numbers = [
        random.randrange(1,10),        # preynum
        random.randrange(1,3)         # hunternum
    ]

    # 파일에 저장
    with open("C:/Users/pc/Documents/GitHub/NSS/NSS/GetRandom.txt", 'w') as file:
        params = prey_params + hunter_params + grass_params + numbers
        message = ' '.join(map(str, params))
        file.write(message)


def main_simulation():

    import random, math, sys, time, pygame, signal
    import threading


    with open("C:/Users/pc/Documents/GitHub/NSS/NSS/GetRandom.txt", 'r') as file:
        preyx, preyy, preywidth, preyheight, preyspeed, preyd_angle, preyrotating, preylife, preyreproduce, hunterx, huntery, hunterwidth, hunterheight, hunterspeed, hunterd_angle, hunterrotating, hunterlife, hunterreproduce, grassnum, grasstime, preynum, hunternum =  map(float,file.read().split())
        data = [preyx, preyy, preywidth, preyheight, preyspeed, preyd_angle, preyrotating, preylife, preyreproduce, hunterx, huntery, hunterwidth, hunterheight, hunterspeed, hunterd_angle, hunterrotating, hunterlife, hunterreproduce, grassnum, grasstime, preynum, hunternum]


    # 초기화
    pygame.init()

    # 이미지 경로
    prey_img = pygame.image.load("C:/Users/pc/Documents/GitHub/NSS/NSS/PreyImage.png")
    hunter_img = pygame.image.load("C:/Users/pc/Documents/GitHub/NSS/NSS/HunterImage.png")
    grass_img = pygame.image.load("C:/Users/pc/Documents/GitHub/NSS/NSS/GrassImage.png")

    # 화면 설정
    S_wdw_size = (640, 480)
    L_wdw_size = (1500, 800)
    window_size = L_wdw_size
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Natural Selection Simulation Simulation")

    # 색 설정
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # 자막 설정
    MyFont = pygame.font.SysFont(None, 20)

    rot_angle = 0

    PreySpeedData = []
    PreyWidthData = []
    PreyHeightData = []
    Preyd_AngleData = []
    PreyLifeData = []

    HunterSpeedData = []
    HunterWidthData = []
    HunterHeightData = []
    Hunterd_AngleData = []
    HunterLifeData = []
    #######################################################

    # Prey 클래스 정의
    class Prey:
        def __init__(self, x, y, width, height, speed, d_angle, rotating, life):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.speed = speed
            self.d_angle = d_angle
            self.angle = 0
            self.rotating = rotating
            self.life = life
            self.prey_img = pygame.transform.scale(prey_img, (self.width, self.height))
            self.lifetext = MyFont.render(str(int(self.life)), True, WHITE)

        # Prey 수명 가시화
        def countlife(self):
            self.lifetext = MyFont.render(str(int(self.life)), True, WHITE)
            return self.lifetext

        # Prey 움직임
        def move(self):
            boundary = window_size
            pos_neg = random.choice([1, -1])
            self.angle = self.angle + self.d_angle * pos_neg

            new_x = self.x + self.speed * math.cos(math.radians(self.angle))
            new_y = self.y + self.speed * math.sin(math.radians(self.angle))

            if 0 <= new_x + self.width / 2 <= boundary[0] and 0 <= new_y + self.height / 2 <= boundary[1]:
                self.x = new_x
                self.y = new_y
            else:
                self.angle -= 180
                new_x = self.x + self.speed * math.cos(math.radians(self.angle))
                new_y = self.y + self.speed * math.sin(math.radians(self.angle))
                self.x = new_x
                self.y = new_y

        # Prey 회전
        def rotate(self):
            global rot_angle
            rot_angle += random.uniform(0, self.rotating)
            new_img = pygame.transform.rotozoom(prey_img, rot_angle / 3, 1)
            rect = new_img.get_rect()
            rect.center = (self.x + self.width / 2, self.y - self.height / 2)
            self.prey_img = pygame.transform.rotate(new_img, rot_angle / 3)

        # Prey 그리기
        def draw(self):
            screen.blit(self.prey_img, (self.x, self.y))

        # Prey 복제
        def reproduce(self):
            reproduce_life = data[8] *  data[7]
            if self.life >= reproduce_life:
                self.life -= data[7]

                variations = []
                for _ in range(6):
                    variations.append((random.uniform(20, -20) + 100) / 100)

                new_width = self.width * variations[0]
                new_height = self.height * variations[1]
                new_speed = self.speed * variations[2]
                new_d_angle = self.d_angle * variations[3]
                new_rotating = self.rotating * variations[4]
                new_life = self.life * variations[5]

                new_prey = Prey(self.x, self.y, new_width, new_height, new_speed, new_d_angle, new_rotating, new_life)
                preys.append(new_prey)

                PreySpeedData.append(new_speed)
                PreyWidthData.append(new_width)
                PreyHeightData.append(new_height)
                Preyd_AngleData.append(new_d_angle)
                PreyLifeData.append(new_life)
        # Prey가 Grass 먹기
        def eat_Grass(self, grasses):
            for grass in grasses:
                if math.sqrt(((grass.x + grass.width / 2) - (self.x + self.width / 2)) ** 2 + ((grass.y + grass.height / 2) - (self.y + self.height / 2)) ** 2) * abs(math.cos(math.atan(((grass.y + grass.height / 2) - (self.y + self.height / 2)) / ((grass.x + grass.width / 2) - (self.x + self.width / 2))) + math.radians(rot_angle))) - (self.width + grass.width) / 2 <= 0 and \
                math.sqrt(((grass.x + grass.width / 2) - (self.x + self.width / 2)) ** 2 + ((grass.y + grass.height / 2) - (self.y + self.height / 2)) ** 2) * abs(math.sin(math.atan(((grass.y + grass.height / 2) - (self.y + self.height / 2)) / ((grass.x + grass.width / 2) - (self.x + self.width / 2))) + math.radians(rot_angle))) - (self.height + grass.height) / 2 <= 0:
                    grasses.remove(grass)
                    self.life += (1 - (self.width + self.height) / 100) * 100

        #그래프화
        def dataization(self):
                PreySpeedData.append(self.speed)
                PreyWidthData.append(self.width)
                PreyHeightData.append(self.height)
                Preyd_AngleData.append(self.d_angle)
                PreyLifeData.append(self.life)

    ############################################################

    # Hunter 클래스 정의
    class Hunter:
        def __init__(self, x, y, width, height, speed, d_angle, rotating, life):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.speed = speed
            self.d_angle = d_angle
            self.angle = 0
            self.rotating = rotating
            self.rotation_direction = random.choice([-1, 1])
            self.life = life
            self.hunter_img = pygame.transform.scale(hunter_img, (self.width, self.height))
            self.lifetext = MyFont.render(str(int(self.life)), True, WHITE)
            HunterSpeedData.append(self.speed)
            HunterWidthData.append(self.width)
            HunterHeightData.append(self.height)
            Hunterd_AngleData.append(self.d_angle)
            HunterLifeData.append(self.life)

        def countlife(self):
            self.lifetext = MyFont.render(str(int(self.life)), True, WHITE)
            return self.lifetext

        def move(self):
            boundary = window_size
            pos_neg = random.choice([1, -1])
            self.angle = self.angle + self.d_angle * pos_neg

            new_x = self.x + self.speed * math.cos(math.radians(self.angle))
            new_y = self.y + self.speed * math.sin(math.radians(self.angle))


            if 0 <= new_x <= boundary[0] and 0 <= new_y <= boundary[1]:
                self.x = new_x
                self.y = new_y
            else:
                self.angle -= 180
                new_x = self.x + self.speed * math.cos(math.radians(self.angle))
                new_y = self.y + self.speed * math.sin(math.radians(self.angle))
                self.x = new_x
                self.y = new_y

        def rotate(self):
            global rot_angle
            rot_angle += random.uniform(0, self.rotating)
            new_img = pygame.transform.rotozoom(hunter_img, rot_angle / 3, 1)
            rect = new_img.get_rect()
            rect.center = (self.x + self.width / 2, self.y - self.height / 2)
            self.hunter_img = pygame.transform.rotate(new_img, rot_angle / 3)

        def draw(self):
            screen.blit(self.hunter_img, (self.x, self.y))

        def reproduce(self):
            reproduce_life = data[17] * data[16]
            if self.life >= reproduce_life:
                self.life -= data[16]

                variations = []
                for _ in range(6):
                    variations.append((random.uniform(20, -20) + 100) / 100)

                new_width = self.width * variations[0]
                new_height = self.height * variations[1]
                new_speed = self.speed * variations[2]
                new_d_angle = self.d_angle * variations[3]
                new_rotating = self.rotating * variations[4]
                new_life = self.life * variations[5]

                new_hunter = Hunter(self.x, self.y, new_width, new_height, new_speed, new_d_angle, new_rotating, new_life)
                hunters.append(new_hunter)

        def eat_Prey(self, preys):
            for prey in preys:
                if math.sqrt((( prey.x +  prey.width / 2) - (self.x + self.width / 2)) ** 2 + (( prey.y +  prey.height / 2) - (self.y + self.height / 2)) ** 2) * abs(math.cos(math.atan((( prey.y +  prey.height / 2) - (self.y + self.height / 2)) / (( prey.x +  prey.width / 2) - (self.x + self.width / 2))) + math.radians(rot_angle))) - (self.width +  prey.width) / 2 <= 0 and \
                math.sqrt((( prey.x +  prey.width / 2) - (self.x + self.width / 2)) ** 2 + (( prey.y +  prey.height / 2) - (self.y + self.height / 2)) ** 2) * abs(math.sin(math.atan((( prey.y +  prey.height / 2) - (self.y + self.height / 2)) / (( prey.x +  prey.width / 2) - (self.x + self.width / 2))) + math.radians(rot_angle))) - (self.height +  prey.height) / 2 <= 0:
                    
                    preys.remove(prey)
                    self.life += (self.width + self.height) / 60 * 100

        def dataization(self):
                HunterSpeedData.append(self.speed)
                HunterWidthData.append(self.width)
                HunterHeightData.append(self.height)
                Hunterd_AngleData.append(self.d_angle)
                HunterLifeData.append(self.life)

    ###########################################################

    # Grass 클래스 정의
    class Grass:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.width = 7
            self.height = 7
            self.grass_img = pygame.transform.scale(grass_img, (self.width, self.height))

        def draw(self):
            screen.blit(self.grass_img, (self.x, self.y))

    ##########################################################

    # Main 함수
    def main():
        start = pygame.time.get_ticks()
        global prey_img, hunter_img, grass_img, preys, hunters, grasses

        clock = pygame.time.Clock()
        running = True

        
        # x, y, width, height, speed, d_angle, rotating, life
        preys = []
        hunters = []
        grasses = []

        for _ in range(int(data[20])):
            variations = []
            for _ in range(6):
                variations.append((random.uniform(10, -10) + 100) / 100)

            new_width = data[2] * variations[0]
            new_height = data[3] * variations[1]
            new_speed = data[4] * variations[2]
            new_d_angle = data[5] * variations[3]
            new_rotating = data[6] * variations[4]
            new_life = data[7] * variations[5]

            new_prey = Prey(data[0], data[1], new_width, new_height, new_speed, new_d_angle, new_rotating, new_life)
            preys.append(new_prey)
        
        for _ in range(int(data[21])):
            variations = []
            for _ in range(6):
                variations.append((random.uniform(10, -10) + 100) / 100)

            new_width = data[11] * variations[0]
            new_height = data[12] * variations[1]
            new_speed = data[13] * variations[2]
            new_d_angle = data[14] * variations[3]
            new_rotating = data[15] * variations[4]
            new_life = data[16] * variations[5]

            new_hunter = Hunter(data[9], data[10], new_width, new_height, new_speed, new_d_angle, new_rotating, new_life)
            hunters.append(new_hunter)

        for _ in range(int(data[18])):
            x = random.randint(0, window_size[0])
            y = random.randint(0, window_size[1])
            grasses.append(Grass(x, y))
            lastcreating = time.time()

        tickrate = 300
        
        while running:
            now = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s and tickrate > 10:
                        tickrate -=10
                        print(tickrate)
                        
                    if event.key == pygame.K_w:
                        tickrate +=10
                        print(tickrate)
                    if event.key == pygame.K_k:
                        del hunters[0]

            # 화면 검은색으로 덮고 그리고 반복
            screen.fill(BLACK)

            # Grass 관련
            for grass in grasses:
                grass.draw()
                Ctime = time.time()

                if Ctime - lastcreating >= data[19]:
                    for i in range(1):
                        x = random.randint(0, window_size[0])
                        y = random.randint(0, window_size[1])
                        grasses.append(Grass(x, y))
                        lastcreating = time.time()

            # Prey 관련
            for prey in preys:
                prey.move()
                prey.draw()
                prey.countlife()
                screen.blit(prey.lifetext, (prey.x + prey.width / 2 - 10, prey.y + prey.height / 2 - 10))

                prey.life -= (prey.speed + prey.width/5 + prey.height/5) / 5
                if prey.life <= 0:
                    preys.remove(prey)

                prey.reproduce()

                prey.eat_Grass(grasses)

                #prey.rotate()

            # Hunter 관련
            for hunter in hunters:
                hunter.move()
                hunter.draw()
                hunter.countlife()
                screen.blit(hunter.lifetext, (hunter.x + hunter.width / 2 - 10, hunter.y + hunter.height / 2 - 10))
                if len(hunters)!=1:
                    hunter.life -= (hunter.speed + hunter.width + hunter.height) / 50
                if hunter.life <= 0 :
                    hunters.remove(hunter)
                

                hunter.reproduce()

                hunter.eat_Prey(preys)

                #hunter.rotate()
            if now - start >= 1000:
            
                HunterSpeedData.clear()
                HunterWidthData.clear()
                HunterHeightData.clear()
                Hunterd_AngleData.clear()
                HunterLifeData.clear()

                PreySpeedData.clear()
                PreyWidthData.clear()
                PreyHeightData.clear()
                Preyd_AngleData.clear()
                PreyLifeData.clear()
                
                for prey in preys:
                    prey.dataization()
                for hunter in hunters:
                    hunter.dataization()
                
                
                def calculate_average(list):
                    if not list:
                        return 0.0
                    
                    total = sum(float(x) for x in list)
                    
                    average = total / len(list)
                    
                    return average    


                PWA = calculate_average(PreyWidthData)
                PHA = calculate_average(PreyHeightData)
                PSA = calculate_average(PreySpeedData)
                PdA = calculate_average(Preyd_AngleData)
                PLA = calculate_average(PreyLifeData)


                HWA = calculate_average(HunterWidthData)
                HHA = calculate_average(HunterHeightData)
                HSA = calculate_average(HunterSpeedData)
                HdA = calculate_average(Hunterd_AngleData)
                HLA = calculate_average(HunterLifeData)

                with open("C:/Users/pc/Documents/GitHub/NSS/NSS/DATA.txt", 'w') as file:
                    file.write(str(PWA) + ' ' + str(PHA) + ' ' + str(PSA) + ' ' + str(PdA) + ' ' + str(PLA) + ' ' + str(HWA) + ' ' + str(HHA) + ' '+ str(HSA) + ' '+ str(HdA) + ' '+ str(HLA))


            # 화면 업데이트
            pygame.display.flip()
            clock.tick(tickrate)

            #데이터 리턴

    if __name__ == "__main__":
        main()

def start():
    make_random()
    main_simulation()

if __name__ == "__main__":
    start()