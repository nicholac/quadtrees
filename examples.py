'''
Created on 25 Oct 2016

'''

from random import random, randint
from QuadTree import quadTree2D
import time, math

def genTestData(xDim, yDim, numPts):
    '''
    Generate some test data to insert to the tree
    '''
    points = []
    for i in range(0, numPts):
        points.append([random()+randint(0,xDim), random()+randint(0,yDim)])
    return points


def initTestQuadTree(xDim, yDim, maxPtsPerQuad):
    centrePt = [float(xDim/2.0), float(yDim/2.0)]
    #Init the blank tree
    quadT = quadTree2D(centrePt, float(xDim)/2.0, float(yDim)/2.0, maxPtsPerQuad, 0)
    return quadT


def initInsertBasic():
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
    print 'get quad pts', quadT.getPtsByPt(tstPt)
    print 'Total points in tree', quadT.getTotalPts()
    del quadT


def testDistanceCalcs():
    '''
    Test the speed of distance reduction
    '''
    xDim = 10.0
    yDim = 10.0
    #elevs * timestep integrations
    outerDim = 1600000
    #Launch positions
    innerDim = 1000
    maxPtsPerQuad = 100
    quadT = initTestQuadTree(xDim, yDim, maxPtsPerQuad)
    #Populate
    tstData = genTestData(xDim, yDim, outerDim)
    tstData.append([1.557, 8.556])
    tstPt = [1.556, 8.55]
    closePt = []
    #Quad tree populate
    print 'Populating quadtree'
    cnt=0
    for i in range(0, outerDim):
        chk = quadT.insertPt(tstData[i])
        if chk == True:
            cnt+=1
    quadT.insertPt([1.557, 8.556])
    print 'successfully inserted', cnt
    print 'depth', quadT.getDepth(0)
    #Beginning Tests
    t0 = time.time()
    closestDist = 99999.0
    closestIdx = 0
    print 'Brute Forcing: ', outerDim*innerDim
    '''
    for i in range(0, outerDim):
        for ii in range(0, innerDim):
            dist = math.sqrt(math.pow((tstPt[0]-tstData[ii][0]), 2.0)+math.pow((tstPt[1]-tstData[ii][1]), 2.0))
            if dist < closestDist:
                closestDist = dist
                closePt = tstData[ii]
    '''
    t1 = time.time()
    total = t1-t0
    print 'brute force results (time, dist, tstpt, closePt): ', '825', closestDist, tstPt, closePt
    #print 'brute time: ', total, ' secs'

    
    t0 = time.time()
    for i in range(0, innerDim):
        closePts = quadT.getPtsByDistance(tstPt, 0.01)
        closestDist = 99999.0
        closestIdx = 0
        for i in closePts:
            dist = math.sqrt(math.pow((tstPt[0]-i[0]), 2.0)+math.pow((tstPt[1]-i[1]), 2.0))
            if dist < closestDist:
                closestDist = dist
                closePt = i
    t1 = time.time()
    total = t1-t0
    print 'quadT (time, closestPts): ', total, closePt
    del quadT
    
    
    
    
        
if __name__ == '__main__':
    testDistanceCalcs()   