'''
Created on 25 Oct 2016

'''

from random import random, randint
from QuadTree import quadTree2D

def genTestData(xDim, yDim, numPts):
    '''
    Generate some test data to insert to the tree
    '''
    points = []
    for i in range(0, numPts):
        points.append([random()+randint(0,xDim), random()+randint(0,yDim)])
    return points


def initTestQuadTree(xDim, yDim, numPts, maxPtsPerQuad):
    centrePt = [float(xDim/2.0), float(yDim/2.0)]
    #Init the blank tree
    quadT = quadTree2D(centrePt, float(xDim)/2.0, float(yDim)/2.0, maxPtsPerQuad, 0)
    return quadT


def main():
    xDim = 10.0
    yDim = 10.0
    numPts = 1000
    maxPtsPerQuad = 10
    quadT = initTestQuadTree(xDim, yDim, numPts, maxPtsPerQuad)
    #Populate
    tstData = genTestData(xDim, yDim, numPts)
    print 'test data len', len(tstData)
    cnt = 0
    for pt in tstData:
        chk = quadT.insertPt(pt)
        if chk == True:
            cnt+=1
    print 'successfully inserted', cnt
    print 'depth', quadT.getDepth(0)
    
    #Get some points at a leaf
    tstPt = [random()+randint(0,xDim), random()+randint(0,yDim)]
    print 'tstPt', tstPt
    print 'get quad pts', quadT.getPointsAtQuad(tstPt)
    print 'Total points in tree', quadT.getTotalPts()
    
        
if __name__ == '__main__':
    main()   