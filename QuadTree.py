'''
Created on 24 Oct 2016

northwest = 0
northeast = 1
southwest = 2
southeast = 3

'''

from __builtin__ import False

class quadTree2D(object):

    def __init__(self, centrePt, halfXDim, halfYDim, maxPts, levelID=0):
        '''
        ::param centrePt [float x, float y] for this Quad (pass total area centre point on tree init)
        ::param halfXDim float half X dimension of quad (pass half total X dim on tree init)
        ::param halfYDim float half Y dimension of quad (pass half total Y dim on tree init)
        ::param maxPts int Maximum number of points per quad before split (controls depth)
        ::param leveID tree depth at this level (pass 0 on tree init)
        '''
        self.maxPts = maxPts
        self.children = []
        self.centrePt = centrePt
        self.halfXDim = halfXDim
        self.halfYDim = halfYDim
        self.points = []
        self.subDivided = False
        self.levelID = levelID
        self.quadID = [0]
     
    def subdivide(self):
        '''Build & populate children
        '''
        childACentre = [self.centrePt[0]-(0.5*self.halfXDim), self.centrePt[1]+(0.5*self.halfYDim)]
        childA = quadTree2D(childACentre, self.halfXDim/2.0, self.halfYDim/2.0, self.maxPts, self.levelID+1)
        childA.quadID = self.quadID[:]
        childA.quadID.append(0)
        
        childBCentre = [self.centrePt[0]+(0.5*self.halfXDim), self.centrePt[1]+(0.5*self.halfYDim)]
        childB = quadTree2D(childBCentre, self.halfXDim/2.0, self.halfYDim/2.0, self.maxPts, self.levelID+1)
        childB.quadID = self.quadID[:]
        childB.quadID.append(1)
        
        childCCentre = [self.centrePt[0]-(0.5*self.halfXDim), self.centrePt[1]-(0.5*self.halfYDim)]
        childC = quadTree2D(childCCentre, self.halfXDim/2.0, self.halfYDim/2.0, self.maxPts, self.levelID+1)
        childC.quadID = self.quadID[:]
        childC.quadID.append(2)
        
        childDCentre = [self.centrePt[0]+(0.5*self.halfXDim), self.centrePt[1]-(0.5*self.halfYDim)]
        childD = quadTree2D(childDCentre, self.halfXDim/2.0, self.halfYDim/2.0, self.maxPts, self.levelID+1)
        childD.quadID = self.quadID[:]
        childD.quadID.append(3)
        
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
    
    def getPtsByPt(self, pt):
        '''
        Retrieve the points at the leaf containing the given point
        ::param pt [float x, float y]
        '''
        if self.chkBounds(pt) == False:
            print 'Pt not in tree bounds'
            return 0
        if self.subDivided == False:
            return self.points
        for child in self.children:
            if child.chkBounds(pt) == True:
                outPts = child.getPtsByPt(pt)
        return outPts
    
    
    def getPtsByQID(self, inQuadID, outPoints):
        '''
        Retrieve the points stored at a specific quadID
        Aggregates points at lower levels
        ::param quadID [0,1,2,3,2,1,2]
        ::param outPoints [] to be filled
        '''
        #When we are the given level start aggregating
        if self.quadID == inQuadID or self.quadID[0:len(inQuadID)] == inQuadID:
            #0 if its subdivided, everything if its not
            outPoints.append(self.points)
            for child in self.children:
                child.getPtsByQID(inQuadID, outPoints)
        return outPoints
                
            
    
    
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
    
    
        
    
        