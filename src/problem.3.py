import threading
import math


def main(url,batchsize):
    file = open(url,'r')
    numberOfPhotos = int(file.readline().rstrip())
    totalSlideShow =[]
    batch = batchsize #number of photos to process at a time

    for k in range(0 , math.ceil(numberOfPhotos / batch)):
        # print progress
        print(url + ":" + str((k)/(math.ceil(numberOfPhotos / batch)) * 100 % 100) + "%")
        slideshow = [] #list of slides created per batch
        verticalPhotos = [] #list of slides created from vertical photos combined  
        if k == math.ceil(numberOfPhotos / batch) - 1 :
            numberOfPhotosToRead = numberOfPhotos
        else:
            numberOfPhotosToRead = (k + 1) * batch
        for i in range(k * batch, numberOfPhotosToRead):
            temp = file.readline().rstrip().split(" ")
            currentPhoto = [temp[2:],i]
            if temp[0] == 'H':
                matchPhoto(slideshow,currentPhoto)
            else:
                matchPhoto(verticalPhotos,currentPhoto)

        #merges the list of slides from vertical photos into the list of slides from horizontal photos
        verticalSlideShow = createVerticalSlide(verticalPhotos)
        for currentPhoto in verticalSlideShow:
            matchPhoto(slideshow,currentPhoto)
        #concatenate result from batch
        totalSlideShow += slideshow


    file.close()
    #creates output file
    outputFile = open(str(batchsize) + "-" + "output-"+url , 'w')
    outputFile.write(str(len(totalSlideShow))+"\n")
    for slide in totalSlideShow:
        outputFile.write(str(slide[1])+"\n")
    outputFile.close()

# removes non-unique items
def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

# returns the score between 2 slides
def computeScore(p1,p2):
    intersection = set(p1[0]).intersection(p2[0])
    A = diff(p1[0],p2[0])
    B = diff(p2[0],p1[0])
    return min(len(intersection), len(A),len(B))

#matches slides based on the score
def matchPhoto(slideShow,photo):
    score = 0
    index = 0
    for i in range(len(slideShow)):
        tempScore = computeScore(slideShow[i],photo)
        if tempScore > score:
            index = i
            score = tempScore
    slideShow.insert(index + 1, photo)

#creates slides from vertical photos
def createVerticalSlide(listOfVerticalPhotos):
    listOfVerticalSlides = []
    i = 0
    while i + 1 < len(listOfVerticalPhotos):
        concatPhoto = list(set(listOfVerticalPhotos[i][0] + (listOfVerticalPhotos[i+1][0])))
        listOfVerticalSlides.append([concatPhoto,str(listOfVerticalPhotos[i][1]) + " " + str(listOfVerticalPhotos[i+1][1])])
        i += 2
    return listOfVerticalSlides


urlList = ["a_example.txt","b_lovely_landscapes.txt","c_memorable_moments.txt","d_pet_pictures.txt","e_shiny_selfies.txt"]
batchSizeList = [100,1000,5000,10000,40000,90000]
threads = []

# thread that starts the main function
def worker(url,batchSize):
    print("started" + " " + url)
    main(url,batchSize)
    print("finished" + " " + url)
    return

def computeProblem():
#parallel computing of multiple inputs
    for url in urlList:
        for size in batchSizeList:
            t = threading.Thread(target=worker, args=(url,size,))
            threads.append(t)
            t.start()


computeProblem()