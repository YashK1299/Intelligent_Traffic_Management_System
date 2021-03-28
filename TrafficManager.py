#import future
from statemachine import StateMachine, State
import schedule
import time
import numpy as np
from random import seed
from random import randint
from ImageProcessing import *
#from gui import *
from InputData import *
from collections import Counter
from math import ceil
import threading
import thread
#import multiprocessing
#Rate = 1 car per sec
#rate depends on lane characteristics(width, construction work going on, etc.)
#fstart = time.time()
#Defining Traffic Light as a State Machine

class TrafficLightMachine(StateMachine):
	def __init__(self, parentImage, parentFrame):
		super(TrafficLightMachine, self).__init__(self)
		self.parentImage = parentImage
		self.parentFrame = parentFrame
		self.traffic_density = 0.0
		self.on_time = 0.0
		#self.prev = 0.5
		#self.rate = 1.0

	green = State('Green')
	yellow = State('Yellow')
	intergreen = State('Intergreen')
	red = State('Red', initial= 'True')
	slowdown = green.to(yellow)
	stop = yellow.to(red)
	start = red.to(intergreen)
	go = intergreen.to(green)
	set = green.to(red)
		
	def on_slowdown(self):
		#print("Yellow")
		self.parentImage.configure(image = self.parentFrame.originalFrame.imgfile[1])
		self.parentFrame.update_idletasks()

	def on_start(self):
		#print("Yellow")
		self.parentImage.configure(image = self.parentFrame.originalFrame.imgfile[1])
		self.parentFrame.update_idletasks()

	def on_stop(self):
		#print("Red")
		self.parentImage.configure(image = self.parentFrame.originalFrame.imgfile[0])
		self.parentFrame.update_idletasks()

	def on_go(self):
		#print("Green")
		self.parentImage.configure(image = self.parentFrame.originalFrame.imgfile[2])
		self.parentFrame.update_idletasks()

class TrafficManager(TrafficLightMachine):
	def __init__(self, parentFrame):
		#super(TrafficLightMachine, self).__init__(self)
		self.parentFrame = parentFrame
		#Creating Traffic Junction
		self.tl = []
		self.laneImage = self.parentFrame.laneSignal
		self.iter = self.parentFrame.originalFrame.iter
		for i in range(4): self.tl.append(TrafficLightMachine(self.laneImage[i], self.parentFrame))
		#self.computeSaturationFlow()
		#self.trafficManager(self.parentFrame.originalFrame.laneView)

	def computeSaturationFlow(self):
		self.laneWidth = [self.parentFrame.originalFrame.specifications['Width of Lane ' + str(i)] for i in range(1, 5)]
		self.uniqueSaturationFlow = np.zeros(4)
		self.saturationFlow = np.zeros(4)
		for i in range(4):
			if float(self.laneWidth[i]) < 7.0: self.uniqueSaturationFlow[i] = 630
			elif float(self.laneWidth[i]) <= 10.5: self.uniqueSaturationFlow[i] = 1140 - 60 * self.laneWidth[i]
			elif float(self.laneWidth[i]) > 10.5: self.uniqueSaturationFlow[i] = 500
			self.saturationFlow[i] = self.uniqueSaturationFlow[i] * self.laneWidth[i] / 30
			self.parentFrame.laneInfoDict[i]['Saturation Flow = '] = self.saturationFlow[i]
		#print(self.saturationFlow)

		"""tl2 = TrafficLightMachine()
		tl3 = TrafficLightMachine()
		tl4 = TrafficLightMachine()
		"""	
		"""
		print ( "Depending on road conditions, enter rate of traffic in each lane")
		tl1.rate = float(input("Enter rate of lane 1:"))
		tl2.rate = float(input("Enter rate of lane 2:"))
		tl3.rate = float(input("Enter rate of lane 3:"))
		tl4.rate = float(input("Enter rate of lane 4:"))
		print(type(tl1.rate))
		#Scheduling jobs
		"""

	def update_traffic_density(self, j):
		#global tot_traffic
		for i in range(4):
			self.tl[i].traffic_density = float(j[i]) #Image processing output
		"""#print(tl1.traffic_density)
		self.tl2.traffic_density = float(j2) #Image processing output
		#print(tl2.traffic_density)
		self.tl3.traffic_density = float(j3) #Image processing output
		#print(tl3.traffic_density)
		self.tl4.traffic_density = float(j4) #Image processing output"""
		#st = ''
		#for i in range(4):
		#	st += 
		#print("Traffic in each lane: " + ', '.join([str(i.traffic_density) for i in self.tl]) +";")#+ str(self.tl2.traffic_density) +", "+ str(self.tl3.traffic_density) +", "+  str(self.tl4.traffic_density) +";")
		tot_traffic = sum(list(i.traffic_density for i in self.tl))# + self.tl2.traffic_density + self.tl3.traffic_density + self.tl4.traffic_density
		#print("Total traffic in all lanes: " + str(tot_traffic))
	
	"""def compute_traffic_density(self):
		#print(tot_traffic)
		#self.tl[0].traffic_density /= tot_traffic
		for i in range(4):
			self.tl[i].traffic_density = self.tl[i].traffic_density
		#print(self.tl1.traffic_density)
		self.tl2.traffic_density /= tot_traffic
		self.tl3.traffic_density /= tot_traffic
		self.tl4.traffic_density /= tot_traffic
"""

	def compute_on_time(self):
		#formula for calculating on time
		self.IntergreenPeriod = self.parentFrame.originalFrame.specifications['Intergreen Period']
		self.amberPeriod = self.parentFrame.originalFrame.specifications['Amber Period']
		self.xPhaseSignal = self.parentFrame.originalFrame.specifications['Number of Phases']
		self.initialDelay = self.parentFrame.originalFrame.specifications['Initial Delay']
		self.minOnTime = self.parentFrame.originalFrame.specifications['Minimum On Time']
		#self.xminTime = 0.0
		self.maxCycleTime = self.parentFrame.originalFrame.specifications['Maximum Cycle Time']
		self.totalLostTime = self.xPhaseSignal * (self.IntergreenPeriod - self.amberPeriod + self.amberPeriod + self.initialDelay)
		self.flowRatio = np.zeros(4)

		for i in range(4): self.flowRatio[i] = self.trafficFlow[i] / self.saturationFlow[i]
		self.totalFlowRatio = sum(self.flowRatio)
		if self.totalFlowRatio < 1 and (1.5 * self.totalLostTime + 5) / (1 - self.totalFlowRatio) < self.maxCycleTime:
			self.optimumCycleTime = (1.5 * self.totalLostTime + 5) / (1 - self.totalFlowRatio)
		else: self.optimumCycleTime = self.maxCycleTime
		self.optimumCycleTime = 5 * ceil(self.optimumCycleTime/5)
		#print(self.optimumCycleTime)
		temp = 0
		for i in range(4):
			self.tl[i].on_time = (self.flowRatio[i] / self.totalFlowRatio) * (self.optimumCycleTime - self.totalLostTime)
			self.tl[i].on_time = round(self.tl[i].on_time)
			if self.tl[i].on_time < self.minOnTime:
				self.optimumCycleTime = self.optimumCycleTime + self.minOnTime - self.tl[i].on_time
				temp = temp + self.minOnTime - self.tl[i].on_time
				self.tl[i].on_time = self.minOnTime
				"""for k in range(i - 1):
					self.tl[i].on_time = (flowRatio[i] / totalFlowRatio) * (self.optimumCycleTime - totalLostTime)
					self.tl[i].on_time = round(self.tl[i].on_time)	
					if self.tl[i].on_time < self.minOnTime:
						self.tl[i].on_time = self.minOnTime"""
		self.optimumCycleTime = self.optimumCycleTime if self.optimumCycleTime < self.maxCycleTime else self.maxCycleTime
		self.optimumCycleTime = 5 * ceil(self.optimumCycleTime/5)
		for i in range(4):		
			if self.tl[i].on_time != 10:
				self.tl[i].on_time = (self.flowRatio[i] / self.totalFlowRatio) * (self.optimumCycleTime - self.totalLostTime - temp)
				self.tl[i].on_time = round(self.tl[i].on_time)
			self.parentFrame.laneInfoDict[i]['On Time = '] = self.tl[i].on_time
		#print(self.optimumCycleTime)
		#print("Traffic Cycle Time: " + str(self.optimumCycleTime))

			#self.tl[i].on_time = (tot_time * self.tl[i].traffic_density / tot_traffic) / self.tl[i].rate
			#print(self.tl[i].on_time, self.tl[i].rate)
			#if self.tl[i].traffic_density / self.tl[i].rate > self.tl[i].on_time :
				#self.tl1.on_time =  (self.tl1.traffic_density * tot_traffic / self.tl1.rate) + 5
				#self.tl[i].on_time += 5
		"""#print(self.tl1.on_time)
		self.tl2.on_time = (tot_time * self.tl2.traffic_density) / self.tl2.rate
		if self.tl2.traffic_density * tot_traffic / self.tl2.rate > self.tl2.on_time :
			self.tl2.on_time += 5
			#self.tl2.on_time =  (self.tl2.traffic_density * tot_traffic / self.tl2.rate) + 5	
		#print(self.tl2.on_time)
		self.tl3.on_time = (tot_time * self.tl3.traffic_density) / self.tl3.rate
		if self.tl3.traffic_density * tot_traffic / self.tl3.rate > self.tl3.on_time :
			self.tl3.on_time += 5
			#self.tl3.on_time =  (self.tl3.traffic_density * tot_traffic / self.tl3.rate) + 5
		#print(self.tl3.on_time)
		self.tl4.on_time = (tot_time * self.tl4.traffic_density) / self.tl4.rate 
		if self.tl4.traffic_density * tot_traffic / self.tl4.rate > self.tl4.on_time :
			self.tl1.on_time += 5
			#self.tl4.on_time =  (self.tl4.traffic_density * tot_traffic / self.tl4.rate) + 5
		"""	
		#print("On time of each lane: " + (', '.join([str(float(i.on_time)) for i in self.tl])) +";")#+ str(self.tl2.on_time) +", "+ str(self.tl3.on_time) +", "+ str(self.tl4.on_time) + ";")

	def trafficFlowManager(self):
		for i in range(4):
			#print("_________Signal " + str(i+1) + "_________")
			#print("Red")
			self.tl[i].run('start')
			time.sleep(self.IntergreenPeriod)
			self.tl[i].run('go')
			time.sleep(self.tl[i].on_time)
			self.tl[i].run('slowdown')
			time.sleep(self.amberPeriod)
			self.tl[i].run('stop')
		time.sleep(5)
		"""
		print("_________Signal 2________")
		self.tl2.run('go')
		time.sleep(self.tl2.on_time)
		self.tl2.run('slowdown')
		time.sleep(1)
		self.tl2.run('stop')
		print("_________Signal 3________")
		self.tl3.run('go')
		time.sleep(self.tl3.on_time)
		self.tl3.run('slowdown')
		time.sleep(1)
		self.tl3.run('stop')
		print("_________Signal 4________")
		self.tl4.run('go')
		time.sleep(self.tl4.on_time)
		self.tl4.run('slowdown')
		time.sleep(1)
		self.tl4.run('stop')
		"""

	#Scheduling Events
	#schedule.every((tot_time/60)).minutes.do(update_traffic_density)
	#schedule.every((tot_time+2/60)).minutes.do(compute_traffic_density)
	#schedule.every((tot_time+4)/60).minutes.do(compute_on_time)
	#schedule.every((tot_time+6)/60).minutes.do(trafficFlow)
	
	#tot_time = 240
	"""def ui(self, itms):
		trafficSignal = tk.Toplevel(itms)
		#trafficSignal = tk.Toplevel(itms)
		trafficSignalPanedWindow = tk.PanedWindow(trafficSignal)
		trafficSignalPanedWindow.pack()
		subPanedWindowLeft = tk.PanedWindow(trafficSignalPanedWindow, orient = VERTICAL)
		imgfile = ImageTk.PhotoImage(Image.open(filename), master = trafficSignalPanedWindow)
		lane1Signal = tk.Label(subPanedWindowLeft, image = imgfile)
		subPanedWindowLeft.add(lane1Signal)

		imgfile = ImageTk.PhotoImage(Image.open(filename), master = trafficSignalPanedWindow)
		lane2Signal = tk.Label(subPanedWindowLeft, image = imgfile)
		subPanedWindowLeft.add(lane2Signal)
		trafficSignalPanedWindow.add(subPanedWindowLeft)

		subPanedWindowRight = tk.PanedWindow(trafficSignalPanedWindow, orient = VERTICAL)
		imgfile = ImageTk.PhotoImage(Image.open(filename), master = trafficSignalPanedWindow)
		lane3Signal = tk.Label(subPanedWindowRight, image = imgfile)
		subPanedWindowRight.add(lane3Signal)

		imgfile = ImageTk.PhotoImage(Image.open(filename), master = trafficSignalPanedWindow)
		lane4Signal = tk.Label(subPanedWindowRight, image = imgfile)
		subPanedWindowRight.add(lane4Signal)
		trafficSignalPanedWindow.add(subPanedWindowRight)
"""
	def imageProcessingThread(self, i, ID):
		#start = time.time()
		trafficDensityObject = TrafficDensity()
		img = "input/" + str(i) + ".png"
		self.j.append(trafficDensityObject.trafficDensity(img, i))
		self.trafficType.append(Counter(trafficDensityObject.trafficType()))
		self.trafficFlow[ID] = sum(self.trafficType[ID][k] * self.trafficPCU[k] for k in self.trafficType[ID])
		self.parentFrame.laneInfoDict[ID]['Number of Vehicles = '] = self.j[ID]
		self.parentFrame.laneInfoDict[ID]['Traffic Flow = '] = self.trafficFlow[ID]		
		#end = time.time()
		#print("Thread " + str(ID) + ": " + str(end - start))

	def trafficManager(self, b):
		#print ("Depending on road conditions, enter rate of traffic in each lane")
		#print(list(i.traffic_density for i in self.tl))
		#for i in range(4):
			#print(self.parentFrame.originalFrame.laneRate[i])
			#self.tl[i].rate = float(self.parentFrame.originalFrame.laneRate[i].get())
			#self.tl[i].rate = float(input("Enter rate of lane 1:"))
		"""self.tl2.rate = float(input("Enter rate of lane 2:"))
		self.tl3.rate = float(input("Enter rate of lane 3:"))
		self.tl4.rate = float(input("Enter rate of lane 4:"))"""
		#self.tl1.rate, self.tl2.rate, self.tl3.rate, self.tl4.rate = tlrateq
		#start = time.time()
		LABELS = open('yolo-coco/coco.names').read().strip().split("\n")
		self.trafficPCU = dict.fromkeys(LABELS, 0)
		self.trafficPCU.update({'car' : 1, 'motorbike' : 0.33, 'bus' : 2.25, 'truck' : 1.75})
		self.j = []
		self.parentFrame.originalFrame.laneView = b
		self.trafficType = []
		self.trafficFlow = np.zeros(4)
		a = 0
		threads = []
		#start = time.time()
		for i in b:
			t = threading.Thread(target=self.imageProcessingThread, args=(i, a, ))
			#t = multiprocessing.Process(target=self.imageProcessingThread, args=(i, a, ))
			threads.append(t)
			t.start()
		for x in threads:
			x.join()
			"""try:
				thread.start_new_thread( self.imageProcessingThread, (i, a, ) )
				a = a + 1;
			except:
				print "Error: unable to start thread"
			"""
			"""img = "input/" + str(i) + ".png"
			j.append(trafficDensityObject.trafficDensity(img, i))
			self.trafficType.append(Counter(trafficDensityObject.trafficType()))"""
			#img = "output/" + str(i) + ".png"
			#image = cv2.imread(img)
			#cv2.imshow(("image" + str(i) + " Traffic Density: " + str(j[a])),image)
			#a += 1
		#end = time.time()
		#print(end - start)
		"""for i in range(4):
			#print(b, self.trafficFlow[i], trafficPCU)
			self.trafficFlow[i] = sum(self.trafficType[i][k] * trafficPCU[k] for k in self.trafficType[i])
			self.parentFrame.laneInfoDict[i]['Number of Vehicles = '] = self.j[i]
			self.parentFrame.laneInfoDict[i]['Traffic Flow = '] = self.trafficFlow[i]
		"""
		#if cv2.waitKey(0) & 0xFF == ord('q'):
		#	cv2.destroyAllWindows()
		#print(type(self.tl1.rate))
		#Scheduling jobs
		#end = time.time()
		#print("[INFO] Code took {:.6f} seconds".format(end - start))
		
		self.update_traffic_density(self.j)
		#self.compute_traffic_density()
		self.computeSaturationFlow()
		self.compute_on_time()
		for k in range(4):
			#print(self.parentFrame.laneInfoDict[k].keys())
			for i in range(len(self.parentFrame.laneInfoDict[k].keys())):
				text = self.parentFrame.laneInfoDict[k].keys()[i] + str(self.parentFrame.laneInfoDict[k][self.parentFrame.laneInfoDict[k].keys()[i]])
				self.parentFrame.laneInfoLabel[k][i].configure(text = text)
		self.parentFrame.update_idletasks()
		#self.trafficFlowManager()
		#end = time.time()
		#print("[INFO] Code took {:.6f} seconds".format(end - start))

class TrafficManagerDataset():
	def __init__(self, parentFrame, parent):
		self.parentFrame = parentFrame
		self.parent = parent
		#self.computeSaturationFlow()
		#self.trafficManagerDataset(self.parentFrame.originalFrame.laneView)

	def computeSaturationFlow(self):
		self.laneWidth = [self.parentFrame.originalFrame.specifications['Width of Lane ' + str(i)] for i in range(1, 5)]
		self.uniqueSaturationFlow = np.zeros(4)
		self.saturationFlow = np.zeros(4)
		for i in range(4):
			if float(self.laneWidth[i]) < 7.0: self.uniqueSaturationFlow[i] = 630
			elif float(self.laneWidth[i]) <= 10.5: self.uniqueSaturationFlow[i] = 1140 - 60 * float(self.laneWidth[i])
			elif float(self.laneWidth[i]) > 10.5: self.uniqueSaturationFlow[i] = 500
			self.saturationFlow[i] = self.uniqueSaturationFlow[i] * float(self.laneWidth[i]) / 30
			#self.parentFrame.laneInfoDict[i]['Saturation Flow = '] = self.saturationFlow[i]
			self.parent.data['Lane ' + str(i + 1) + ' Saturation Flow'].append(self.saturationFlow[i])
		#print(self.saturationFlow)

	def compute_on_time(self):
		#formula for calculating on time
		self.IntergreenPeriod = self.parentFrame.originalFrame.specifications['Intergreen Period']
		self.amberPeriod = self.parentFrame.originalFrame.specifications['Amber Period']
		self.xPhaseSignal = self.parentFrame.originalFrame.specifications['Number of Phases']
		self.initialDelay = self.parentFrame.originalFrame.specifications['Initial Delay']
		self.minOnTime = self.parentFrame.originalFrame.specifications['Minimum On Time']
		self.maxCycleTime = self.parentFrame.originalFrame.specifications['Maximum Cycle Time']
		self.totalLostTime = self.xPhaseSignal * (self.IntergreenPeriod - self.amberPeriod + self.amberPeriod + self.initialDelay)
		self.parent.data['Total Time Lost'].append(self.totalLostTime)
		self.flowRatio = np.zeros(4)
		for i in range(4): 
			self.flowRatio[i] = self.trafficFlow[i] / self.saturationFlow[i]
			self.parent.data['Lane ' + str(i + 1) + ' Flow Ratio'].append(self.flowRatio[i])
		self.totalFlowRatio = sum(self.flowRatio)
		self.parent.data['Total Flow Ratio'].append(self.totalFlowRatio)
		if self.totalFlowRatio < 1 and (1.5 * self.totalLostTime + 5) / (1 - self.totalFlowRatio) < self.maxCycleTime:
			self.optimumCycleTime = (1.5 * self.totalLostTime + 5) / (1 - self.totalFlowRatio)
		else: self.optimumCycleTime = self.maxCycleTime
		self.optimumCycleTime = 5 * ceil(self.optimumCycleTime/5)
		temp = 0
		self.onTime = np.zeros(4)
		#print(self.onTime)
		for i in range(4):
			self.onTime[i] = (self.flowRatio[i] / self.totalFlowRatio) * (self.optimumCycleTime - self.totalLostTime)
			self.onTime[i] = round(self.onTime[i])
			#print(self.onTime)
			if self.onTime[i] < self.minOnTime:
				self.optimumCycleTime = self.optimumCycleTime + self.minOnTime - self.onTime[i]
				temp = temp + self.minOnTime - self.onTime[i]
				self.onTime[i] = self.minOnTime
			#print(self.onTime)
		self.optimumCycleTime = self.optimumCycleTime if self.optimumCycleTime < self.maxCycleTime else self.maxCycleTime
		self.optimumCycleTime = 5 * ceil(self.optimumCycleTime/5)
		self.parent.data['Optimum Cycle Time'].append(self.optimumCycleTime)
		for i in range(4):		
			if self.onTime[i] > 1.4*self.minOnTime:
				self.onTime[i] = (self.flowRatio[i] / self.totalFlowRatio) * (self.optimumCycleTime - self.totalLostTime - temp)
				self.onTime[i] = round(self.onTime[i])
			#print(self.onTime)
			self.parent.data['Lane ' + str(i + 1) + ' On Time'].append(self.onTime[i])
		#print(self.minOnTime)
		
	def cycleParameters(self, b):
		LABELS = open('yolo-coco/coco.names').read().strip().split("\n")
		trafficPCU = dict.fromkeys(LABELS, 0)
		trafficPCU.update({'car' : 1, 'motorbike' : 0.33, 'bus' : 2.25, 'truck' : 1.75})
		j = []
		trafficType = []
		self.trafficFlow = np.zeros(4)
		for i in range(4):
			img = "input/" + str(b[i]) + ".png"
			j.append(getData(b[i])[0])
			if type(getData(b[i])[1]) != float:
				trafficType.append(Counter((getData(b[i])[1]).split(':')))
			else: trafficType.append(Counter([]))
			#print(j[0], (getData(b[i])[1]).split(':'))
			self.trafficFlow[i] = sum(trafficType[i][k] * trafficPCU[k] for k in trafficType[i])
			self.parent.data['Number of Vehicles in Lane ' + str(i + 1)].append(j[i])
			self.parent.data['Lane ' + str(i + 1) + ' Traffic Flow'].append(self.trafficFlow[i])
		self.computeSaturationFlow()
		self.compute_on_time()

#a = TrafficManager()
#a.trafficManager([5, 6, 4, 7])
#main.coderun()
