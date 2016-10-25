'''
Created on 24 Oct 2016

northwest = 0
northeast = 1
southwest = 2
southeast = 3
'''

from __builtin__ import False

class quadTree2D(object):

    def __init__(self, centrePt, halfXDim, halfYDim, maxPts, levelID):
        self.maxPts = maxPts
        self.children = []
        self.centrePt = centrePt
        self.halfXDim = halfXDim
        self.halfYDim = halfYDim
        self.points = []
        self.subDivided = False
        self.levelID = levelID
        #print self.levelID, self.centrePt
     
    def subdivide(self):
        '''Build & populate children
        '''
        childACentre = [self.centrePt[0]-(0.5*self.halfXDim), self.centrePt[1]+(0.5*self.halfYDim)]
        childA = quadTree2D(childACentre, self.halfXDim/2.0, self.halfYDim/2.0, self.maxPts, self.levelID+1)
        
        childBCentre = [self.centrePt[0]+(0.5*self.halfXDim), self.centrePt[1]+(0.5*self.halfYDim)]
        childB = quadTree2D(childBCentre, self.halfXDim/2.0, self.halfYDim/2.0, self.maxPts, self.levelID+1)
        
        childCCentre = [self.centrePt[0]-(0.5*self.halfXDim), self.centrePt[1]-(0.5*self.halfYDim)]
        childC = quadTree2D(childCCentre, self.halfXDim/2.0, self.halfYDim/2.0, self.maxPts, self.levelID+1)
        
        childDCentre = [self.centrePt[0]+(0.5*self.halfXDim), self.centrePt[1]-(0.5*self.halfYDim)]
        childD = quadTree2D(childDCentre, self.halfXDim/2.0, self.halfYDim/2.0, self.maxPts, self.levelID+1)
        
        self.children = [childA, childB, childC, childD]
        self.subDivided = True
        
        #Populate children
        cnt = 0
        for pt in self.points:
            for child in self.children:
                chk = child.insertPt(pt)
                if chk == True:
                    cnt+=1
                    break
        if cnt == len(self.points):
            pass
            #All successfully in
        else:
            print 'Sub div failed'
        self.points = []
        
        
    def insertPt(self, pt):
        '''
        Try to insert a point into this quad
        Only if its within bounds
        '''
        if self.chkBounds(pt) == False:
            #print pt, self.levelID, self.centrePt
            return False
        if self.subDivided == True:
            for child in self.children:
                chk = child.insertPt(pt)
                if chk == True:
                    return True
        else:  
            self.points.append(pt)
            if len(self.points) > self.maxPts:
                self.subdivide()
                return True
            return True
        return False
        
        
    def chkBounds(self, pt): 
        '''
        Check a point lies within the bounds of this quad
        '''  
        if pt[0]<=self.centrePt[0]+self.halfXDim and pt[0]>=self.centrePt[0]-self.halfXDim:
            if pt[1]<=self.centrePt[1]+self.halfYDim and pt[1]>=self.centrePt[1]-self.halfYDim:
                return True
        return False
    
    def getPointsAtQuad(self, pt):
        '''
        Drill down through the tree - recover the points at the leaf of given point
        '''
        if self.chkBounds(pt) == False:
            print 'Pt not in tree bounds'
            return 0
        if self.subDivided == False:
            return self.points
        for child in self.children:
            if child.chkBounds(pt) == True:
                outPts = child.getPointsAtQuad(pt)
        return outPts
    
    
    def getDepth(self, maxLevelID):
        '''
        Return the depth of the tree
        Pass 0 in to instantiate at tree top
        '''
        if self.levelID > maxLevelID:
            maxLevelID = self.levelID
        for child in self.children:
            maxLevelID = child.getDepth(maxLevelID)
        return maxLevelID
    
    
    def getTotalPts(self):
        '''
        Count total number of points stored in tree
        '''
        cnt = 0
        if self.subDivided == False:
            return len(self.points)
        for child in self.children:
            cnt+=child.getTotalPts()
        return cnt

    def dumpAllPoints(self):
        '''
        Clean the tree of all points
        '''
        for child in self.children:
            child.points = []
            del child
        self.points = []   
    

    
    
        