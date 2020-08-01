import pygame, os, sys, random

width = 800
height = 600
buttonWidth = 360
buttonHeight = 80
gameBackgroundColour = [36, 36, 36]
menuBackgroundColour = [41, 22, 59]
textColour = [255, 255, 255]
menuButtonColour = [76, 34, 117]
selectedMenuButtonColour = [113, 52, 173]
sidebarColour = [18, 18, 18]
stopSurfaceColour = [0, 0, 0]
fruitColour = [196, 115, 0]
wallColour = [0, 0, 0]
speed = 10

musicOnText = "Music ON"
musicOffText = "Music OFF"
sfxOnText = "SFX ON"
sfxOffText = "SFX OFF"

highscore = 0
try:
	highscoreFile = open(os.path.join(sys.path[0], "highscore.dat"), "r")
	highscore = int(highscoreFile.read())
	highscoreFile.close()
except IOError:
	print("Error reading file highscore.dat")
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
pygame.display.set_caption("Snake by Jamesscn")
screen = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
titleFont = pygame.font.Font(None, 48)
midFont = pygame.font.Font(None, 28)
beep = pygame.mixer.Sound(os.path.join(sys.path[0], "sfx.wav"))
menuOptions = [
	"One player",
	"Two players",
	musicOnText,
	sfxOnText
]
selectedMenuOption = 0
music = True
sfx = True
running = True
gameOver = False
paused = False
menuSelecting = False
gameState = 0
xTiles = 60
yTiles = 60
pieceWidth = 10
pieceHeight = 10
sidebarWidth = width - xTiles * pieceWidth
score = 0
snakes = []
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if gameState == 1:
				for snake in snakes:
					if event.key == snake["keys"][0]:
						if (snake["prevDirection"] != 2 or len(snake["snake"]) == 1) and not paused:
							snake["direction"] = 0
					if event.key == snake["keys"][1]:
						if (snake["prevDirection"] != 3 or len(snake["snake"]) == 1) and not paused:
							snake["direction"] = 1
					if event.key == snake["keys"][2]:
						if (snake["prevDirection"] != 0 or len(snake["snake"]) == 1) and not paused:
							snake["direction"] = 2
					if event.key == snake["keys"][3]:
						if (snake["prevDirection"] != 1 or len(snake["snake"]) == 1) and not paused:
							snake["direction"] = 3
				if gameOver:
					gameOver = False
					gameState = 0
					continue
			if event.key == pygame.K_UP:
				if gameState == 0:
					selectedMenuOption = max(selectedMenuOption - 1, 0)
			if event.key == pygame.K_DOWN:
				if gameState == 0:
					selectedMenuOption = min(selectedMenuOption + 1, len(menuOptions) - 1)
			if event.key == pygame.K_RETURN:
				if gameState == 0:
					menuSelecting = True
			if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
				if gameState == 1 and not gameOver:
					paused = not paused
					if paused:
						pygame.mixer.music.pause()
					else:
						pygame.mixer.music.unpause()
		if event.type == pygame.MOUSEMOTION:
			if gameState == 0:
				mousePos = pygame.mouse.get_pos()
				for i in range(len(menuOptions)):
					centerX = width // 2
					centerY = height // (len(menuOptions) + 2) * (i + 2)
					dx = abs(mousePos[0] - centerX)
					dy = abs(mousePos[1] - centerY)
					if dx <= buttonWidth // 2 and dy <= buttonHeight // 2:
						selectedMenuOption = i
		if event.type == pygame.MOUSEBUTTONDOWN:
			if gameState == 0:
				mousePos = pygame.mouse.get_pos()
				for i in range(len(menuOptions)):
					centerX = width // 2
					centerY = height // (len(menuOptions) + 2) * (i + 2)
					dx = abs(mousePos[0] - centerX)
					dy = abs(mousePos[1] - centerY)
					if dx <= buttonWidth // 2 and dy <= buttonHeight // 2:
						selectedMenuOption = i
						menuSelecting = True
			if gameState == 1:
				if gameOver:
					gameOver = False
					gameState = 0

	clock.tick(speed)

	if menuSelecting:
		menuSelecting = False
		if selectedMenuOption == 0:
			gameState = 1
			snakes = [
				{
					"snake": [[xTiles // 2, yTiles // 2]],
					"prevDirection": 0,
					"direction": 0,
					"keys": [pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a],
					"score": 0,
					"snakeColour": [60, 168, 50],
					"snakeAltColour": [88, 130, 30],
					"snakeHeadColour": [255, 255, 255],
					"name": "Green Snake"
				}
			]
			fruit = [random.randint(1, xTiles - 2), random.randint(1, yTiles - 2)]
			if fruit == snakes[0]["snake"][0]:
				fruit = [snakes[0]["snake"][0][0] + 1, snakes[0]["snake"][0][1] + 1]
			if music:
				pygame.mixer.music.load(os.path.join(sys.path[0], "music.mp3"))
				pygame.mixer.music.play(-1)
		if selectedMenuOption == 1:
			gameState = 1
			snakes = [
				{
					"snake": [[xTiles // 3, yTiles // 2]],
					"prevDirection": 0,
					"direction": 0,
					"keys": [pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a],
					"score": 0,
					"snakeColour": [60, 168, 50],
					"snakeAltColour": [88, 130, 30],
					"snakeHeadColour": [255, 255, 255],
					"name": "Green Snake"
				},
				{
					"snake": [[xTiles * 2 // 3, yTiles // 2 - 1]],
					"prevDirection": 2,
					"direction": 2,
					"keys": [pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT],
					"score": 0,
					"snakeColour": [110, 15, 0],
					"snakeAltColour": [153, 77, 29],
					"snakeHeadColour": [255, 255, 255],
					"name": "Red Snake"
				}
			]
			fruit = [random.randint(1, xTiles - 2), random.randint(1, yTiles - 2)]
			if fruit == snakes[0]["snake"][0] or fruit == snakes[1]["snake"][0]:
				fruit = [snakes[0]["snake"][0][0] + 1, snakes[0]["snake"][0][1] + 1]
			if music:
				pygame.mixer.music.load(os.path.join(sys.path[0], "music.mp3"))
				pygame.mixer.music.play(-1)
		if selectedMenuOption == 2:
			music = not music
		if selectedMenuOption == 3:
			sfx = not sfx

	if music:
		menuOptions[2] = musicOnText
	else:
		menuOptions[2] = musicOffText
	if sfx:
		menuOptions[3] = sfxOnText
	else:
		menuOptions[3] = sfxOffText

	if gameState == 0:
		screen.fill(menuBackgroundColour)
		titleRender = titleFont.render("Snake", 1, textColour)
		subtitleRender = font.render("By Jamesscn", 1, textColour)
		screen.blit(titleRender, titleRender.get_rect(center = [width // 2, height // (len(menuOptions) + 2) - 15]))
		screen.blit(subtitleRender, subtitleRender.get_rect(center = [width // 2, height // (len(menuOptions) + 2) + 15]))
		for i in range(len(menuOptions)):
			buttonColour = menuButtonColour
			if i == selectedMenuOption:
				buttonColour = selectedMenuButtonColour
			textRender = midFont.render(menuOptions[i], 1, textColour)
			centerX = width // 2
			centerY = height // (len(menuOptions) + 2) * (i + 2)
			pygame.draw.rect(screen, buttonColour, pygame.Rect(centerX - buttonWidth // 2, centerY - buttonHeight // 2, buttonWidth, buttonHeight))
			screen.blit(textRender, textRender.get_rect(center = [centerX, centerY]))
	elif gameState == 1:
		screen.fill(sidebarColour)
		snakeIndex = 0
		highestScore = 0
		for snake in snakes:
			if not gameOver and not paused:
				lastSnakeIndex = len(snake["snake"]) - 1
				newPiece = [snake["snake"][lastSnakeIndex][0], snake["snake"][lastSnakeIndex][1]]
				if snake["direction"] == 0:
					newPiece[1] -= 1
				elif snake["direction"] == 1:
					newPiece[0] += 1
				elif snake["direction"] == 2:
					newPiece[1] += 1
				else:
					newPiece[0] -= 1
				snake["prevDirection"] = snake["direction"]
				if newPiece == fruit:
					if sfx:
						beep.play()
					snake["score"] += 1
					fruitPlacementCandidates = []
					for x in range(1, xTiles - 1):
						for y in range(1, yTiles - 1):
							inSnake = False
							for testSnake in snakes:
								if [x, y] in testSnake["snake"]:
									inSnake = True
							if inSnake:
								continue
							fruitPlacementCandidates.append([x, y])
					random.shuffle(fruitPlacementCandidates)
					if len(fruitPlacementCandidates) == 0:
						gameOver = True
						pygame.mixer.music.fadeout(2000)
					else:
						fruit = fruitPlacementCandidates[0]
				else:
					snake["snake"].pop(0)

				if newPiece[0] <= 0 or newPiece[0] >= xTiles - 1 or newPiece[1] <= 0 or newPiece[1] >= yTiles - 1:
					gameOver = True
					pygame.mixer.music.fadeout(2000)

				for testSnake in snakes:
					if newPiece in testSnake["snake"]:
						gameOver = True
						pygame.mixer.music.fadeout(2000)

				snake["snake"].append(newPiece)
			
			highestScore = max(highestScore, snake["score"])
			nameRender = midFont.render(snake["name"], 1, textColour)
			scoreTitleRender = font.render("Score:", 1, textColour)
			scoreRender = font.render(str(snake["score"]), 1, textColour)
			screen.blit(nameRender, nameRender.get_rect(center = [pieceWidth * xTiles + sidebarWidth // 2, 40 + 100 * snakeIndex]))
			screen.blit(scoreTitleRender, scoreTitleRender.get_rect(center = [pieceWidth * xTiles + sidebarWidth // 2, 70 + 100 * snakeIndex]))
			screen.blit(scoreRender, scoreRender.get_rect(center = [pieceWidth * xTiles + sidebarWidth // 2, 90 + 100 * snakeIndex]))
			snakeIndex += 1

		highscoreTitleRender = font.render("Highscore:", 1, textColour)
		highscoreRender = font.render(str(max(highestScore, highscore)), 1, textColour)
		screen.blit(highscoreTitleRender, highscoreTitleRender.get_rect(center = [pieceWidth * xTiles + sidebarWidth // 2, 40 + 100 * snakeIndex]))
		screen.blit(highscoreRender, highscoreRender.get_rect(center = [pieceWidth * xTiles + sidebarWidth // 2, 60 + 100 * snakeIndex]))

		pygame.draw.rect(screen, gameBackgroundColour, pygame.Rect(0, 0, pieceWidth * xTiles, pieceHeight * yTiles))
		pygame.draw.rect(screen, wallColour, pygame.Rect(0, 0, pieceWidth, pieceHeight * yTiles))
		pygame.draw.rect(screen, wallColour, pygame.Rect(pieceWidth * xTiles - pieceWidth, 0, pieceWidth, pieceHeight * yTiles))
		pygame.draw.rect(screen, wallColour, pygame.Rect(0, 0, pieceWidth * xTiles, pieceHeight))
		pygame.draw.rect(screen, wallColour, pygame.Rect(0, pieceWidth * xTiles - pieceHeight, pieceWidth * xTiles, pieceHeight))
		pygame.draw.rect(screen, fruitColour, pygame.Rect(fruit[0] * pieceWidth, fruit[1] * pieceHeight, pieceWidth, pieceHeight))

		for snake in snakes:
			for i in range(len(snake["snake"])):
				lastSnakeIndex = len(snake["snake"]) - 1
				pieceColour = snake["snakeColour"]
				if i == lastSnakeIndex:
					pieceColour = snake["snakeHeadColour"]
				elif i % 2 == 0:
					pieceColour = snake["snakeAltColour"]
				pygame.draw.rect(screen, pieceColour, pygame.Rect(snake["snake"][i][0] * pieceWidth, snake["snake"][i][1] * pieceHeight, pieceWidth, pieceHeight))

		stopSurface = pygame.Surface([pieceWidth * xTiles, pieceHeight * yTiles])
		stopSurface.set_alpha(128)
		stopSurface.fill(stopSurfaceColour)
		if paused:
			screen.blit(stopSurface, [0, 0])
			pausedRender = titleFont.render("Paused", 1, textColour)
			unpauseRender = font.render("Press P or ESC to unpause", 1, textColour)
			screen.blit(pausedRender, pausedRender.get_rect(center = [pieceWidth * xTiles // 2, pieceHeight * yTiles // 2 - 20]))
			screen.blit(unpauseRender, unpauseRender.get_rect(center = [pieceWidth * xTiles // 2, pieceHeight * yTiles // 2 + 20]))
		if gameOver:
			if highscore < highestScore:
				highscore = highestScore
				try:
					highscoreFile = open(os.path.join(sys.path[0], "highscore.dat"), "w")
					highscoreFile.write(str(highscore))
					highscoreFile.close()
				except IOError:
					print("Error writing file highscore.dat")
			screen.blit(stopSurface, [0, 0])
			gameOverRender = titleFont.render("Game Over", 1, textColour)
			replayRender = font.render("Press any key to continue", 1, textColour)
			screen.blit(gameOverRender, gameOverRender.get_rect(center = [pieceWidth * xTiles // 2, pieceHeight * yTiles // 2 - 20]))
			screen.blit(replayRender, replayRender.get_rect(center = [pieceWidth * xTiles // 2, pieceHeight * yTiles // 2 + 20]))
	pygame.display.flip()

pygame.quit()