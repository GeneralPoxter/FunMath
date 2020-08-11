import pygame, os, sys
import random, math
try:
    base_path = sys._MEIPASS
except Exception:
    base_path = os.path.dirname(__file__)
os.chdir(os.path.join(base_path, "images"))
pygame.init()
pygame.display.set_caption("FunMath")
screen = pygame.display.set_mode((1000,800))
done = False

def Arithmetic_Adventure():
  def renderText(inputText,inputCoordinates,inputSize,inputColor,screen):
      font = pygame.font.SysFont("comicsansms",inputSize)
      text = []
      for e in inputText:
          text.append(font.render(e,True,inputColor))
      for e in range(len(text)):
          screen.blit(text[e],inputCoordinates[e])
  
  def generateEquation(xy):
      xy[0] = str(random.randint(-12,12)) + " " + random.choice(["+","-"]) + " " + str(random.randint(-12,12))
      xy[1] = str(random.randint(-12,12)) + " " + random.choice(["+","-"]) + " " + str(random.randint(-12,12))
      return xy
  
  def createCheck(chests):
      global chestsCheck
      chestsCheck = []
      for i in chests:
          chestsCheck.append([int(eval(i[0])),int(eval(i[1]))])
          
  def newClue(chests):
      createCheck(chests)
      variableList = generateEquation(["",""])
      while (int(eval(variableList[0])) > 12 or int(eval(variableList[0])) < -12) or (int(eval(variableList[1])) > 12 or int(eval(variableList[1])) < -12) or [int(eval(variableList[0])),int(eval(variableList[1]))] in chestsCheck:
          variableList = generateEquation(["",""])
      return [variableList[0],variableList[1]]
  
  def displayHint(chests):
      pygame.init()
  
      while True:
          screen = pygame.display.set_mode((1000,800))
          if(pygame.QUIT in [i.type for i in pygame.event.get()]):return
          pressed = pygame.key.get_pressed()
          if pressed[pygame.K_SPACE]:return
          
          screen.fill((50,75,15))
          if chestNum < 4:
              renderText(["The location of the next clue is:","x =  " + chests[0],"y =  " + chests[1],"Press SPACE to continue"],[[165,250],[350,310],[350,370],[225,475]],48,(255,215,0),screen)
          else:
              renderText(["The location of the treasure chest is:","x =  " + chests[0],"y =  " + chests[1],"Press SPACE to continue"],[[100,300],[350,360],[350,420],[225,525]],48,(255,215,0),screen)
  
          pygame.display.flip()
          
  def main():
      pygame.init()
      screen = pygame.display.set_mode((1000,800))
      coordinates = [0,0]
      ticker = 0
      tree = pygame.image.load("tree.png")
      rock = pygame.image.load("rock.png")
      player = pygame.image.load("adventurer.png")
      features = [[],[]]
      for x in range(-12,12):
          for y in range(-12,12):
              if random.randint(1,4) == 1:
                  features[random.randint(0,1)].append([x,y])
      chestsList = [['0','0']]
      for i in range(4):
          chestsList.append(newClue(chestsList))
      createCheck(chestsList)
      global chestNum
      chestNum = 0
  
      while True:
          for event in pygame.event.get():
              if event.type == pygame.QUIT:return
              elif event.type == pygame.MOUSEBUTTONDOWN:
                  loc = pygame.mouse.get_pos()
                  if loc[0] > 805 and loc[0] < 975 and loc[1] > 300 and loc[1] < 504:
                      displayHint(chestsList[chestNum])
  
          if ticker > 0:
              ticker -= 1
          pressed = pygame.key.get_pressed()
          if ticker == 0:
              if pressed[pygame.K_UP] or pressed[pygame.K_DOWN] or pressed[pygame.K_RIGHT] or pressed[pygame.K_LEFT]:
                  ticker = 35
              if pressed[pygame.K_UP] and coordinates[1] + 1 <= 12: coordinates[1] += 1
              elif pressed[pygame.K_DOWN] and coordinates[1] - 1 >= -12:coordinates[1] -= 1
              elif pressed[pygame.K_RIGHT] and coordinates[0] + 1 <= 12:coordinates[0] += 1
              elif pressed[pygame.K_LEFT] and coordinates[0] - 1 >= -12:coordinates[0] -= 1
          xshift = coordinates[0] - 2
          yshift = coordinates[1] + 2
          
          screen.fill((87,59,12))
          for x in range(5):
              tileCoordinates = [x + xshift,0]
              for y in range(5):
                  tileCoordinates[1] = (y * -1) + yshift
                  if tileCoordinates[0] >= -12 and tileCoordinates[0] <= 12 and tileCoordinates[1] >= -12 and tileCoordinates[1] <= 12:
                      pygame.draw.rect(screen,(34,139,34),pygame.Rect((20 * (x + 1)) + (136 * x),(20 * (y + 1)) + (136 * y),136,136))
                  else:
                      pygame.draw.rect(screen,(0,0,0),pygame.Rect((20 * (x + 1)) + (136 * x),(20 * (y + 1)) + (136 * y),136,136))
                  if tileCoordinates in features[0]:
                      screen.blit(pygame.transform.scale(tree,(130,130)),((20 * (x + 1)) + (136 * x),(20 * (y + 1)) + (136 * y)))
                  elif tileCoordinates in features[1]:
                      screen.blit(pygame.transform.scale(rock,(130,130)),((20 * (x + 1)) + (136 * x),(20 * (y + 1)) + (136 * y)))
          screen.blit(pygame.transform.scale(player,(125,130)),(332,335))
  
          renderText(["Coordinates:","x = " + str(coordinates[0]) + "  y = " + str(coordinates[1])],[(805,20),(805,50)],28,(255,255,255),screen)
          pygame.draw.rect(screen,(50,75,15),pygame.Rect(805,300,170,204))
          renderText(["Click here","for Clue"],[(830,380),(840,410)],24,(255,215,0),screen)
          
          if coordinates == chestsCheck[chestNum]:
              pygame.display.flip()
              initial = pygame.time.get_ticks()
              while pygame.time.get_ticks() - initial < 2000:
                  for event in pygame.event.get():
                      if event.type == pygame.QUIT:return
              chestNum += 1
              if chestNum < 5:
                  renderText(["Congratulations!","You found a clue!"],[[225,100],[215,160]],48,(255,215,0),screen)
                  pygame.display.flip()
                  initial = pygame.time.get_ticks()
                  while pygame.time.get_ticks() - initial < 2000:
                      for event in pygame.event.get():
                          if event.type == pygame.QUIT:return
                  displayHint(chestsList[chestNum])
              else:
                  while True:
                    for event in pygame.event.get():
                      if event.type == pygame.QUIT:return
                    screen.fill((50,75,15))
                    renderText(["Congratulations!","You found the treasure chest!","Click the red 'x' on the","top right of the screen to exit"],[[300,100],[155,160],[225,250],[155,310]],48,(255,215,0),screen)
                    pygame.display.flip()
              
          pygame.display.flip()
          
  main()

def Multiplication_Muggers():
  def renderText(inputText,inputCoordinates,inputSize,inputColor,screen):
      font = pygame.font.SysFont("comicsansms",inputSize)
      text = []
      for e in inputText:
          text.append(font.render(e,True,inputColor))
      for e in range(len(text)):
          screen.blit(text[e],inputCoordinates[e])
          
  def muggersMove(locations,userLocation):
      for i in locations:
          index = random.choice([0,1])
          movement = random.choice([1,0,-1])
          locations[locations.index(i)][index] += movement
          while locations[locations.index(i)][index] < -12 or locations[locations.index(i)][index] > 12 or locations.count(locations[locations.index(i)]) > 1 or locations[locations.index(i)] == userLocation:
              locations[locations.index(i)][index] -= movement
              movement = random.choice([1,0,-1])
              locations[locations.index(i)][index] += movement
      return locations
  
  def catchCheck(locations,userLocation):
      count = 0
      for i in locations:
          if [i[0]+1,i[1]] == userLocation or [i[0]-1,i[1]] == userLocation or [i[0],i[1] + 1] == userLocation or [i[0],i[1]-1] == userLocation:
              count += 1
      if count > 1:return "0"
      elif count == 1:return "1"
      else:return "2"
  
  def question():
      pygame.init()
      screen = pygame.display.set_mode((1000,800))
      
      while True:
          for event in pygame.event.get():
              if event.type == pygame.QUIT:return "exit"
              
          pressed = pygame.key.get_pressed()
          if pressed[pygame.K_SPACE]:
              number1 = random.randint(1,99)
              number2 = random.randint(1,99)
              multiplicationList = [str(number1),str(number2),str(number1*number2)]
              userAnswer = ""
                  
              while True:
                  for event in pygame.event.get():
                      if event.type == pygame.QUIT:return "exit"
                      elif event.type == pygame.KEYDOWN:
                          if pygame.key.name(event.key) in ["0","1","2","3","4","5","6","7","8","9"] and len(userAnswer) < 5:userAnswer += pygame.key.name(event.key)
                          elif pygame.key.name(event.key) == "backspace":userAnswer = userAnswer[:-1]
                          elif pygame.key.name(event.key) == "return":
                              while True:
                                  for event in pygame.event.get():
                                      if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and pygame.key.name(event.key) == "space"):
                                          if userAnswer == multiplicationList[2]:
                                              global caught
                                              caught += 1
                                          global remaining
                                          remaining -= 1
                                          return
                                  
                                  screen.fill((0,0,128))
                                  if userAnswer == multiplicationList[2]:
                                      renderText(["You successfully captured the mugger!","Press SPACE to continue"],[[70,340],[240,410]],48,(176,196,222),screen)
                                  else:
                                      renderText(["The mugger escaped!","Press SPACE to continue"],[[280,340],[240,410]],48,(176,196,222),screen)
  
                                  pygame.display.flip()
                                  
                  screen.fill((0,0,128))
                  pygame.draw.rect(screen,(176,196,222),pygame.Rect(250,100,500,60))
                  renderText([userAnswer],[[250,100]],48,(255,255,0),screen)
                  renderText(["Enter the answer of the following multiplication expression","Type your answer using numbers only and press BACKSPACE to delete","Press ENTER to submit when you are ready"],[[165,250],[105,290],[255,330]],24,(176,196,222),screen)
                  renderText([multiplicationList[0] + " × " + multiplicationList[1]],[[420,450]],48,(176,196,222),screen)
                  
                  pygame.display.flip()               
  
          screen.fill((0,0,128))
          renderText(["Good work!","You found a mugger!","Now it's time to catch him!","Press SPACE when you are ready"],[[375,120],[275,180],[200,400],[140,460]],48,(176,196,222),screen)
  
          pygame.display.flip()
      
  def catch(locations,userLocation):
      while catchCheck(locations,userLocation) == "0":
          locations = muggersMove(locations)
      if catchCheck(locations,userLocation) == "1":
          initial = pygame.time.get_ticks()
          while pygame.time.get_ticks() - initial < 2000:
              allEvents = pygame.event.get()
              for event in allEvents:
                  if event.type == pygame.QUIT:return "exit"
          stop = question()
          if stop == "exit":return "exit"
          for i in locations:
              if [i[0]+1,i[1]] == userLocation or [i[0]-1,i[1]] == userLocation or [i[0],i[1] + 1] == userLocation or [i[0],i[1]-1] == userLocation:
                  locations.remove(i)
                  return locations
      else:
          return locations
      
  def main():
      pygame.init()
      screen = pygame.display.set_mode((1000,800))
      coordinates = [0,0]
      ticker = 0
      count = 10
      player = pygame.image.load("police.png")
      mugger = pygame.image.load("mugger.png")
      building = pygame.image.load("skyscraper.png")
      features = []
      people = []
      peopleImages = []
      for i in range(8):
          peopleImages.append(pygame.image.load("person" + str(i + 1) + ".png"))
      for x in range(-12,12):
          for y in range(-12,12):
              if random.randint(1,7) == 1:
                  features.append([x,y])
              if random.randint(1,3) == 1:
                  people.extend([[x,y],peopleImages[random.randint(0,7)]])
      muggersCoordinates = [[random.randint(-12,12),random.randint(-12,12)],[random.randint(-12,12),random.randint(-12,12)],[random.randint(-12,12),random.randint(-12,12)]]
      for i in muggersCoordinates:
          while muggersCoordinates.count(muggersCoordinates[muggersCoordinates.index(i)]) > 1 or muggersCoordinates[muggersCoordinates.index(i)] in [[0,0],[0,1],[0,-1],[1,0],[-1,0]]:
              newCoordinates = [random.randint(-12,12),random.randint(-12,12)]
              muggersCoordinates[muggersCoordinates.index(i)] = newCoordinates
              i = newCoordinates
      global remaining
      remaining = 3
      global caught
      caught = 0
      
      while True:
          for event in pygame.event.get():
              if event.type == pygame.QUIT:return
  
          if ticker > 0:
              ticker -= 1
          pressed = pygame.key.get_pressed()
          if ticker == 0:
              if pressed[pygame.K_UP] or pressed[pygame.K_DOWN] or pressed[pygame.K_RIGHT] or pressed[pygame.K_LEFT]:
                  ticker = 35
                  count += 1
                  if pressed[pygame.K_UP] and coordinates[1] + 1 <= 12: coordinates[1] += 1
                  elif pressed[pygame.K_DOWN] and coordinates[1] - 1 >= -12:coordinates[1] -= 1
                  elif pressed[pygame.K_RIGHT] and coordinates[0] + 1 <= 12:coordinates[0] += 1
                  elif pressed[pygame.K_LEFT] and coordinates[0] - 1 >= -12:coordinates[0] -= 1
                  muggersCoordinates = muggersMove(muggersCoordinates,coordinates)
          xshift = coordinates[0] - 2
          yshift = coordinates[1] + 2
  
          screen.fill((0,0,128))
          for x in range(5):
              tileCoordinates = [x + xshift,0]
              for y in range(5):
                  tileCoordinates[1] = (y * -1) + yshift
                  if tileCoordinates[0] >= -12 and tileCoordinates[0] <= 12 and tileCoordinates[1] >= -12 and tileCoordinates[1] <= 12:
                      pygame.draw.rect(screen,(176,196,222),pygame.Rect((20 * (x + 1)) + (136 * x),(20 * (y + 1)) + (136 * y),136,136))
                  else:
                      pygame.draw.rect(screen,(0,0,0),pygame.Rect((20 * (x + 1)) + (136 * x),(20 * (y + 1)) + (136 * y),136,136))
                  if tileCoordinates in features:
                      screen.blit(pygame.transform.scale(building,(60,130)),((20 * (x + 1)) + (136 * x) + 35,(20 * (y + 1)) + (136 * y)))
                  if tileCoordinates in people:
                      screen.blit(pygame.transform.scale(people[people.index(tileCoordinates) + 1],(60,70)),((20 * (x + 1)) + (136 * x),(20 * (y + 1)) + (136 * y) + 40))
                  if tileCoordinates in muggersCoordinates:
                      screen.blit(pygame.transform.scale(mugger,(120,130)),((20 * (x + 1)) + (136 * x) + 10,(20 * (y + 1)) + (136 * y) + 40))
          screen.blit(pygame.transform.scale(player,(90,100)),(390,350))

          if count == 10:
              stupidAliasing = []
              for i in muggersCoordinates:
                  coor = []
                  for e in i:
                      coor.append(e)
                  stupidAliasing.append(coor)
              hint = random.choice(stupidAliasing)
              count = 0
  
          renderText(["Coordinates:","x = " + str(coordinates[0]) + "  y = " + str(coordinates[1])],[(805,20),(805,50)],28,(255,255,0),screen)
          renderText(["Muggers Remaining:",str(remaining),"Muggers Caught:",str(caught)],[(805,200),(805,220),(805,260),(805,280)],20,(255,255,0),screen)
          renderText(["Last known","mugger location:","x = " + str(hint[0]) + "  y = " + str(hint[1])],[(805,500),(805,530),(805,560)],24,(255,255,0),screen)
          
          pygame.display.flip()
  
          if remaining == 0:
              while True:
                for event in pygame.event.get():
                  if event.type == pygame.QUIT:return
                screen.fill((0,0,128))
                renderText(["No Muggers Left","Click the red 'x' on the","top right of the screen to exit","Muggers Caught: " + str(caught)],[[300,100],[225,250],[155,310],[155,460]],48,(255,255,0),screen)
                pygame.display.flip()
  
          muggersCoordinates = catch(muggersCoordinates,coordinates)
          if muggersCoordinates == "exit":return
        
  main()
  
def Chocolate_Chances():
  def renderText(inputText,inputCoordinates,inputSize,inputColor,screen):
      font = pygame.font.SysFont("comicsansms",inputSize)
      text = []
      for e in inputText:
          text.append(font.render(e,True,inputColor))
      for e in range(len(text)):
          screen.blit(text[e],inputCoordinates[e])

  def inputInstructions():
      pygame.init()
  
      while True:
          screen = pygame.display.set_mode((1000,800))
          if(pygame.QUIT in [i.type for i in pygame.event.get()]):return
          pressed = pygame.key.get_pressed()
          if pressed[pygame.K_SPACE]:return
          
          screen.fill((210,75,75))
          renderText(["Type your answer using the keyboard","in the form of a simplified fraction","Use only numbers and the '/' sign","Use backspace to delete","The numerator and the denominator of your fraction","should be separated by a '/'","For example: 1/3","Press ENTER to submit your answer","Press SPACE to return"],[[75,100],[75,140],[75,180],[75,220],[75,260],[75,300],[75,340],[75,380],[75,460]],32,(50,6,6),screen)
          pygame.display.flip()
          
  def main():
      pygame.init()
      screen = pygame.display.set_mode((1000,800))
      ticker = 0
      count = 0
      correct = 0
      chocolateNames1 = ["Napoleon","Dark","Cherry","Caramel","Milk","White","Mint","Coconut","Strawberry","Raspberry","Swiss","French","Belgium"]
      chocolateNames2 = [" Truffle: "," Chocolate: "," Créme: "," Fudge: "," Swirl: "]
      chocolateData = []
      for i in range(3):
        data = random.choice(chocolateNames1) + random.choice(chocolateNames2)
        while data in chocolateData:data = random.choice(chocolateNames1) + random.choice(chocolateNames2)
        chocolateData.extend([data,random.randint(1,30)])
      chocolate = random.choice([chocolateData[0],chocolateData[2],chocolateData[4]])
      chocolatesList = [[random.choice([(78,46,40),(19,9,2),(38,19,5),(57,28,8)]),[1050,650],random.choice(["swirl","dot"]),random.choice([(78,46,40),(19,9,2),(38,19,5),(57,28,8),(242,214,193),(255,248,220),(152,255,152),(189,0,72),(152,255,152),(189,0,72),(167,107,41)])]]
      userAnswer = ""
  
      while True:
          for event in pygame.event.get():
              if event.type == pygame.QUIT:return
              elif event.type == pygame.MOUSEBUTTONDOWN:
                loc = pygame.mouse.get_pos()
                if loc[0] > 350 and loc[0] < 650 and loc[1] > 450 and loc[1] < 510:
                  inputInstructions()
              elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) in ["0","1","2","3","4","5","6","7","8","9","/"] and len(userAnswer) < 10:userAnswer += pygame.key.name(event.key)
                elif pygame.key.name(event.key) == "backspace":
                  if userAnswer == "Try again. BACKSPACE to Clear" or userAnswer == "Correct! BACKSPACE to Clear":userAnswer = ""
                  else:userAnswer = userAnswer[:-1]
                elif pygame.key.name(event.key) == "return":
                  if userAnswer.count("/") == 1 and userAnswer[0] != "/" and userAnswer[-1] != "/":
                    if userAnswer.split("/")[1][0] != "0" and userAnswer[0] != "0":
                      if math.gcd(int(userAnswer.split("/")[0]),int(userAnswer.split("/")[1])) == 1 and int(userAnswer.split("/")[0]) / int(userAnswer.split("/")[1]) == chocolateData[chocolateData.index(chocolate) + 1] / (chocolateData[1] + chocolateData[3] + chocolateData[5]):
                        userAnswer = "Correct! BACKSPACE to Clear"
                        correct += 1
                        chocolateData = []
                        for i in range(3):
                          data = random.choice(chocolateNames1) + random.choice(chocolateNames2)
                          while data in chocolateData:data = random.choice(chocolateNames1) + random.choice(chocolateNames2)
                          chocolateData.extend([data,random.randint(1,30)])
                        chocolate = random.choice([chocolateData[0],chocolateData[2],chocolateData[4]])
                      else:userAnswer = "Try again. BACKSPACE to Clear"
                    else:userAnswer = "Try again. BACKSPACE to Clear"
                  else:userAnswer = "Try again. BACKSPACE to Clear"
  
          screen.fill((210,75,75))

          renderText(["# Correct:",str(correct)],[[30,50],[30,90]],32,(50,6,6),screen)
          renderText(["# Correct:",str(correct)],[[800,50],[800,90]],32,(50,6,6),screen)
          pygame.draw.rect(screen,(127,34,34),pygame.Rect(250,50,500,100))
          if userAnswer == "Try again. BACKSPACE to Clear" or userAnswer == "Correct! BACKSPACE to Clear":renderText([userAnswer],[[250,75]],32,(50,6,6),screen)
          else:renderText([userAnswer],[[250,50]],80,(50,6,6),screen)
          renderText(["In the chocolate box, there are: "],[[75,180]],32,(50,6,6),screen)
          for i in range(3):renderText([chocolateData[i*2] + str(chocolateData[(i*2)+1])],[[75,220 + (40*i)]],32,(50,6,6),screen)
          renderText(["What is the probability that a randomly selected chocolate","is a " + chocolate[:-2] + "?"],[[75,360],[75,400]],32,(50,6,6),screen)
          pygame.draw.rect(screen,(127,34,34),pygame.Rect(350,460,300,60))
          renderText(["Click for Input Instructions"],[[370,475]],20,(50,6,6),screen)
          pygame.draw.rect(screen,(105,105,105),pygame.Rect(0,550,1000,200))

          if ticker > 0:
            for i in range(len(chocolatesList)):
              pygame.draw.circle(screen,chocolatesList[i][0],(chocolatesList[i][1][0],chocolatesList[i][1][1]),50,0)
              if chocolatesList[i][2] == "swirl":
                pygame.draw.circle(screen,chocolatesList[i][3],(chocolatesList[i][1][0],chocolatesList[i][1][1]),30,5)
                pygame.draw.circle(screen,chocolatesList[i][3],(chocolatesList[i][1][0],chocolatesList[i][1][1]),15,5)
              else:
                pygame.draw.circle(screen,chocolatesList[i][3],(chocolatesList[i][1][0],chocolatesList[i][1][1]),20,0)
            ticker -=1
          else:
            for i in range(len(chocolatesList)):
              pygame.draw.circle(screen,chocolatesList[i][0],(chocolatesList[i][1][0],chocolatesList[i][1][1]),50,0)
              chocolatesList[i][1] = [chocolatesList[i][1][0] - 15,chocolatesList[i][1][1]]
              if chocolatesList[i][2] == "swirl":
                pygame.draw.circle(screen,chocolatesList[i][3],(chocolatesList[i][1][0],chocolatesList[i][1][1]),30,5)
                pygame.draw.circle(screen,chocolatesList[i][3],(chocolatesList[i][1][0],chocolatesList[i][1][1]),15,5)
              else:
                pygame.draw.circle(screen,chocolatesList[i][3],(chocolatesList[i][1][0],chocolatesList[i][1][1]),20,0)
              if chocolatesList[i][1][1] < -50:
                chocolatesList.remove(chocolatesList[i])
            ticker = 8
            count += 1
          if count == 10:
              chocolatesList.append([random.choice([(78,46,40),(19,9,2),(38,19,5),(57,28,8)]),[1050,650],random.choice(["swirl","dot"]),random.choice([(78,46,40),(19,9,2),(38,19,5),(57,28,8),(242,214,193),(255,248,220),(152,255,152),(189,0,72),(152,255,152),(189,0,72),(167,107,41)])])
              count = 0
  
          pygame.display.flip()

          if correct == 5:
            while True:
              for event in pygame.event.get():
                if event.type == pygame.QUIT:return
              screen.fill((210,75,75))
              renderText(["Congratulations!","You are a master of chances","and chocolates!","Click the red 'x' on the","top right of the screen to exit"],[[300,100],[180,160],[310,220],[225,310],[155,370]],48,(50,6,6),screen)
              pygame.display.flip()
              
  main()

def renderText(inputText,inputCoordinates,inputSize):
    font = pygame.font.SysFont("comicsansms",inputSize)
    text = []
    for e in inputText:
        text.append(font.render(e,True,(0,255,255)))
    for e in range(len(text)):
        screen.blit(text[e],inputCoordinates[e])
        
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            loc = pygame.mouse.get_pos()
            if loc[0] > 400 and loc[0] < 600:
                if loc[1] > 150 and loc[1] < 250:
                    
                    # Game Menu
                    homeMenu = False
                    while not homeMenu:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:homeMenu = True
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                loc = pygame.mouse.get_pos()
                                if loc[0] > 400 and loc[0] < 600:
                                    if loc[1] > 150 and loc[1] < 250:
                                        Arithmetic_Adventure()
                                    elif loc[1] > 300 and loc[1] < 400:
                                        Multiplication_Muggers()
                                    elif loc[1] > 450 and loc[1] < 550:
                                        Chocolate_Chances()
                                    elif loc[1] > 600 and loc[1] < 700:
                                        homeMenu = True
                        
                        screen.fill((0,20,40))
                        for i in range(4):pygame.draw.rect(screen,(9,0,255),pygame.Rect(400,600 - (150 * i),200,100))

                        renderText(["Select Your Game"],[(325,50)],42)
                        renderText(["Arithmetic","Adventure","Multiplication","Muggers","Chocolate","Chances","Exit"],[(410,150),(410,180),(410,300),(410,330),(410,450),(410,480),(410,600)],28)
                        renderText(["+","-","×","÷"],[(200,250),(200,500),(800,250),(800,500)],100)
                        
                        pygame.display.flip()
                                    
                elif loc[1] > 300 and loc[1] < 400:

                    # Instructions
                    homeMenu = False
                    while not homeMenu:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:homeMenu = True
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                loc = pygame.mouse.get_pos()
                                if loc[0] > 400 and loc[0] < 600:
                                    if loc[1] > 150 and loc[1] < 250:
                                        instructionsMenu = False
                                        while not instructionsMenu:
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:instructionsMenu = True
                                                pressed = pygame.key.get_pressed()
                                                if pressed[pygame.K_SPACE]:instructionsMenu = True
                                            screen.fill((0,20,40))
                                            renderText(["Arithmetic Adventure","Your goal is to find the treasure chest.","There are a total of 4 clues. The first 3 clues lead to the next clue.","The last clue leads to the treasure chest.","You are given the first clue in the beginning."],[(25,25),(25,50),(25,75),(25,100),(25,125)],22)
                                            renderText(["Use the arrow keys to navigate around the map.","Your coordinates are given on the top right corner of the screen.","Press the 'Click Here for Clue' button to view the last clue."],[(25,150),(25,175),(25,200)],22)
                                            renderText(["The game ends when you find the treasure chest.","Click on the red 'X' on the top right corner of the screen to exit the game at any time."],[(25,225),(25,250)],22)
                                            renderText(["Press SPACE to return"],[(25,300)],22)
                                            pygame.display.flip()
                                            
                                    elif loc[1] > 300 and loc[1] < 400:
                                        instructionsMenu = False
                                        while not instructionsMenu:
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:instructionsMenu = True
                                                pressed = pygame.key.get_pressed()
                                                if pressed[pygame.K_SPACE]:instructionsMenu = True
                                            screen.fill((0,20,40))
                                            renderText(["Multiplication Muggers","Your goal is to catch as many muggers as possible. There are 3 muggers."],[(25,25),(25,50)],22)
                                            renderText(["Use the arrow keys to navigate around the city. But beware! The muggers can move too!","Your coordinates are given on the top right corner of the screen.","The number of remaining and caught muggers is also given."],[(25,75),(25,100),(25,125)],22)
                                            renderText(["Every 10 steps you move, the police department provides you with a hint.","The hint is the last known coordinates of a random remaining mugger."],[(25,150),(25,175)],22)
                                            renderText(["If the tile you are on is right next to the tile where a mugger is on,","you are given the chance to capture him.","In order to capture a mugger, you must answer the given multiplication question correctly.","Feel free to use paper and pencil."],[(25,200),(25,225),(25,250),(25,275)],22)
                                            renderText(["The game ends when there are no more muggers remaining.","Click on the red 'X' at the top right corner of the screen to exit the game at any time."],[(25,300),(25,325)],22)
                                            renderText(["Press SPACE to return"],[(25,375)],22)
                                            pygame.display.flip()
                                            
                                    elif loc[1] > 450 and loc[1] < 550:
                                        instructionsMenu = False
                                        while not instructionsMenu:
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:instructionsMenu = True
                                                pressed = pygame.key.get_pressed()
                                                if pressed[pygame.K_SPACE]:instructionsMenu = True
                                            screen.fill((0,20,40))
                                            renderText(["Chocolate Chances","You are given a box of chocolates and its contents.","You must find the probability that a randomly selected chocolate","is a specific chocolate"],[(25,25),(25,50),(25,75),(25,100)],22)
                                            renderText(["Type your answer using the keyboard in the form of a simplified fraction.","Use only numbers and the '/' sign and use backspace to delete.","The numerator and the denominator of your fraction should be separated by a '/'.","Press ENTER to submit the answer you typed."],[(25,125),(25,150),(25,175),(25,200)],22)
                                            renderText(["To reference input instructions, click on the 'Click for Input Instructions' button.","If you answer correctly, the game will give you a new box of chocolates and a new question.","If you answer incorrectly, you are given another chance to try again."],[(25,225),(25,250),(25,275)],22)
                                            renderText(["The game ends when you answer 5 probability questions correctly.","Click on the red 'X' at the top right corner of the screen to exit the game at any time."],[(25,300),(25,325)],22)
                                            renderText(["Press SPACE to return"],[(25,375)],22)
                                            pygame.display.flip()
                                            
                                    elif loc[1] > 600 and loc[1] < 700:
                                        homeMenu = True
                            
                        screen.fill((0,20,40))

                        for i in range(4):pygame.draw.rect(screen,(9,0,255),pygame.Rect(400,600 - (150 * i),200,100))

                        renderText(["Select A Game to View Instructions"],[(160,50)],42)
                        renderText(["Arithmetic","Adventure","Multiplication","Muggers","Chocolate","Chances","Exit"],[(410,150),(410,180),(410,300),(410,330),(410,450),(410,480),(410,600)],28)
                        renderText(["+","-","×","÷"],[(200,250),(200,500),(800,250),(800,500)],100)
                        
                        pygame.display.flip()
                        
                elif loc[1] > 450 and loc[1] < 550:

                    # Credits
                    homeMenu = False
                    while not homeMenu:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:homeMenu = True
                            pressed = pygame.key.get_pressed()
                            if pressed[pygame.K_SPACE]:homeMenu = True
                            
                        screen.fill((0,20,40))

                        renderText(["Developers:"],[(25,25)],32)
                        renderText(["Jason Liu","Andrew Healey","Matthew Casertano"],[(25,65),(25,90),(25,115)],24)
                        renderText(["Image Credits:"],[(25,175)],32)
                        renderText(["https://gameartpartners.com/downloads/super-pixel-platformer-set/","https://www.stockunlimited.com/vector-illustration/collection-of-criminal-icons","_2009054.html","https://piq.codeus.net/picture/342440/Pine","http://pixelartmaker.com/art/67c17fc6b27ffae","http://pixelartmaker.com/art/df388a3d209c794","PixelPeople"],[(25,215),(25,240),(25,265),(25,290),(25,315),(25,340),(25,365)],24)
                        renderText(["Special thanks to our testers and families!"],[(25,425)],32)
                        renderText(["Press SPACE to return"],[(25,500)],32)

                        pygame.display.flip()
                        
                elif loc[1] > 600 and loc[1] < 700:done = True

    screen.fill((0,20,40))
    for i in range(4):pygame.draw.rect(screen,(9,0,255),pygame.Rect(400,600 - (150 * i),200,100))

    renderText(["FunMath"],[(345,25)],75)
    renderText(["Play","Instructions","Credits","Exit"],[(410,150),(410,300),(410,450),(410,600)],28)
    renderText(["+","-","×","÷"],[(200,250),(200,500),(800,250),(800,500)],100)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
