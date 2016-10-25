'''
Created on 24 Oct 2016

northwest = 0
northeast = 1
southwest = 2
southeast = 3

'''

from __builtin__ import False
import math


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
        self.vertices = []
        self.points = []
        self.subDivided = False
        self.levelID = levelID
        #Record top level dims
        self.worldMinX = 0.0
        self.worldMinY = 0.0
        self.worldMaxX = 0.0
        self.worldMaxY = 0.0
        if levelID == 0:
            self.worldMinX = centrePt[0]-halfXDim
            self.worldMinY = centrePt[1]-halfYDim
            self.worldMaxX = centrePt[0]+halfXDim
            self.worldMaxY = centrePt[1]+halfYDim
        self.quadID = [0]
        #Maximum depth for the tree - to stop recursion when adding many points the same
        self.maxDepth = 10
        self.generateVertices()
        
    
    def generateVertices(self):
        '''
        Populate the vertices for this quad
        memory vs re-calc
        '''
        tl = [self.centrePt[0]-self.halfXDim, self.centrePt[1]+self.halfYDim]
        tr = [self.centrePt[0]+self.halfXDim, self.centrePt[1]+self.halfYDim]
        bl = [self.centrePt[0]-self.halfXDim, self.centrePt[1]-self.halfYDim]
        br = [self.centrePt[0]+self.halfXDim, self.centrePt[1]-self.halfYDim]
        self.vertices = [tl, tr, bl, br]
     
    def subdivide(self):
        '''Build & populate children
        '''
        childACentre = [self.centrePt[0]-(0.5*self.halfXDim), self.centrePt[1]+(0.5*self.halfYDim)]
        childA = quadTree2D(childACentre, self.halfXDim/2.0, self.halfYDim/2.0, self.maxPts, self.levelID+1)
        childA.quadID = self.quadID[:]
        childA.quadID.append(0)
        childA.worldMaxX = self.worldMaxX
        childA.worldMaxY = self.worldMaxY
        childA.worldMinX = self.worldMinX
        childA.worldMinX = self.worldMinY
        
        childBCentre = [self.centrePt[0]+(0.5*self.halfXDim), self.centrePt[1]+(0.5*self.halfYDim)]
        childB = quadTree2D(childBCentre, self.halfXDim/2.0, self.halfYDim/2.0, self.maxPts, self.levelID+1)
        childB.quadID = self.quadID[:]
        childB.quadID.append(1)
        childB.worldMaxX = self.worldMaxX
        childB.worldMaxY = self.worldMaxY
        childB.worldMinX = self.worldMinX
        childB.worldMinX = self.worldMinY
        
        childCCentre = [self.centrePt[0]-(0.5*self.halfXDim), self.centrePt[1]-(0.5*self.halfYDim)]
        childC = quadTree2D(childCCentre, self.halfXDim/2.0, self.halfYDim/2.0, self.maxPts, self.levelID+1)
        childC.quadID = self.quadID[:]
        childC.quadID.append(2)
        childC.worldMaxX = self.worldMaxX
        childC.worldMaxY = self.worldMaxY
        childC.worldMinX = self.worldMinX
        childC.worldMinX = self.worldMinY
        
        childDCentre = [self.centrePt[0]+(0.5*self.halfXDim), self.centrePt[1]-(0.5*self.halfYDim)]
        childD = quadTree2D(childDCentre, self.halfXDim/2.0, self.halfYDim/2.0, self.maxPts, self.levelID+1)
        childD.quadID = self.quadID[:]
        childD.quadID.append(3)
        childD.worldMaxX = self.worldMaxX
        childD.worldMaxY = self.worldMaxY
        childD.worldMinX = self.worldMinX
        childD.worldMinX = self.worldMinY
        
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
                if self.levelID < self.maxDepth:
                    self.subdivide()
                    return True
                else:
                    #Bottomed out - points been added, do nothing
                    pass
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
        if inQuadID[0:len(self.quadID)] == self.quadID[0:len(inQuadID)]:
            #Its in this branch
            if self.subDivided == False:
                #Make sure we dont get points for layer above the requested
                if len(self.quadID)>=len(inQuadID):
                    for i in self.points:
                        outPoints.append(i)
            else:
                for child in self.children:
                    child.getPtsByQID(inQuadID, outPoints)
        return outPoints
                
    
    def getPtsByDistance(self, tstPt, tstDist):
        '''
        Retrieve points based on distance from given point - 
        uses min bounding quad for input pt and dist
        ::param tstPt [x,y]
        ::param dist float dist to search 2d in this space
        :: outPoints results
        '''
        #Convert to bounding shape
        bBox = [[tstPt[0]-tstDist, tstPt[1]-tstDist], 
                [tstPt[0]-tstDist, tstPt[1]+tstDist],
                [tstPt[0]+tstDist, tstPt[1]+tstDist],
                [tstPt[0]+tstDist, tstPt[1]-tstDist]]
        
        #Get min bounding quad
        minQuad = self.minBoundingQuad(bBox)
        #Get points in this quad
        outPts = []
        self.getPtsByQID(minQuad, outPts)
        return outPts
    
    
    def vertexDist(self, chkPt, chkDist, quadIDs):
        '''
        Helper function for getting points by distance
        Works through the tree grabbing quad id's based on the distance of their 
        vertices from given dist
        '''   
        #Leaf and has data?
        if self.subDivided == False:
            if len(self.points) > 0:
                for v in self.vertices:  
                    if self.dist2D(v, chkPt) <= chkDist:
                        quadIDs.append(self.quadID)
            else:
                #No data here
                return
        else:
            for child in self.children:
                child.vertexDist(chkPt, chkDist, quadIDs)
        return quadIDs
            
        
    def dist2D(self, pt0, pt1):
        return math.sqrt(math.pow((pt0[0]-pt1[0]), 2.0)+math.pow((pt0[1]-pt1[1]), 2.0))
    
    
    def minBoundingQuad(self, inShapeVerts):
        '''
        Find the smallest quad that bounds the given shape
        ::param inShapeVerts [[x,y], [x,y], ...] Shape vertices
        '''
        #Top level
        if self.containsShape(inShapeVerts) == True:
            if self.subDivided == True:
                chkContains = []
                chk = False
                for child in self.children:
                    QID = child.minBoundingQuad(inShapeVerts)
                    if QID:
                        return QID
                return self.quadID
            else:
                #Smallest?
                return self.quadID
        else:
            return None
            
    
    def containsShape(self, inShapeVerts):
        '''
        Check if quad contains the given shape
        ::param inShapeVerts [[x,y], [x,y], ...]
        '''
        #Get bounds
        bRect = self.getBounds(inShapeVerts)
        #Trim to Tree world dims if required
        for idx, pt in enumerate(bRect):
            if pt[0] < self.worldMinX:
                bRect[idx][0] = self.worldMinX
            if pt[1] < self.worldMinY:
                bRect[idx][1] = self.worldMinY
            if pt[0] > self.worldMaxX:
                bRect[idx][0] = self.worldMaxX
            if pt[1] > self.worldMaxY:
                bRect[idx][1] = self.worldMaxY
        #Now check intersection 
        for pt in bRect:
            if self.chkBounds(pt) == False:
                #Isnt contained by this quad
                return False
        #Is contained by this quad
        return True
        
        
    def getBounds(self, inShapeVerts):
        '''
        Get bounding rect of given shape
        '''
        maxX = 0.0
        maxY = 0.0
        minX = 9999999.0
        minY = 9999999.0
        for pt in inShapeVerts:
            #shape bounds
            if pt[0]<minX:
                minX = pt[0]
            if pt[1]<minY:
                minY = pt[1]
            if pt[0] > maxX:
                maxX = pt[0]
            if pt[1]>maxY:
                maxY = pt[1]
        return [[minX, minY], [maxX, maxY]]
        
        
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
        self.children = []   
    
    
        
    
        