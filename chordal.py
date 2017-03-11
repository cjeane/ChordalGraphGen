from __future__ import print_function
import random
import math
import numpy as np
from sets import Set
from collections import deque #for queues

import Tkinter
import tkMessageBox

def isStrInt(str):
	try: 
		int(str)
		return True
	except ValueError:
		return False

#node stucture for a tree 
class NodeTree:
	
	def __init__(self, data):
		self.data = data
		self.parent = None
		self.leftChild = None
		self.rightChild = None

	def __repr__ (self):
		return "(%s, %s, %s)" % (self.data, self.leftChild, self.rightChild)
	def __str__ (self):
		return "(%s, %s, %s)" % (self.data, self.leftChild, self.rightChild)

#node strucutre for a two purpose tree and adjency lists		
class NodeGen:
	
	def __init__(self, data, tree):
		self.data = data
		if tree==True:
			self.neighbour = [None, None, None] ## for tree representation 0 = parent, 1=leftChild, 2= rightChild
		else:
			self.neighbour=Set()
	
	def __repr__(self):
		li = []
		for i in self.neighbour:
			li.append (i.data)		
		return "(D:%s|N:%s)" % (self.data, li)
	
	#returns neighbour
	def getAdj(self):
		return self.neighbour
		
#tree structure		
class Tree:

	def __init__ (self):
		self.size = 0
		self.root = None		
	
	#returns the root of the tree 
	def getRoot (self):
		return self.root
	
	#Adds a node to the tree
	#Input: The root node, and the data to be added
	#Output: None
	def insertNode (self, node, data):
		if node == None:
			self.root = NodeGen (data, True)
			self.size += 1
		else:
			if data < node.data and node.neighbour[1] == None:
				node.neighbour[1] = NodeGen (data, True)
				node.neighbour[1].neighbour[0] = node
				self.size += 1
			elif data < node.data:
				self.insertNode (node.neighbour[1], data)
			elif data > node.data and node.neighbour[2] == None:
				node.neighbour[2] = NodeGen (data, True)
				node.neighbour[2].neighbour[0] = node
				self.size += 1
			elif data > node.data:
				self.insertNode (node.neighbour[2], data)
		return
		
	#prints out inOrder traveseral of tree
	#Input: The root node
	#Output: Display inorder traveseral of tree
	def inOrder(self, node):
		if node != None:
			self.inOrder (node.neighbour[1])
			print (node.data)
			self.inOrder (node.neighbour[2])
		return
			
	#prints out the preOrder traveseral of tree
	#Input: The root node
	#Output: Display preorder traveseral of tree
	def preOrder(self, node):
		if node != None:
			print (node.data)
			self.preOrder (node.neighbour[1])
			self.preOrder (node.neighbour[2])
		return

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
		
	def __repr__ (self):
		return "(X:%s, Y:%s)" % (self.x, self.y)

#class for generating a sparse chordal graph
class ChordalSparse:
	
	def __init__ (self):
		self.edges = 0
		self.vertex = 0
		self.root = None
		self.edgeNeed = 0
		self.dictNode = {} #the structure for holding all the points
		self.generatedPtList =None
		self.matrixDist = None
		self.ptMap = None
		self.listVerticeDegree1=[]
	
	#returns the dictionary(hashmap) for the adjency list
	#Input: None
	#Output: The adjency list hashmap
	def getGraph(self):
		return self.dictNode
	
	#the general starting point of the connected graph
	#Input: None
	#Output: The starting node in graph/tree
	def getRoot(self):
		return self.root
	
	#takes the tree and converts it an adjency list structure
	#Input: A tree class 
	#Output: None
	def convertFromTree(self, tree):
		self.root = tree.getRoot()
		self.removeNoneEdgeFromTree(self.root,Set())
		self.edges = self.vertex - 1 
		return
	
	#remove the None points that exists in leaf nodes from trees
	#input: the base node, and list of already visited node
	#output: none
	def removeNoneEdgeFromTree(self, node, visited):
		if node != None:			
			temp = Set(node.neighbour)
			node.neighbour = temp
			if None in node.neighbour: node.neighbour.remove(None)
			self.dictNode[node.data] = node
			visited.add(node)
			self.vertex+=1
		for i in node.neighbour:
			if i not in visited:
				self.removeNoneEdgeFromTree(i, visited)
		return

	#checks if a edge between two vertex
	#input: two vertex
	#out: boolean value of if an edge exist between the vertex
	def ifEdgeExist(self, v1, v2):
		return v2 in v1.neighbour or v1 in v2.neighbour
		
	#adds an edge between two vertex
	#input: two vertex
	#out: none
	def addEdge(self, v1, v2): 
		v1.neighbour.add(v2) 
		v2.neighbour.add(v1)
		self.edges +=1
		
	#test for if the two suggested vertex is still chordal
	#input: two vertex
	#output: boolean if adding an edge between two point will maintain chordalality
	def insertQuery(self, v1, v2):
		setInter = v1.neighbour.intersection(v2.neighbour)
		if len(setInter) == 0:
			return False
		else:
			sampleV = random.sample(setInter, 1)
			if self.bfs(v1, v2, setInter, sampleV[0].neighbour):
				self.addEdge(v1,v2)
				return True
		return False
	
	#breathe first search for path exist between start and goal
	#input: vertex of start, goal and visited = Set Intersection of the two vertex, adj is the set of neighbours of a point
	#output: boolean value of the condition 
	def bfs (self, start, goal, visited, adj):
		q = deque([])
		current = None
		
		q.append(start)
		visited.add(start)		
		while q:
			current = q.popleft()
			if current == goal:
				return False
			for vertex in current.neighbour:
				if vertex in adj and vertex not in visited:
					q.append(vertex)
				if vertex not in visited:
					visited.add(vertex)
		return True 
		
	#tries to add the num of edges to the graph maintain chordalality
	#input: int number of edges to be added
	#output: none
	def addRanEdges(self, num):
		goal = (num+self.edges)		
		if ((num+self.edges) > ((self.vertex * (self.vertex-1)))/2):
			print ("Unable to this many edges")
			return False
		while self.edges < goal:
			if len(self.listVerticeDegree1)==0:
				ranPt1=random.randint(0,self.vertex-1)
			else:
				ranPt1=random.sample(self.listVerticeDegree1,1)[0]
			ranPt2=random.randint(0,self.vertex-1)
			testV1 =  self.dictNode[ranPt1]
			testV2 =  self.dictNode[ranPt2]
			if testV1 == testV2 or self.ifEdgeExist(testV1,testV2):
				continue
			else:
				if (self.insertQuery(testV1, testV2) and len(self.listVerticeDegree1) !=0):
					try:
						self.listVerticeDegree1.remove(ranPt1)
					except ValueError:
						pass
					try:
						self.listVerticeDegree1.remove(ranPt2)
					except ValueError:
						pass

	###Sets up random points 
	###input: two positive ints for the range of number to generated
	###output: none
	def setupPoints(self, minRange, maxRange):
		self.ptMap= dict()
		used =[]
		self.generatedPtList= self.ptMap
		for i in range (self.vertex):			
			p= Point(random.randint(minRange, maxRange),random.randint(minRange, maxRange))
			while (p in used):
				p= Point(random.randint(minRange, maxRange),random.randint(minRange, maxRange))
			self.ptMap[i]=p
			used.append(p)
		for i in range(self.vertex):
			if (len(self.dictNode[i].neighbour) == 1):
				self.listVerticeDegree1.append(i)
		
		return None
	
	#fills in the a random distance squared matrix based on the graph created must be called after setupPoints
	#input: none
	#output: the distance Squared Matrix 
	def createDistSqMatrix(self):
		matrix = [[0 for x in range(len(self.dictNode))] for y in range(len(self.dictNode))]		
					
		for i in range(len(self.dictNode)):
			for j in range(i,len(self.dictNode)):
				if self.ifEdgeExist(self.dictNode[i],self.dictNode[j]):
					matrix[i][j]= self.calcDistSq(self.ptMap[i],self.ptMap[j])
					matrix[j][i]= matrix[i][j]
				else:
					matrix[i][j]= 0
		
		return matrix
	
			
	#calculates the distanceSquared between two points
	#Input: Two x,y points
	#Output: the distance squared between the two points
	def calcDistSq(self, pt1, pt2):
		return math.pow (pt2.x-pt1.x,2) + math.pow (pt2.y-pt1.y,2)
 
	#sets up and creates the display for chordal graph
	#input none
	#output creates and fills the canvas with the graph
	def createDisplay(self, w, h, minRange, maxRange):
		screenHeight = h
		screenWidth = w
		master = Tkinter.Tk()
		
		w = Tkinter.Canvas(master, width=w, height=h)
		w.pack()
		rangeDif = maxRange - minRange
		
		
		for i in range (self.vertex):
			#print (chor.dictNode[i].data)
			for n in self.dictNode[i].neighbour:
				#print ("N: ",n.data)
				self.drawLine(w,self.dictNode[i].data, n.data, screenHeight, screenWidth, rangeDif)
				#w.create_line()
		for i in range (self.vertex):
			self.drawCircle(w,self.dictNode[i].data,3, screenHeight, screenWidth, rangeDif)
		
		
		return None
	
	#draws a circle (internal fcn)
	#input requires the canvas object, a point object, and radius (int)
	#output draws a red circle at that point
	def drawCircle(self, canvas, pt, r, maxHeight, maxWidth, rangeDif):		
				
		canvas.create_oval((self.ptMap[pt].x)*maxWidth/rangeDif-r, maxHeight-((self.ptMap[pt].y))*maxHeight/rangeDif-r, 
			(self.ptMap[pt].x)*maxWidth/rangeDif+r, maxHeight-((self.ptMap[pt].y))*maxHeight/rangeDif+r, fill="red")
		return None
	
	#draws a line (internal fcn)
	#input requires the canvas object, 2 point object
	#output draws a black line between two points
	def drawLine(self, canvas, pt1, pt2, maxHeight, maxWidth, rangeDif):		

		canvas.create_line(self.ptMap[pt1].x*maxWidth/rangeDif, maxHeight-(self.ptMap[pt1].y*maxHeight/rangeDif), 
			self.ptMap[pt2].x*maxWidth/rangeDif, maxHeight-(self.ptMap[pt2].y*maxHeight/rangeDif))		
		return None
	
	#saves the distance matrix to a given file name
	#input filename as name including the extension type needed
	#saves distance matrix at the current directory
	def saveFile(self,name):
		np.savetxt(name, self.matrixDist)
		return None		


class gui_tk(Tkinter.Tk):
	
	
	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent				
		self.matrixReady= False
		self.tree= None
		self.chor= None
		self.ready = False
		self.initialize()

	##defines the menu layout in grid view
	def initialize(self):
		self.grid()
		
		self.labelNumVerticesText = Tkinter.StringVar()
		labelVertices = Tkinter.Label(self, textvariable=self.labelNumVerticesText)
		labelVertices.grid(row=0, sticky=Tkinter.W)
		self.labelNumVerticesText.set(u'Number of vertices to make:')
		
		self.verticeEntry = Tkinter.Entry(self)
		self.verticeEntry.grid (column=1, row=0, sticky=Tkinter.W)
		
		self.labelNumEdgesText = Tkinter.StringVar()
		labelEdges = Tkinter.Label(self, textvariable=self.labelNumEdgesText)
		labelEdges.grid(row=1, sticky=Tkinter.W)
		self.labelNumEdgesText.set(u'Number of edges to make:')
		
		self.edgeEntry = Tkinter.Entry(self)
		self.edgeEntry.grid (column=1, row=1, sticky=Tkinter.W)
		
		self.labelNumRangeText =Tkinter.StringVar()
		labelNumRange = Tkinter.Label(self,textvariable=self.labelNumRangeText)
		labelNumRange.grid(row=2, sticky=Tkinter.W)
		self.labelNumRangeText.set(u'Enter the value range for points:')
		
		self.numRangeLowEntry = Tkinter.Entry(self)
		self.numRangeLowEntry.grid (column=1, row=2, sticky=Tkinter.W)
		
		self.numRangeHighEntry = Tkinter.Entry(self)
		self.numRangeHighEntry.grid (column=2, row=2, sticky=Tkinter.W)
		
		buttonGenerateGraph = Tkinter.Button(self,text="GenerateGraph", 
			command=self.onGenerateGraphClick)##edit command
		buttonGenerateGraph.grid(column=0,row=3, sticky=Tkinter.W)
		
		self.addEdgesText =Tkinter.StringVar()
		labelAddEdges = Tkinter.Label(self,textvariable=self.addEdgesText)
		labelAddEdges.grid(row=4, sticky=Tkinter.W)
		self.addEdgesText.set(u'Enter the amount of edges to add:')
		
		self.AddEdgesEntry = Tkinter.Entry(self)
		self.AddEdgesEntry.grid (column=1, row=4, sticky=Tkinter.W)

		buttonAddEdges = Tkinter.Button(self,text="Add Edges", 
			command=self.onClickAddEdges)##edit command
		buttonAddEdges.grid(column=2,row=4, sticky=Tkinter.W)
		
		buttonDisplayGraph = Tkinter.Button(self,text="Display Graph", 
			command=self.onDisplayGraph)##edit command
		buttonDisplayGraph.grid(column=0,row=5, sticky=Tkinter.W)
		
		buttonDisplayLabels = Tkinter.Button(self,text="Display Point Labels with Graph", 
			command=self.dummyClick)##edit command
		#buttonDisplayLabels.grid(column=0,row=6, sticky=Tkinter.W)
		
		self.saveDistMatrixText =Tkinter.StringVar()
		labelSaveDistMatrix = Tkinter.Label(self,textvariable=self.saveDistMatrixText)
		labelSaveDistMatrix.grid(row=7, sticky=Tkinter.W)
		self.saveDistMatrixText.set(u'Distance matrix save to file name:')
		
		self.saveDistMatrixEntry= Tkinter.Entry(self)
		self.saveDistMatrixEntry.grid(column=1,row=7, sticky=Tkinter.W)
		
		buttonSaveDistMatrix = Tkinter.Button(self,text="Save", 
			command=self.onSaveMatrixClick)##edit command
		buttonSaveDistMatrix.grid(column=2,row=7, sticky=Tkinter.W +Tkinter.E)
		
		buttonDisplayDistMatrix = Tkinter.Button(self,text="Display distance matrix", 
			command=self.onDisplayMatrixClick)##edit command
		buttonDisplayDistMatrix.grid(column=3,row=7, sticky=Tkinter.W)
		
		self.savePtListText =Tkinter.StringVar()
		labelSavePtList = Tkinter.Label(self,textvariable=self.savePtListText)
		labelSavePtList.grid(row=8, sticky=Tkinter.W)
		self.savePtListText.set(u'Point list save to file name:')
		
		self.savePtListEntry= Tkinter.Entry(self)
		self.savePtListEntry.grid(column=1,row=8, sticky=Tkinter.W)
		
		buttonSavePtList = Tkinter.Button(self,text="Save", 
			command=self.onSavePtListClick)##edit command
		buttonSavePtList.grid(column=2,row=8, sticky=Tkinter.W +Tkinter.E)
		
		buttonDisplayPtList = Tkinter.Button(self,text="Display points", 
			command=self.onDisplayPtListClick)##edit command
		buttonDisplayPtList.grid(column=3,row=8, sticky=Tkinter.W+Tkinter.E)
		
		
		labeloutputText = Tkinter.Label(self,text="Output Box:")
		labeloutputText.grid(row=9, sticky=Tkinter.W)
		
		
		self.textBox = Tkinter.Text(self,width = 50, height = 10, wrap = 'word')
		self.textBox.grid (column = 0, row =10, columnspan=4, sticky=Tkinter.W+Tkinter.E)
	
	###dummy function to hold non implemented commands
	def dummyClick(self):
		tkMessageBox.showwarning("Error", "Function not implemented!!")			
		return None
	
	### saves the distance matrix to fileName from entry
	def onSaveMatrixClick(self):
		if (self.ready == False):
			tkMessageBox.showwarning("Error", "No graph generated please generate a graph first.")
			return
		fileName = self.saveDistMatrixEntry.get()
		if '.' not in fileName:
			fileName+=".txt"			
		elif not fileName.endswith(".txt"):
			tkMessageBox.showwarning("Error", "File name extension provided is not valid")		
			return None		
		np.savetxt(fileName, self.chor.matrixDist)
		return None
	
	### saves the pointList to fileName from entry
	def onSavePtListClick(self):
		if (self.ready == False):
			tkMessageBox.showwarning("Error", "No graph generated please generate a graph first.")
			return
		
		self.chor.generatedPtList = [n for n in self.chor.generatedPtList if n is not None]	
		
		fileName=self.savePtListEntry.get()
		
		if '.' not in fileName:
			fileName+=".txt"			
		elif not fileName.endswith(".txt"):
			tkMessageBox.showwarning("Error", "File name extension provided is not valid")		
			return None
			
		file= open(fileName, 'w')
		for pt in self.chor.generatedPtList:
			output = str (pt)
			output= output +":: "+str (self.chor.ptMap[pt])
			file.write("%s\n" % output)
		
		
	### displays the content of the distance matrix in the output text box
	def onDisplayMatrixClick(self):
		if (self.ready == False):
			tkMessageBox.showwarning("Error", "No graph generated please generate a graph first.")
			return
		self.textBox.delete(1.0,'end')
		self.textBox.insert(1.0,"Distance Matrix Squared Representation:\n")
		self.chor.matrixDist= np.matrix(self.chor.createDistSqMatrix())
		self.textBox.insert('end', str(self.chor.matrixDist))

	### displays the content of the pointList in the output text box
	def onDisplayPtListClick(self):
		if (self.ready == False):
			tkMessageBox.showwarning("Error", "No graph generated please generate a graph first.")
			return
		self.textBox.delete(1.0,'end')
		self.textBox.insert(1.0,"Point List:\n")
		
		self.chor.generatedPtList = [n for n in self.chor.generatedPtList if n is not None]
		for i in self.chor.generatedPtList:						
			self.textBox.insert('end', (i, self.chor.ptMap[i]))
			self.textBox.insert('end',"\n")
			
		##self.textBox.insert('end', str(self.chor.displayPtList()))		
	
	### generates the a new graph based on the input ranges
	def onGenerateGraphClick(self):
		## error checking for inputs block
		
		numVertices = self.verticeEntry.get()
		if isStrInt(numVertices):
			numVertices = int (self.verticeEntry.get())
			if (numVertices < 0):
				tkMessageBox.showwarning("Error","Entry for vertices is less than 0.")
				return
		else:
			tkMessageBox.showwarning("Error","Entry for vertices is not an integer.")
			return
		
		numEdges = self.edgeEntry.get()
		if isStrInt(numEdges):
			numEdges = int (self.edgeEntry.get())
			if (numEdges < 0):
				tkMessageBox.showwarning("Error","Entry for edges is less than 0.")
				return
			if (numEdges < numVertices-1):
				tkMessageBox.showwarning("Error","Entry for edges must be enough for a tree structure. Needs %d." %(numVertices-1))
				return
			if (numEdges > (numVertices *(numVertices-1))/2)  :
				tkMessageBox.showwarning("Error","Entry for edges provided is more than a complete graph." )
				return
		else:
			tkMessageBox.showwarning("Error","Entry for edges is not an integer.")
			return
		
		numRangeLow = self.numRangeLowEntry.get()
		if isStrInt(numRangeLow):
			numRangeLow = int (self.numRangeLowEntry.get())
			if (numRangeLow < 0):
				tkMessageBox.showwarning("Error","Entry for lower bound of point is less than 0.")
				return
		else:
			tkMessageBox.showwarning("Error","Entry for lower bound of point is not an integer.")
			return
			
		numRangeHigh = self.numRangeHighEntry.get()
		if isStrInt(numRangeHigh):
			numRangeHigh = int (self.numRangeHighEntry.get())
			if (numRangeHigh < 0):
				tkMessageBox.showwarning("Error","Entry for upper bound of point is less than 0.")
				return
			if (numRangeHigh < numRangeLow):
				tkMessageBox.showwarning("Error","Entry for upper bound of point is less than lower bound.")
				return
		else:
			tkMessageBox.showwarning("Error","Entry for upper bound of point is not an integer.")
			return			
		##end of error checking from inputs
		
		self.ready = True
		self.tree = Tree()
		self.chor = ChordalSparse()
				
		li=[]
		for i in range(0, numVertices):
			li.append(i)
		random.shuffle(li)
		
		for i in li:
			self.tree.insertNode(self.tree.getRoot(), li[i])
		self.chor.convertFromTree(self.tree)
		self.chor.setupPoints(numRangeLow, numRangeHigh)
		
		if (numEdges>(numVertices-1)):
			self.chor.addRanEdges(numEdges-(numVertices-1))
		return None

	### adds edges to the current graph based on input
	def onClickAddEdges(self):
		edges = self.AddEdgesEntry.get()
		if (self.ready == False):
			tkMessageBox.showwarning("Error", "No graph generated please generate a graph first")
			return
		
		if isStrInt(edges):
			edges = int (self.AddEdgesEntry.get())
			max = ((self.chor.vertex*(self.chor.vertex-1)/2)-(self.chor.vertex-1))
			if (edges < 0):
				tkMessageBox.showwarning("Error","Entry for add edges is less than 0.")
				return
			if (edges > max):
				tkMessageBox.showwarning("Error","The max edges you can add is " +str(max))
				return
		else:
			tkMessageBox.showwarning("Error","Entry for add edges is not an integer.")
			return
		self.chor.addRanEdges(edges)

	###displays the current graph representation in a new window
	def onDisplayGraph(self):
		if (self.ready == False):
			tkMessageBox.showwarning("Error", "No graph generated please generate a graph first")
			return
			
		numRangeLow = self.numRangeLowEntry.get()
		if isStrInt(numRangeLow):
			numRangeLow = int (self.numRangeLowEntry.get())
			if (numRangeLow < 0):
				tkMessageBox.showwarning("Error","Entry for lower bound of point is less than 0.")
				return
		else:
			tkMessageBox.showwarning("Error","Entry for lower bound of point is not an integer.")
			return
			
		numRangeHigh = self.numRangeHighEntry.get()
		if isStrInt(numRangeHigh):
			numRangeHigh = int (self.numRangeHighEntry.get())
			if (numRangeHigh < 0):
				tkMessageBox.showwarning("Error","Entry for upper bound of point is less than 0.")
				return
			if (numRangeHigh < numRangeLow):
				tkMessageBox.showwarning("Error","Entry for upper bound of point is less than lower bound.")
				return
		else:
			tkMessageBox.showwarning("Error","Entry for upper bound of point is not an integer.")
			return		
		
		self.chor.createDisplay(800,600,numRangeLow,numRangeHigh)
		
##resolution presets
resWidth = 800
resHeight = 600

if __name__ == "__main__":
	app = gui_tk(None)
	app.geometry('600x400')#window size
	app.mainloop()