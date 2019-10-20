import threading

def main(url):
    file = open(url,'r')
    numberOfPhotos = int(file.readline().rstrip())
    slideshow = []
    verticalPhotos = []
    for i in range(numberOfPhotos):
        print(url + ":" + str((i+1)/numberOfPhotos * 100 % 100) + "%")
        temp = file.readline().rstrip().split(" ")
        currentPhoto = [temp[0],int(temp[1]),sorted(temp[2:]),i]
        if currentPhoto[0] == 'H':
            matchPhoto(slideshow,currentPhoto)
        else:
            matchPhoto(verticalPhotos,currentPhoto)

    verticalSlideShow = createVerticalSlide(verticalPhotos)
    for i in range(len(verticalSlideShow)):
        print(url + ":" + str((i+1)/numberOfPhotos * 100 % 100) + "%")
        matchPhoto(slideshow,verticalSlideShow[i])
    # print(slideshow)

    outputFile = open("output-"+url , 'w')
    outputFile.write(str(len(slideshow))+"\n")
    for slide in slideshow:
        outputFile.write(str(slide[3])+"\n")
    file.close()

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

def computeScore(p1,p2):
    intersection = set(p1[2]).intersection(p2[2])
    A = diff(p1[2],p2[2])
    B = diff(p2[2],p1[2])
    return min(len(intersection), len(A),len(B))

def matchPhoto(slideShow,photo):
    score = 0
    index = 0
    for i in range(len(slideShow)):
        tempScore = computeScore(slideShow[i],photo)
        if tempScore > score:
            index = i
            score = tempScore
    slideShow.insert(index + 1, photo)

def createVerticalSlide(listOfVerticalPhotos):
    listOfVerticalSlides = []
    # print(listOfVerticalPhotos)

    i = 0
    while i < len(listOfVerticalPhotos):
        # print(i)
        concatPhoto = list(set(listOfVerticalPhotos[i][2] + (listOfVerticalPhotos[i+1][2])))
        listOfVerticalSlides.append(['V',len(concatPhoto),concatPhoto,str(listOfVerticalPhotos[i][3]) + " " + str(listOfVerticalPhotos[i+1][3])])
        i += 2
    return listOfVerticalSlides



urlList = ["a_example.txt","b_lovely_landscapes.txt","c_memorable_moments.txt","d_pet_pictures.txt","e_shiny_selfies.txt"]

threads = []

def worker(url):
    print("started" + " " + url)
    main(url)
    print("finished" + " " + url)
    return


for i in range(2):
    t = threading.Thread(target=worker, args=(urlList[i],))
    threads.append(t)
    t.start()


