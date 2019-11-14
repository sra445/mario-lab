platform = "platform,{0},{1},200,50,platform.png\n"
mario = "mario,{0},{1},35,0,mario.png,100,70,11\n"
gomba = "gomba,{0},{1},35,0,gomba.png,70,70,5,{2},{3}\n"
ground = "ground,0,{0}\n"

inputFile = open("level1Sketch.csv", "r")
outputFile = open("level1.csv", "w")

y = 0
for line in inputFile:
    line = line.strip().split(",")
    x = 0
    for px in line:
        if px == "platform":
            outputFile.write(platform.format(x,y))
        elif px == "mario":
            outputFile.write(mario.format(x,y))
        elif "gomba" in px:
            tmp = px.split(";")
            outputFile.write(gomba.format(x,y, x - int(tmp[1]), x+int(tmp[2])))
        elif px == "ground":
            outputFile.write(ground.format(y))
        x+=5
    y+=5

inputFile.close()
outputFile.close()