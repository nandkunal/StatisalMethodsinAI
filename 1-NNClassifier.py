import random as rnd
import math
import operator
import matplotlib.pyplot as plt

def loadDataFile(filename,training,test):
   f = open(filename,'r');
   for line in f:
    if not line.isspace():
       data=list(line.strip().split(","))
       if rnd.random()<=0.66:
        training.append(data)
       else:
        test.append(data)



def euclideanDistance(data1, data2, length):
	distance = 0
	for x in range(length):
		distance += pow(float(data1[x]) - float(data2[x]), 2)
	return math.sqrt(distance)


def getNeighbors(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance)-2
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))

	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def getAccurancy(trainingsataset,testdataset):
    count=0
    for data in testdataset:
        neighbour=getNeighbors(trainingsataset,data,1)


        if neighbour[0][-1] == data[-1]:#Since 1-NN so only one element will be in neighbour list
            count=count+1

    accuracy=count/float(len(testdataset))
    return accuracy*100

def calculateMean(data):
    sum=0
    for num in data:
        sum+=num
    average=sum/float(len(data))
    return average
def calculateStandarDeviation(data,mean):
    sum=0
    for num in data:
        sum+=math.pow((num-mean),2)

    varience=sum/float(len(data))
    return math.sqrt(varience)

def populateConfusionMatrix(training,testdata,classifiers):
    prediction=list()
    actualdict=dict()
    predictiondict=dict()
    falsepredlist=list();
    for clss in classifiers:
       actualdict.update({clss:0})

    for data in testdata:
        neighbour=getNeighbors(training,data,1)
        actualdict.update({data[-1]:actualdict.get(data[-1])+1})
        prediction.append((data[-1],neighbour[0][-1]))
   # print actualdict
    #print prediction
    for labels in classifiers:
        predictiondict.update({labels:0})
    for val in prediction:
        if(val[0]==val[1]):
            predictiondict.update({val[0]:predictiondict.get(val[0])+1})
        else:
            falsepredlist.append(val)

    print "Prediction ",predictiondict
    drawMatrix(classifiers,predictiondict,actualdict,falsepredlist)
def getMatrixIndexForFalsePrediction(confusionmatrix,falselist):
    #print " FalseList",falselist[0],falselist[1]
    index=list()
    xindex=0
    yindex=1
    for x in confusionmatrix[0]:
      if x==falselist[0]:
          index.append(xindex)
      xindex+=1
    for y in range(1,len(confusionmatrix[0])):
        if confusionmatrix[y][0]==falselist[1]:
            index.append(yindex)
        yindex+=1
    return index
def drawMatrix(classifiers,predict,actualdict,falsepredlist):

    classifiers.insert(0,'')
    confusion_matrix=[classifiers]

    for cls in classifiers:
        if cls:
         confusion_matrix.append([cls])
    for i in range(1,len(classifiers)):
        for j in range(1,len(classifiers)):
         confusion_matrix[i].append(0)




    #print confusion_matrix
    for i in range(1,len(classifiers)):
      confusion_matrix[i][i]=predict.get(confusion_matrix[i][0])
    print "Flase PredList ",falsepredlist
    for values in falsepredlist:
      falseindex=getMatrixIndexForFalsePrediction(confusion_matrix,values)
      #print "False Index",falseindex
      confusion_matrix[falseindex[0]][falseindex[1]]=confusion_matrix[falseindex[0]][falseindex[1]]+1
    print "Confusion Matrix "
    for rows in confusion_matrix:
        print rows




def plotGraph(datalist):
    plt.plot(datalist)
    plt.show()



accuracyList=list()

for i in range(9):
 filename="iris.data"
 classNamesList=['Iris-setosa','Iris-versicolor','Iris-virginica']
 training=list()
 test=list()
 loadDataFile(filename,training,test)
 accuracy=(getAccurancy(training,test))
 accuracyList.append(accuracy)
 print "Accuracy ",accuracy
 populateConfusionMatrix(training,test,classNamesList)

mean=calculateMean(accuracyList)
print "Mean ",mean

standard_deviation=calculateStandarDeviation(accuracyList,mean)

print "Standard Deviation ",standard_deviation

coordinateMap=dict()
for elem in training:
    key =  elem[4];
    if coordinateMap.has_key(key):
        lst=coordinateMap.get(key)
        lst.append((elem[1],elem[3]))
        coordinateMap.update({key:lst})
    else:
        lst=list()
        lst.append((elem[1],elem[3]))
        coordinateMap.update({key:lst});

print coordinateMap
#plotGraph(coordinatelist)


