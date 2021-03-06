from numpy import *
import operator 
import matplotlib
import matplotlib.pyplot as plt
from os import listdir
def creatDataset():
    group =array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels

def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = zeros((numberOfLines,3))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index = index + 1
    return returnMat,classLabelVector


def classify0(inX,dataSet,labels,k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX,(dataSetSize,1))-dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicis=distances.argsort()
    classCount ={}# init a dict
    for i in range(k):
        voteIlabel = labels[sortedDistIndicis[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0)+1
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals,(m,1))
    normDataSet = normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals



def datingClassTest():
    hoRatio = 0.10
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0



    for i in list(range(numTestVecs)):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],5)
        print("the classifier came back with:%d,the real answer is:%d" % (classifierResult,datingLabels[i]))
        if(classifierResult != datingLabels[i]) : errorCount += 1.0
    print("the total error rate is:%f" % (errorCount/float(numTestVecs)))
    print("numTestVecs=%d" % numTestVecs)

def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        linestr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(linestr[j])
    return returnVect

def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')
    m=len(trainingFileList)
    trainingMat=zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        filestr = fileNameStr.split('.')[0]
        classNumStr = int(fileNameStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
    testFileList = listdir('testDigits')
    errorCount = 0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        filestr = fileNameStr.split('.')[0]
        classNumStr = int(filestr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s'% fileNameStr)
        classifierResult = classify0(vectorUnderTest,trainingMat,hwLabels,3)
        print ("the classfier came back with: %d, the real answer is :%d" % (classifierResult,classNumStr))
        if(classifierResult!=classNumStr) : errorCount += 1.0
    print("\nthe total number of errors is %d" % errorCount)
    print("\nthe total error rate is : %f "% (errorCount/float(mTest)))


def main():
    #sit test code
    #group,labels=creatDataset()
    #print(group,labels)

    #print(classify0([0.3,0.3],group,labels,3))

    #datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')

    #normMat,ranges,minVals = autoNorm(datingDataMat)

    #print(normMat)

    #print(datingDataMat)

    #fig = plt.figure()
    #ax = fig.add_subplot(121)
    #ax.scatter(datingDataMat[:,1],datingDataMat[:,2],15.0*array(datingLabels),15.0*array(datingLabels))
    #plt.show()
    #ax = fig.add_subplot(122)
    #ax.scatter(datingDataMat[:,2],datingDataMat[:,0],15.0*array(datingLabels),15.0*array(datingLabels))
    #plt.show()

    #datingClassTest()

    #testVector=img2vector('testDigits/0_13.txt')
    #print(testVector[0,0:31])

    handwritingClassTest()



if __name__ == '__main__':
     main() 