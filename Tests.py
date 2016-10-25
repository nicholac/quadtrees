'''
Created on 25 Oct 2016

'''
import unittest
from random import random, randint
from QuadTree import quadTree2D


class TestQuadTree2D(unittest.TestCase):

    def setUp(self):
        self.xDim = 10.0
        self.yDim = 10.0
        self.numPts = 1000
        self.maxPtsPerQuad = 10
        self.centrePt = [float(self.xDim/2.0), float(self.yDim/2.0)]
        #Init the blank tree
        self.quadT = quadTree2D(self.centrePt, float(self.xDim)/2.0, float(self.yDim)/2.0, self.maxPtsPerQuad, 0)


    def tearDown(self):
        self.quadT.dumpAllPoints()
        self.assertEqual(self.quadT.getTotalPts(), 0)
        self.assertEqual(self.quadT.children, [])


    def genTestData(self, xDim, yDim, numPts):
        '''
        Generate some test data to insert to the tree
        '''
        points = []
        for i in range(0, numPts):
            points.append([random()+randint(0,xDim), random()+randint(0,yDim)])
        return points


#     def test_initTree(self):
#         '''
#         Basic Init Tests
#         '''
#         self.assertEqual(self.quadT.maxPts, self.maxPtsPerQuad)
#         self.assertEqual(self.quadT.children, [])
#         self.assertEqual(self.quadT.centrePt, [float(self.xDim/2.0), float(self.yDim/2.0)])
#         self.assertEqual(self.quadT.halfXDim, float(self.xDim/2.0))
#         self.assertEqual(self.quadT.halfYDim, float(self.yDim/2.0))
#         self.assertEqual(self.quadT.points, [])
#         self.assertEqual(self.quadT.subDivided, False)
#         self.assertEqual(self.quadT.levelID, 0)
#     
#     
#     def test_loadData(self):
#         '''
#         Load Data
#         '''
#         tstData = self.genTestData(self.xDim, self.yDim, self.numPts)
#         cnt = 0
#         badPts = 0
#         for pt in tstData:
#             #Check random gen points and bounds independently
#             if pt[0]>10.0 or pt[1]>10.0:
#                 badPts+=1
#             chk = self.quadT.insertPt(pt)
#             if chk == True:
#                 cnt+=1
#         self.assertEqual(cnt, self.numPts-badPts)
#         self.assertEqual(self.quadT.getTotalPts(), cnt)
#     
#     
#     def test_dumpAllPoints(self):
#         '''
#         Flush the tree
#         '''
#         self.quadT.dumpAllPoints()
#         self.assertEqual(self.quadT.getTotalPts(), 0)
#         self.assertEqual(self.quadT.getDepth(0), 0)
#     
#     
#     def test_getDepth(self):
#         '''
#         Check Quadtree depth - init with non random data
#         '''
#         cnt = 0
#         for i in range(0,10):
#             #Need to add a bit of noise so the tree bottoms out
#             chk = self.quadT.insertPt([1.1, 1.1])
#             if chk == True:
#                 cnt+=1
#         self.assertEqual(cnt, 10)
#         self.assertEqual(self.quadT.getTotalPts(), 10)
#         self.assertEqual(self.quadT.getDepth(0), 0)
#         #Tip it over to next layer
#         chk = self.quadT.insertPt([5.51, 5.51])
#         if chk == True:
#             cnt+=1
#         self.assertEqual(cnt, 11)
#         self.assertEqual(self.quadT.getTotalPts(), 11)
#         self.assertEqual(self.quadT.getDepth(0), 1)
#         #Once more 
#         for i in range(0,9):
#             #Need to add a bit of noise so the tree bottoms out
#             chk = self.quadT.insertPt([5.51, 5.51])
#             if chk == True:
#                 cnt+=1
#         self.assertEqual(cnt, 20)
#         self.assertEqual(self.quadT.getTotalPts(), 20)
#         self.assertEqual(self.quadT.getDepth(0), 1)
#         #Tip it over to next layer
#         chk = self.quadT.insertPt([7.51, 7.51])
#         if chk == True:
#             cnt+=1
#         self.assertEqual(cnt, 21)
#         self.assertEqual(self.quadT.getTotalPts(), 21)
#         self.assertEqual(self.quadT.getDepth(0), 2)
#     
#     def test_getQueryQuad(self):
#         '''
#         Query the tree at a given position
#         '''
#         self.quadT.dumpAllPoints()
#         tstPt = []
#         chkPts1 = []
#         cnt = 0
#         for i in range(0,10):
#             #Need to add a bit of noise so the tree bottoms out
#             chkPts1.append([1.1, 1.1])
#             chk = self.quadT.insertPt([1.1, 1.1])
#             if chk == True:
#                 cnt+=1
#         self.assertEqual(cnt, 10)
#         self.assertEqual(self.quadT.getTotalPts(), 10)
#         self.assertEqual(self.quadT.getDepth(0), 0)
#         #Tip it over to next layer
#         chk = self.quadT.insertPt([5.51, 5.51])
#         if chk == True:
#             cnt+=1
#         #Grab points
#         chkPts2 = self.quadT.getPtsByPt([7.5, 7.5])
#         self.assertEqual(chkPts2, [[5.51, 5.51]])
#         chkPts2 = self.quadT.getPtsByPt([2.456, 4.334])
#         self.assertEqual(chkPts2, chkPts1)
#         self.quadT.dumpAllPoints()


    def test_quadids(self):
        '''
        Check we are mapping quadIDs properly
        '''
        tstPt = []
        chkPts1 = []
        cnt = 0
        for i in range(0,10):
            #Need to add a bit of noise so the tree bottoms out
            chkPts1.append([1.1, 1.1])
            chk = self.quadT.insertPt([1.1, 1.1])
            if chk == True:
                cnt+=1
        self.assertEqual(cnt, 10)
        self.assertEqual(self.quadT.getTotalPts(), 10)
        self.assertEqual(self.quadT.getDepth(0), 0)
        #Tip it over to next layer
        chk = self.quadT.insertPt([5.51, 5.51])
        self.assertEqual(self.quadT.getDepth(0), 1)
        self.assertEqual(self.quadT.quadID, [0])
        for idx, child in enumerate(self.quadT.children):
            self.assertEqual(child.quadID, [0, idx])
        #Once more 
        for i in range(0,9):
            #Need to add a bit of noise so the tree bottoms out
            chk = self.quadT.insertPt([5.51, 5.51])
            if chk == True:
                cnt+=1
        for idx1, child in enumerate(self.quadT.children):
            for idx2, child2 in enumerate(child.children):
                self.assertEqual(child2.quadID, [0, idx1, idx2])
        

    def test_maxDepth(self):
        '''
        Test if the tree bottoms out at max depth without dying
        '''
        cnt = 0
        for i in range(0,11):
            #Need to add a bit of noise so the tree bottoms out
            chk = self.quadT.insertPt([1.1, 1.1])
            if chk == True:
                cnt+=1
        self.assertEqual(cnt, 11)
        self.assertEqual(self.quadT.getTotalPts(), 11)
        self.assertEqual(self.quadT.getDepth(0), self.quadT.maxDepth)
    
    
    def test_getPtsbyQuadID(self):
        '''
        Retrieve all points under a given quadID
        '''
        tstPt = []
        chkPts1 = []
        cnt = 0
        for i in range(0,10):
            #Need to add a bit of noise so the tree bottoms out
            chk = self.quadT.insertPt([1.1, 1.1])
            if chk == True:
                cnt+=1
        self.assertEqual(cnt, 10)
        self.assertEqual(self.quadT.getTotalPts(), 10)
        self.assertEqual(self.quadT.getDepth(0), 0)
        #Tip it over to next layer
        chk = self.quadT.insertPt([5.51, 5.51])
        self.assertEqual(self.quadT.getTotalPts(), 11)
        
        #Now get the points at quadID
        outPoints = []
        self.quadT.getPtsByQID([0,1], outPoints)
        self.assertEqual(outPoints, [[5.51, 5.51]])
        self.assertEqual(self.quadT.getDepth(0), 1)
        
        #Check we dont get points above a small requested QID
        outPoints = []
        self.quadT.getPtsByQID([0,1,1,1], outPoints)
        self.assertEqual(outPoints, [])
        
        #Try deeper
        chkPts1 = []
        for i in range(0,10):
            #Need to add a bit of noise so the tree bottoms out
            chk = self.quadT.insertPt([9.1, 9.12])
            chkPts1.append([9.1, 9.12])
            if chk == True:
                cnt+=1
        self.assertEqual(self.quadT.getTotalPts(), 21)
        self.assertEqual(self.quadT.getDepth(0), 2)
         
        #Check we can get all the points this way
        outPoints = []
        self.quadT.getPtsByQID([0], outPoints)
        self.assertEqual(len(outPoints), self.quadT.getTotalPts())

        #Check hi-res
        outPoints = []
        self.quadT.getPtsByQID([0,1,1], outPoints)
        self.assertEqual(outPoints, chkPts1)
        
        #Check hi-res
        outPoints = []
        self.quadT.getPtsByQID([0,1,2], outPoints)
        self.assertEqual(outPoints, [[5.51, 5.51]])
    
    def test_quadIDsByVertexDist(self):
        '''
        Get quads by distance of their vertices from given point
        '''
        tstPt = []
        chkPts1 = []
        cnt = 0
        for i in range(0,10):
            #Need to add a bit of noise so the tree bottoms out
            chk = self.quadT.insertPt([1.1, 1.1])
            if chk == True:
                cnt+=1
        self.assertEqual(cnt, 10)
        self.assertEqual(self.quadT.getTotalPts(), 10)
        self.assertEqual(self.quadT.getDepth(0), 0)
        #Tip it over to next layer
        chk = self.quadT.insertPt([5.51, 5.51])
        self.assertEqual(self.quadT.getTotalPts(), 11)
        self.assertEqual(self.quadT.getDepth(0), 1)
        
        chkPt = [5.1, 9.9]
        chkDist = 2.1
        quadIDs = []
        self.quadT.vertexDist(chkPt, chkDist, quadIDs)
        self.assertEqual(quadIDs, [[0,1]])
    
    def test_getBounds(self):
        inShapeVerts = [[1.0, 10.0], [10.0, 12.0], [10.0, 1.5], [1.0, 0.5]]
        bbox = self.quadT.getBounds(inShapeVerts)  
        self.assertEqual(bbox, [[1.0, 0.5], [10.0, 12.0]]) 
        
    def test_minBoundingQuad(self):
        '''
        Get smallest quad that fiully bounds the given shape
        '''
        tstPt = []
        chkPts1 = []
        cnt = 0
        for i in range(0,10):
            #Need to add a bit of noise so the tree bottoms out
            chk = self.quadT.insertPt([1.1, 1.1])
            if chk == True:
                cnt+=1
        self.assertEqual(cnt, 10)
        self.assertEqual(self.quadT.getTotalPts(), 10)
        self.assertEqual(self.quadT.getDepth(0), 0)
        #Tip it over to next layer
        chk = self.quadT.insertPt([5.51, 5.51])
        self.assertEqual(self.quadT.getTotalPts(), 11)
        #Try deeper
        chkPts1 = []
        for i in range(0,10):
            #Need to add a bit of noise so the tree bottoms out
            chk = self.quadT.insertPt([9.1, 9.12])
            chkPts1.append([9.1, 9.12])
            if chk == True:
                cnt+=1
        self.assertEqual(self.quadT.getTotalPts(), 21)
        self.assertEqual(self.quadT.getDepth(0), 2)
        #Now check the bounding quad
        inShapeVerts = [[7.6, 7.6], [7.6, 9.2], [9.2, 9.2], [9.2, 7.6]]
        quadID = self.quadT.minBoundingQuad(inShapeVerts, [0])
        self.assertEqual(quadID, [0,1,1])
        #Try deeper
        chkPts1 = []
        for i in range(0,10):
            #Need to add a bit of noise so the tree bottoms out
            chk = self.quadT.insertPt([9.1, 9.12])
            chkPts1.append([9.1, 9.12])
            if chk == True:
                cnt+=1
        self.assertEqual(self.quadT.getTotalPts(), 31)
        self.assertEqual(self.quadT.getDepth(0), 10)
        #Now check the bounding quad
        inShapeVerts = [[7.6, 7.6], [7.6, 9.2], [9.2, 9.2], [9.2, 7.6]]
        quadID = self.quadT.minBoundingQuad(inShapeVerts, [0])
        self.assertEqual(quadID, [0,1,1])
        #Check a very small one
        inShapeVerts = [[7.6123123, 7.66123123], [7.6123123, 7.67123123], [7.6223123, 7.67123123], [7.6223123, 7.66123123]]
        quadID = self.quadT.minBoundingQuad(inShapeVerts, [0])
        self.assertEqual(quadID, [0, 1, 1, 2])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()