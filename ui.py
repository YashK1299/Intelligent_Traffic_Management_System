from statemachine import StateMachine, State
import schedule 
import time
from Tkinter import *
import Tkinter as tk
#from tkinter 
import ttk
import tkFileDialog as filedialog
import numpy as np
from PIL import ImageTk, Image
from random import sample
from random import randint
#from pubsub import pub
#import threading
from collections import OrderedDict
import tkFont
from ImageProcessing import *
from TrafficManager import *
from InputData import *
import pandas as pd
from pandastable import Table, TableModel
#tlrate = [10.0, 10.0, 10.0, 10.0]
#tlrate[:] = [x / 4 for x in tlrate]
#order = sample(1,66,4)


#itms.geometry("280x175")
#directory = '/home/yash/workspace-ITMS/BEProject/input'
#label = [None, None, None, None]
#entry = [None, None, None, None]

class SpecificationsFrame(tk.Toplevel):
	def __init__(self, original):
		"""Constructor"""
		self.originalFrame = original
		tk.Toplevel.__init__(self)
		#self.geometry("400x200")
		self.title("Traffic Parameter Specifications")
		self.specificationsframe()

	def close(self):
		self.destroy()
		self.originalFrame.show()

	def changeValues(self):
		for i in range(len(self.originalFrame.specifications)):
			#self.specificationsVariable[i].set(float(self.entry[i].get()))
			self.originalFrame.specificationsVariable[i].set(self.specificationsVariable[i].get())
		j = 0
		for i in self.originalFrame.specifications.keys():
			self.originalFrame.specifications[i] = float((self.specificationsVariable[j].get()))
			j += 1
		#print(self.originalFrame.specifications)
		"""tlrate[1] = float(self.entry[1].get())
		self.originalFrame.variable2.configure(text = 'Lane 2 rate: ' + str(tlrate[1]))
		tlrate[2] = float(self.entry[2].get())
		self.originalFrame.variable3.configure(text = 'Lane 3 rate: ' + str(tlrate[2]))
		tlrate[3] = float(self.entry[3].get())
		self.originalFrame.variable4.configure(text = 'Lane 4 rate: ' + str(tlrate[3]))"""
		self.close()
		#print(tlrate)

	def specificationsframe(self):
		self.frame = []
		self.label = []
		self.entry = []
		self.specificationsVariable = []
		for i in range(len(self.originalFrame.specifications)):
			self.specificationsKey = self.originalFrame.specifications.keys()[i]
			self.frame.append(tk.Frame(self))
			self.label.append(tk.Label(self.frame[i], text = self.specificationsKey + ':', width = 20, anchor = W))
			self.label[i].pack(side = LEFT, fill = BOTH, expand = 1)
			self.specificationsVariable.append(StringVar())
			self.entry.append(tk.Entry(self.frame[i], textvariable = self.specificationsVariable[i]))
			self.specificationsVariable[i].set(self.originalFrame.specifications[self.specificationsKey])
			#self.entry[i].insert('end', int(tlrate[i]))
			self.entry[i].pack(side = LEFT, fill = BOTH, expand = 1)
			self.frame[i].pack()
		okButton = tk.Button(self, text='OK', width=10, command = self.changeValues)
		okButton.pack()
		self.protocol("WM_DELETE_WINDOW", self.originalFrame.root.destroy)
		#laneRateToplevel.mainloop()

class ImageProcessingFrame(tk.Toplevel):
	def __init__(self, original):
		"""Constructor"""
		self.originalFrame = original
		tk.Toplevel.__init__(self)
		#self.geometry("500x500")
		self.title("Image Processing Algorithm Output")
		self.td = TrafficDensity()
		self.imageProcessingFrame()

	def close(self):
		self.destroy()
		self.originalFrame.show()
	
	#def showimage(self, img):
		
	def imageProcessingFrame(self):
		self.frame1 = tk.Frame(self)
		self.frame1.pack(fill = X, expand = 1)
		self.imgId = randint(1,65)
		self.img = self.originalFrame.inputFolder.get() + '/' + str(self.imgId) + ".png"
		self.inputImage = tk.PhotoImage(file = self.img)
		self.loadGif = tk.PhotoImage(file = 'images/load.png')
		#print(self.imgId)
		self.label1 = tk.Label(self.frame1, text = 'Image File: ' + str(self.imgId) + ".png")
		self.label1.pack(side = LEFT,expand = 1)

		self.frame2 = tk.Frame(self)
		self.frame2.pack(fill = BOTH, expand = 1)
		self.frame3 = tk.Frame(self.frame2)
		self.frame3.pack(side = LEFT, fill = BOTH, expand = 1)
		self.inputImageLabel = tk.Label(self.frame3, image = self.inputImage)
		self.inputImageLabel.pack()
		self.frame4 = tk.Frame(self.frame2)
		self.frame4.pack(side = LEFT, fill = BOTH, expand = 1)
		self.outputImageLabel = tk.Label(self.frame4, image = self.loadGif)
		self.outputImageLabel.pack()
		self.label2 = tk.Label(self.frame1, text = 'Number of vehicles detected: ')
		self.label2.pack(side = LEFT,expand = 1)

		self.frame5 = tk.Frame(self)
		self.frame5.pack(fill = BOTH, expand = 1)
		closeButton = tk.Button(self.frame5, text='Back', width=15, command = self.close)
		closeButton.pack(side = BOTTOM, expand = 1)
		self.protocol("WM_DELETE_WINDOW", self.originalFrame.root.destroy)
		self.update_idletasks()
		self.testImage()
		#laneRateToplevel.mainloop()
	
	def testImage(self):
		self.label2.configure(text = 'Number of vehicles detected: ' + str(self.td.trafficDensity(self.img, self.imgId)))
		self.outputImage = tk.PhotoImage(file = self.originalFrame.outputFolder.get() + '/' + str(self.imgId) + ".png")
		self.outputImageLabel.configure(image = self.outputImage)
		self.update_idletasks()

class RoadViewFrame(tk.Toplevel):
	def __init__(self, original):
		"""Constructor"""
		self.originalFrame = original
		tk.Toplevel.__init__(self)
		#self.geometry("500x500")
		self.title("Road View")
		self.td = TrafficDensity()
		self.roadViewFrame()

	def close(self):
		self.destroy()
		self.originalFrame.show()

	def roadViewFrame(self):
		traffic = []
		for i in range(4):
			traffic.append(self.td.trafficDensity(self.originalFrame.inputFolder.get() + '/' + str(self.originalFrame.laneView[i]) + ".png", self.originalFrame.laneView[i]))
		roadViewPanedWindow = tk.PanedWindow(self, height = 625, width = 620, orient = VERTICAL)
		roadViewPanedWindow.pack()
		subPanedWindowLeft = tk.PanedWindow(roadViewPanedWindow, height = 312, orient = HORIZONTAL)
		lane1Frame = tk.Frame(subPanedWindowLeft)
		lane1 = tk.Label(lane1Frame, text = 'Number of Cars in Lane 1 = ' + str(traffic[0]), relief = RIDGE)
		lane1.pack(fill = BOTH, expand = 1)
		lane1Image = tk.PhotoImage(file = self.originalFrame.outputFolder.get() + '/' + str(self.originalFrame.laneView[0]) + ".png")
		lane1Signal = tk.Label(lane1Frame, image = lane1Image, relief = RIDGE)
		lane1Signal.pack(fill = BOTH, expand = 1)
		subPanedWindowLeft.add(lane1Frame)

		lane2Frame = tk.Frame(subPanedWindowLeft)
		lane2 = tk.Label(lane2Frame, text = 'Number of Cars in Lane 2 = ' + str(traffic[1]), relief = RIDGE)
		lane2.pack(fill = BOTH, expand = 1)
		lane2Image = tk.PhotoImage(file = self.originalFrame.outputFolder.get() + '/' + str(self.originalFrame.laneView[1]) + ".png")
		lane2Signal = tk.Label(lane2Frame, image = lane2Image, relief = RIDGE)
		lane2Signal.pack(fill = BOTH, expand = 1)
		subPanedWindowLeft.add(lane2Frame)
		#subPanedWindowLeft.add(lane2Frame)
		roadViewPanedWindow.add(subPanedWindowLeft)

		subPanedWindowRight = tk.PanedWindow(roadViewPanedWindow, height = 312, orient = HORIZONTAL)
		lane3Frame = tk.Frame(subPanedWindowRight)
		lane3 = tk.Label(lane3Frame, text = 'Number of Cars in Lane 3 = ' + str(traffic[2]), relief = RIDGE)
		lane3.pack(fill = BOTH, expand = 1)
		lane3Image = tk.PhotoImage(file = self.originalFrame.outputFolder.get() + '/' + str(self.originalFrame.laneView[2]) + ".png")
		lane3Signal = tk.Label(lane3Frame, image = lane3Image, relief = RIDGE)
		lane3Signal.pack(fill = BOTH, expand = 1)
		subPanedWindowRight.add(lane3Frame)

		lane4Frame = tk.Frame(subPanedWindowRight)
		lane4 = tk.Label(lane4Frame, text = 'Number of Cars in Lane 4 = ' + str(traffic[3]), relief = RIDGE)
		lane4.pack(fill = BOTH, expand = 1)
		lane4Image = tk.PhotoImage(file = self.originalFrame.outputFolder.get() + '/' + str(self.originalFrame.laneView[3]) + ".png")
		lane4Signal = tk.Label(lane4Frame, image = lane4Image, relief = RIDGE)
		lane4Signal.pack(fill = BOTH, expand = 1)
		subPanedWindowRight.add(lane4Frame)
		#subPanedWindowRight.add(lane4Frame)
		roadViewPanedWindow.add(subPanedWindowRight)
		#roadView.after(int(tim*1000), trafficSignal.destroy)
		closeButton = tk.Button(self, text='Back', width=15, command = self.close)
		closeButton.pack(side = BOTTOM, expand = 1)
		self.protocol("WM_DELETE_WINDOW", self.originalFrame.root.destroy)
		#self.originalFrame.root.wait_window(self)
		self.wait_window()
		#startButton = tk.Button(trafficSignalPanedWindow, text = 'START', command = coderun)
		#trafficSignalPanedWindow.add(startButton)
		#trafficSignal.destroy()

class ManageTrafficFrame(tk.Toplevel):
	def __init__(self, original):
		"""Constructor"""
		self.originalFrame = original
		tk.Toplevel.__init__(self)
		#self.geometry("500x500")
		self.title("Lane View")
		self.originalFrame.laneView = sample(range(1,66), 4)
		self.iter = self.originalFrame.specifications['Number of Iterations']
		
		self.animationFrame()
		#self.manageTraffic()
		#threadLock = threading.Lock()
		#self.thread1 = threading.Thread(target = self.animationFrame(), args(threadLock, ))
		#self.thread2 = threading.Thread(target = manageTraffic(), args(threadLock, ))
		#self.lane1Signal.image = self.originalFrame.imgfile[0]
		#self.lane1Signal.update()
		#self.manageTraffic()
	
	def close(self):
		self.destroy()
		self.originalFrame.show()
	
	def manageTraffic(self):
		for i in range(int(self.iter)):
			self.trafficManager.trafficFlowManager()
			time.sleep(1)
			if i < int(self.iter) - 1: self.trafficManager.trafficManager(sample(range(1,66), 4))
			#self.closeButton.configure(command = self.close)
			#self.mainloop()
			#time.sleep(5)
			#self.close()

	def animationFrame(self):
		#print(color, color[0])
		self.trafficSignalPanedWindow = tk.PanedWindow(self, height = 300, orient = HORIZONTAL)
		self.trafficSignalPanedWindow.pack()
		self.subPanedWindowLeft = tk.PanedWindow(self.trafficSignalPanedWindow, orient = VERTICAL)
		self.laneFrame = []
		self.trafficSignal = []
		self.lane = []
		self.laneSignal = []
		self.laneInfoFrame = []
		self.laneInfoLabel = []
		self.laneInfoDict = []
		for k in range(2):
			self.laneFrame.append(tk.Frame(self.subPanedWindowLeft, relief = RAISED))
			self.lane.append(tk.Label(self.laneFrame[k], text = 'Lane ' + str(k + 1), relief = RAISED))
			self.lane[k].pack(fill = BOTH, expand = 1)
			self.trafficSignal.append(tk.Frame(self.laneFrame[k], relief = RAISED))
			self.trafficSignal[k].pack(side = LEFT)
			img = self.originalFrame.imgfile[0]
			self.laneSignal.append(tk.Label(self.trafficSignal[k], image = img, relief = RAISED))
			self.laneSignal[k].pack()
			self.laneInfoFrame.append(tk.Frame(self.laneFrame[k], relief = RAISED))
			self.laneInfoFrame[k].pack(side = LEFT, fill = BOTH, expand = 1)
			self.laneInfoLabel.append([])
			self.laneInfoDict.append(OrderedDict([('Width of Lane ' + str(k + 1) + ' = ', self.originalFrame.specifications['Width of Lane ' + str(k + 1)]), ('Number of Vehicles = ', 0), ('Traffic Flow = ', 0), ('Saturation Flow = ', 0), ('On Time = ', 0)]))
			for i in range(len(self.laneInfoDict[k].keys())):
				text = self.laneInfoDict[k].keys()[i] + str(self.laneInfoDict[k][self.laneInfoDict[k].keys()[i]])
				self.laneInfoLabel[k].append(tk.Label(self.laneInfoFrame[k], text = text, width = 25, anchor = W))
				self.laneInfoLabel[k][i].pack(fill = BOTH, expand = 1)
			self.subPanedWindowLeft.add(self.laneFrame[k])
		
		"""
		self.lane2Frame = tk.Frame(self.subPanedWindowLeft)
		self.lane2 = tk.Label(self.lane2Frame, text = 'Lane 2', relief = RAISED)
		self.lane2.pack()
		img = self.originalFrame.imgfile[0]
		self.lane2Signal = tk.Label(self.lane2Frame, image = img, relief = RAISED)
		self.lane2Signal.pack()
		self.subPanedWindowLeft.add(self.lane2Frame)
		"""
		self.trafficSignalPanedWindow.add(self.subPanedWindowLeft)
		
		self.subPanedWindowRight = tk.PanedWindow(self.trafficSignalPanedWindow, orient = VERTICAL)
		for k in range(2, 4):
			self.laneFrame.append(tk.Frame(self.subPanedWindowRight, relief = RAISED))
			self.lane.append(tk.Label(self.laneFrame[k], text = 'Lane ' + str(k + 1), relief = RAISED))
			self.lane[k].pack(fill = BOTH, expand = 1)
			self.trafficSignal.append(tk.Frame(self.laneFrame[k], relief = RAISED))
			self.trafficSignal[k].pack(side = LEFT)
			img = self.originalFrame.imgfile[0]
			self.laneSignal.append(tk.Label(self.trafficSignal[k], image = img, relief = RAISED))
			self.laneSignal[k].pack()
			self.laneInfoFrame.append(tk.Frame(self.laneFrame[k], relief = RAISED))
			self.laneInfoFrame[k].pack(side = LEFT, fill = BOTH, expand = 1)
			self.laneInfoLabel.append([])
			self.laneInfoDict.append(OrderedDict([('Width of Lane ' + str(k + 1) + ' = ', self.originalFrame.specifications['Width of Lane ' + str(k + 1)]), ('Number of Vehicles = ', 0), ('Traffic Flow = ', 0), ('Saturation Flow = ', 0), ('On Time = ', 0)]))
			for i in range(len(self.laneInfoDict[k].keys())):
				text = self.laneInfoDict[k].keys()[i] + str(self.laneInfoDict[k][self.laneInfoDict[k].keys()[i]])
				self.laneInfoLabel[k].append(tk.Label(self.laneInfoFrame[k], text = text, width = 25, anchor = W))
				self.laneInfoLabel[k][i].pack(fill = BOTH, expand = 1)
		self.subPanedWindowRight.add(self.laneFrame[3])
		self.subPanedWindowRight.add(self.laneFrame[2])
		"""
			self.trafficSignal.append(tk.Frame(self.subPanedWindowRight))
			self.lane.append(tk.Label(self.trafficSignal[k], text = 'Lane ' + str(k + 1), relief = RAISED))
			self.lane[k].pack()
			img = self.originalFrame.imgfile[0]
			self.laneSignal.append(tk.Label(self.trafficSignal[k], image = img, relief = RAISED))
			self.laneSignal[k].pack()
			self.laneInfoFrame.append(tk.Frame(self.subPanedWindowRight))
			self.laneInfoLabel.append([])
			self.laneInfoDict.append(OrderedDict([('Width of Lane = ', self.originalFrame.specifications['Width of Lane 1']), ('Number of Vehicles = ', 0), ('Traffic Flow = ', 0), ('Saturation Flow = ', 0), ('On Time = ', 0)]))
			for i in range(len(self.laneInfoDict[k].keys())):
				text = self.laneInfoDict[k].keys()[i] + str(self.laneInfoDict[k][self.laneInfoDict[k].keys()[i]])
				self.laneInfoLabel[k].append(tk.Label(self.laneInfoFrame[k], text = text, anchor = W))
				self.laneInfoLabel[k][i].pack(fill = BOTH, expand = 1)
			self.subPanedWindowRight.add(self.trafficSignal[k])
			self.subPanedWindowRight.add(self.laneInfoFrame[k])
			"""
		"""
		self.trafficSignal[k] = tk.Frame(self.subPanedWindowRight)
		self.lane3 = tk.Label(self.lane3Frame, text = 'Lane 3', relief = RAISED)
		self.lane3.pack()
		img = self.originalFrame.imgfile[0]
		self.lane3Signal = tk.Label(self.lane3Frame, image = img, relief = RAISED)
		self.lane3Signal.pack()
		self.subPanedWindowRight.add(self.lane3Frame)

		self.lane4Frame = tk.Frame(self.subPanedWindowRight)
		self.lane4 = tk.Label(self.lane4Frame, text = 'Lane 4', relief = RAISED)
		self.lane4.pack()
		img = self.originalFrame.imgfile[0]
		self.lane4Signal = tk.Label(self.lane4Frame, image = img, relief = RAISED)
		self.lane4Signal.pack()
		self.subPanedWindowRight.add(self.lane4Frame)
		"""
		self.trafficSignalPanedWindow.add(self.subPanedWindowRight)
		self.startButton = tk.Button(self, text='Start', width=15)#, command = self.manageTraffic)
		self.startButton.pack(side = LEFT, expand = 1)
		self.closeButton = tk.Button(self, text='Back', width=15, command = self.close)
		self.closeButton.pack(side = LEFT, expand = 1)
		self.update_idletasks()
		self.trafficManager = TrafficManager(self)
		self.update_idletasks()
		self.trafficManager.trafficManager(self.originalFrame.laneView)
		self.startButton.configure(command = self.manageTraffic)
		#self.update_idletasks()
		self.protocol("WM_DELETE_WINDOW", self.originalFrame.root.destroy)
		self.update_idletasks()
    	#tk.update()
		#self.mainloop()
		#self.after(int(tim*1000), self.destroy)
		#startButton = tk.Button(trafficSignalPanedWindow, text = 'START', command = coderun)
		#trafficSignalPanedWindow.add(startButton)
		#trafficSignal.destroy()

class CreateDatasetFrame(tk.Toplevel):
	def __init__(self, original):
		"""Constructor"""
		self.originalFrame = original
		tk.Toplevel.__init__(self)
		self.geometry("900x700")
		self.title("Dataset")
		self.data = OrderedDict([('Number of Vehicles in Lane 1', []), ('Number of Vehicles in Lane 2', []), ('Number of Vehicles in Lane 3', []), ('Number of Vehicles in Lane 4', []), ('Lane 1 Traffic Flow', []), ('Lane 2 Traffic Flow', []), ('Lane 3 Traffic Flow', []), ('Lane 4 Traffic Flow', []), ('Lane 1 On Time', []), ('Lane 2 On Time', []), ('Lane 3 On Time', []), ('Lane 4 On Time', []), ('Lane 1 Saturation Flow', []), ('Lane 2 Saturation Flow', []), ('Lane 3 Saturation Flow', []), ('Lane 4 Saturation Flow', []), ('Lane 1 Flow Ratio', []), ('Lane 2 Flow Ratio', []), ('Lane 3 Flow Ratio', []), ('Lane 4 Flow Ratio', []), ('Total Flow Ratio', []), ('Optimum Cycle Time', []), ('Width of Lane 1', []), ('Width of Lane 2', []), ('Width of Lane 3', []), ('Width of Lane 4', []), ('Intergreen Period', []), ('Amber Period', []), ('Number of Phases', []), ('Initial Delay', []), ('Minimum On Time', []), ('Maximum Cycle Time', []), ('Total Time Lost', [])])
		self.trafficDataset = TrafficManagerDataset(self, self)
		self.createDatasetFrame()

	def close(self):
		self.destroy()
		self.originalFrame.show()
	
	def InitialisationParameters(self):
		for i in range(1, 5): self.data['Width of Lane ' + str(i)].append(self.originalFrame.specifications['Width of Lane ' + str(i)])
		self.data['Intergreen Period'].append(self.originalFrame.specifications['Intergreen Period'])
		self.data['Amber Period'].append(self.originalFrame.specifications['Amber Period'])
		self.data['Number of Phases'].append(self.originalFrame.specifications['Number of Phases'])
		self.data['Initial Delay'].append(self.originalFrame.specifications['Initial Delay'])
		self.data['Minimum On Time'].append(self.originalFrame.specifications['Minimum On Time'])
		self.data['Maximum Cycle Time'].append(self.originalFrame.specifications['Maximum Cycle Time'])
		
	def createDataset(self):
		self.InitialisationParameters()
		self.trafficDataset.cycleParameters(sample(range(1,66), 4))
	
	def saveDataset(self):
		df = pd.DataFrame(self.data)
		df.to_csv('dataset/TrafficDataset' + str(self.originalFrame.specifications['Size of Dataset']) + '.csv', index = False)

	def createDatasetFrame(self):
		# r and c tell us where to grid the labels
		self.mainFrame = tk.PanedWindow(self, orient = VERTICAL)
		self.mainFrame.pack()
		self.buttonFrame = tk.Frame(self)
		self.mainFrame.add(self.buttonFrame)
		self.saveButton = tk.Button(self.buttonFrame, text='Save', width=15, command = self.saveDataset)
		self.saveButton.pack(side = LEFT, fill = X, expand = 1)
		self.closeButton = tk.Button(self.buttonFrame, text='Back', width=15, command = self.close)
		self.closeButton.pack(side = LEFT, fill = X, expand = 1)
		self.update_idletasks()
		self.Frame = tk.Frame(self.mainFrame, height = 600, width = 900)
		self.mainFrame.add(self.Frame)
		self.update_idletasks()
		columnWidth = [len(k) for k in self.data.keys()]
		"""
		scrollbar1 = Scrollbar(self.Frame)
		scrollbar1.pack(side = RIGHT, fill = Y)
		scrollbar2 = Scrollbar(self.Frame)
		scrollbar2.pack(side = BOTTOM, fill = X)
		self.Canvas.configure(yscrollcommand = scrollbar1.set, xscrollcommand = scrollbar2.set)
		"""
		self.label = [[None] * len(self.data.keys())]
		self.frame = []
		self.createDataset()
		#print([self.data[x] for x in self.data.keys()])
		self.frame.append(tk.Frame(self.Frame))
		for i in range(len(self.data.keys())):
			self.label[0][i] = tk.Label(self.frame[0], text = self.data.keys()[i], relief = RIDGE, width = columnWidth[i])#, height = 2)
			self.label[0][i].pack(side = LEFT)
		self.frame[0].pack()
		for r in range(1, int(self.originalFrame.specifications['Size of Dataset'])):
			c = 0
			self.frame.append(tk.Frame(self.Frame))
			self.label.append([None] * len(self.data.keys()))
			for col in self.data.keys():
				#print(row)
				self.label[r][c] = tk.Label(self.frame[r], text = str(self.data[col][r - 1]), relief = RIDGE, width = columnWidth[c])#, width = 10, height = 2)
				self.label[r][c].pack(side = LEFT)
				c += 1
			self.frame[r].pack()
			r += 1
			self.createDataset()
			self.update_idletasks()
		#print('----Done----')
		self.protocol("WM_DELETE_WINDOW", self.originalFrame.root.destroy)
		self.update_idletasks()

class DisplayDatasetFrame(tk.Frame):
	"""Basic test frame for the table"""
	def __init__(self, parent=None):
		self.parent = parent
		tk.Frame.__init__(self)
		self.main = self.master
		#print(self.master)
		#self.main.geometry('600x400+200+100')
		self.main.title('Dataset Display')
		f = tk.Toplevel(self.main)
		#f.pack(fill=BOTH,expand=1)
		df = pd.DataFrame(pd.read_csv('dataset/TrafficDataset' + str(self.originalFrame.specifications['Size of Dataset']) + '.csv'))
		self.table = pt = Table(f, dataframe=df, showtoolbar=True, showstatusbar=True)
		pt.show()
		return

class DataVisualizationFrame(tk.Toplevel):
	def __init__(self, original):
		"""Constructor"""
		self.originalFrame = original
		#setDatasetSize(self.originalFrame.specifications['Size of Dataset'])
		self.graph = graph(self.originalFrame.specifications['Size of Dataset'])
		tk.Toplevel.__init__(self)
		self.geometry("300x220")
		self.title("Data Visualization")
		self.dataVisualiztaionFrame()

	def close(self):
		self.destroy()
		self.originalFrame.show()

	def dataVisualiztaionFrame(self):
		vehicleNumberButton = tk.Button(self, text = 'Number of Vehicles at Each Lane', command = self.graph.createGraphs_vehicleNumber)
		vehicleNumberButton.pack(fill = BOTH, expand = 1)
		trafficFlowButton = tk.Button(self, text = 'Traffic Flow of Each Lane', command = self.graph.createGraphs_trafficFlow)
		trafficFlowButton.pack(fill = BOTH, expand = 1)
		onTimeButton = tk.Button(self, text = 'On Time of Each Lane', command = self.graph.createGraphs_onTime)
		onTimeButton.pack(fill = BOTH, expand = 1)
		flowRatioButton = tk.Button(self, text = 'Traffic Flow Ratio of Each Lane', command = self.graph.createGraphs_flowRatio)
		flowRatioButton.pack(fill = BOTH, expand = 1)
		totalTrafficFlowButton = tk.Button(self, text = 'Total Traffic Flow', command = self.graph.createGraphs_totalTrafficFlow)
		totalTrafficFlowButton.pack(fill = BOTH, expand = 1)
		optimumCycleTimeButton = tk.Button(self, text = 'Optimum Cycle Time', command = self.graph.createGraphs_optimumCycleTime)
		optimumCycleTimeButton.pack(fill = BOTH, expand = 1)
		closeButton = tk.Button(self, text = 'Back', command = self.close)
		closeButton.pack(side = LEFT, expand = 1)
		self.protocol("WM_DELETE_WINDOW", self.originalFrame.root.destroy)
		self.update_idletasks()

class ITM(object):
	def __init__(self, parent):
		"""Constructor"""
		self.root = parent
		self.root.title("Intelligent Traffic Manager")
		self.frame1 = tk.Frame(parent)
		self.frame1.pack(fill=X, expand=True)
		self.openframe(self.frame1)
	
	def openframe(self, parent):
		#mainPanedWindow = tk.PanedWindow(parent, orient = HORIZONTAL)
		#mainPanedWindow.pack(fill=BOTH, expand=1)
		self.laneView = sample(range(1,66), 4)
		self.iter = 1
		subPanedWindow1 = tk.PanedWindow(parent, orient = VERTICAL)
		#laneRateFrame = tk.Frame(subPanedWindow1)
		#self.EmptyLine = tk.Label(laneRateFrame, text = "")
		#self.EmptyLine.pack()
		#laneRateButton = tk.Button(laneRateFrame, text = 'Change Specifications', command = self.openSpecificationsFrame)
		#laneRateButton.pack(fill = X, expand=1)
		#subPanedWindow1.add(laneRateFrame)		
		algorithmFrame = tk.Frame(subPanedWindow1)
		subPanedWindow1.add(algorithmFrame)

		inputFolderFrame = tk.Frame(subPanedWindow1)
		#folderLabel = tk.Label(directoryNameFrame, text = 'Input Directory:')
		#folderLabel.pack(side = LEFT)
		inputFolderButton = tk.Button(inputFolderFrame, text = 'Browse Input Folder', width = 20, command = lambda:[self.browseFiles(inputFolderEntry)])
		inputFolderButton.pack(side = LEFT, fill = Y)
		self.inputFolder = StringVar()
		self.inputFolder.set('/home/yash/workspace-ITMS/BEProject/input')
		inputFolderEntry = tk.Entry(inputFolderFrame, textvariable = self.inputFolder)
		#inputFolderEntry.insert(0, inputFolder.get())
		inputScrollbar = tk.Scrollbar(inputFolderFrame, orient = tk.HORIZONTAL, command = inputFolderEntry.xview)
		inputScrollbar.pack(side = BOTTOM, fill = X)
		inputFolderEntry.configure(xscrollcommand = inputScrollbar.set)
		inputFolderEntry.pack(side = LEFT, fill = X, expand = 1)
		subPanedWindow1.add(inputFolderFrame)
		
		outputFolderFrame = tk.Frame(subPanedWindow1)
		#folderLabel = tk.Label(directoryNameFrame, text = 'Input Directory:')
		#folderLabel.pack(side = LEFT)
		outputFolderButton = tk.Button(outputFolderFrame, text = 'Browse Output Folder', width = 20, command = lambda:[self.browseFiles(outputFolderEntry)])
		outputFolderButton.pack(side = LEFT, fill = Y)
		self.outputFolder = StringVar()
		self.outputFolder.set('/home/yash/workspace-ITMS/BEProject/output')
		outputFolderEntry = tk.Entry(outputFolderFrame, textvariable = self.outputFolder)
		#outputFolderEntry.insert(0, outputFolder.get())
		outputScrollbar = tk.Scrollbar(outputFolderFrame, orient = tk.HORIZONTAL, command = outputFolderEntry.xview)
		outputScrollbar.pack(side = BOTTOM, fill = X)
		#print(inputFolder.get(), outputFolder.get())
		
		outputFolderEntry.configure(xscrollcommand = outputScrollbar.set)
		outputFolderEntry.pack(side = LEFT, fill = X, expand = 1)
		subPanedWindow1.add(outputFolderFrame)
		
		testImageButton = tk.Button(algorithmFrame, text = 'Test Image Processing Algorithm', command = self.openImageProcessingFrame)
		testImageButton.pack(fill = X, expand=1)
		self.imgfile = [tk.PhotoImage(file = 'images/red.png'), tk.PhotoImage(file = 'images/yellow.png'), tk.PhotoImage(file = 'images/green.png')]
		trafficManageButton = tk.Button(algorithmFrame, text = 'Run Intelligent Traffic Manager', command = self.openManageTrafficFrame)
		trafficManageButton.pack(fill = X, expand=1)
		subPanedWindow1.pack(side = LEFT, fill = X, expand = 1)
		#mainPanedWindow.add(subPanedWindow1)

		roadViewButton = tk.Button(algorithmFrame, text = 'Show Road View', command = self.openRoadViewFrame)
		roadViewButton.pack(fill = X, expand=1)
		
		createDatasetButton = tk.Button(algorithmFrame, text = 'Create Dataset', command = self.openCreateDatasetFrame)
		createDatasetButton.pack(fill = X, expand=1)
		
		displayDatasetButton = tk.Button(algorithmFrame, text = 'Display Dataset', command = self.openDisplayDatasetFrame)
		displayDatasetButton.pack(fill = X, expand=1)
		
		displayDatasetButton = tk.Button(algorithmFrame, text = 'Data Visualization', command = self.openDataVisualizationFrame)
		displayDatasetButton.pack(fill = X, expand=1)


		subPanedWindow2 = tk.PanedWindow(parent, orient = VERTICAL)
		self.changeSpecificationsButton = tk.Button(subPanedWindow2, text = "Traffic Specifications", command = self.openSpecificationsFrame)
		self.changeSpecificationsButton.pack(fill = X, expand=1)
		#self.variableTitle.pack(fill = BOTH)
		self.variableFrame = []
		self.variableLabel = []
		self.variable = []
		self.specificationsVariable = []
		self.specifications = OrderedDict([('Intergreen Period', 4), ('Amber Period', 2), ('Number of Phases', 4), ('Initial Delay', 0), ('Minimum On Time', 10), ('Width of Lane 1', 10), ('Width of Lane 2', 10), ('Width of Lane 3', 10), ('Width of Lane 4', 10), ('Maximum Cycle Time', 120), ('Size of Dataset', 100), ('Number of Iterations', 2)])
		for i in range(len(self.specifications.keys())):
			self.specificationsKey = self.specifications.keys()[i]
			self.variableFrame.append(tk.Frame(subPanedWindow2))
			self.variableFrame[i].pack(fill = BOTH, expand=1)
			text = self.specificationsKey + ": "
			self.variableLabel.append(tk.Label(self.variableFrame[i], text = text, width = 20, anchor = W))#,  relief = RAISED))
			self.variableLabel[i].pack(side = LEFT)#, fill = BOTH)#, expand=1)
			self.specificationsVariable.append(StringVar())
			self.variable.append(tk.Label(self.variableFrame[i], textvariable = self.specificationsVariable[i],  relief = RIDGE))
			self.specificationsVariable[i].set(self.specifications[self.specificationsKey])
			self.variable[i].pack(side = LEFT, fill = BOTH, expand=1)
			"""self.variable2 = tk.Label(variableFrame, text = 'Lane 2 rate: ' + str(tlrate[1]), relief = RAISED)
			self.variable2.pack(fill = BOTH, expand=1)
			self.variable3 = tk.Label(variableFrame, text = 'Lane 3 rate: ' + str(tlrate[2]), relief = RAISED)
			self.variable3.pack(fill = BOTH, expand=1)
			self.variable4 = tk.Label(variableFrame, text = 'Lane 4 rate: ' + str(tlrate[3]), relief = RAISED)
			self.variable4.pack(fill = BOTH, expand=1)"""
			#subPanedWindow2.add(self.variableFrame[i])
		subPanedWindow2.pack(side = LEFT, fill = BOTH, expand=1)
		#mainPanedWindow.add(subPanedWindow2)

	def hide(self):
		self.root.withdraw()

	def onCloseOtherFrame(self, otherFrame):
		otherFrame.destroy()
		self.show()

	def show(self):
		self.root.update()
		self.root.deiconify()
	
	def openSpecificationsFrame(self):
		self.hide()
		subFrame = SpecificationsFrame(self)

	def openImageProcessingFrame(self):
		self.hide()
		subFrame = ImageProcessingFrame(self)

	def openRoadViewFrame(self):
		self.hide()
		subFrame = RoadViewFrame(self)

	def openManageTrafficFrame(self):
		self.hide()
		subFrame = ManageTrafficFrame(self)

	def openCreateDatasetFrame(self):
		self.hide()
		subFrame = CreateDatasetFrame(self)

	def openDisplayDatasetFrame(self):
		subFrame = DisplayDatasetFrame()

	def openDataVisualizationFrame(self):
		self.hide()
		subFrame = DataVisualizationFrame(self)

	def browseFiles(self, parent): 
		directory = filedialog.askdirectory(initialdir = "../../", title = "Select a Directory")
		#print(directory)
		parent.delete(0,'end')
		parent.insert(0, directory)
		#Change label contents
		#label_file_explorer.configure(text="File Opened: "+filename)

"""
def changeValues():
	tlrate[0] = float(entry[0].get())/4
	variable1.configure(text = 'Lane 1 rate: ' + str(tlrate[0]))
	tlrate[1] = float(entry[1].get())/4
	variable2.configure(text = 'Lane 2 rate: ' + str(tlrate[1]))
	tlrate[2] = float(entry[2].get())/4
	variable3.configure(text = 'Lane 3 rate: ' + str(tlrate[2]))
	tlrate[3] = float(entry[3].get())/4
	variable4.configure(text = 'Lane 4 rate: ' + str(tlrate[3]))
	print(tlrate)

def changelaneRate():
	laneRateToplevel = tk.Toplevel(itms)
	for i in range(4):
		label[i] = tk.Label(laneRateToplevel, text = 'Lane ' + str(i+1) + '\t')
		label[i].pack()
		entry[i] = tk.Entry(laneRateToplevel)
		entry[i].insert('end', int(tlrate[i]))
		entry[i].pack()
	okButton = tk.Button(laneRateToplevel, text='OK', width=10, command=lambda:[laneRateToplevel.withdraw(), changeValues()])
	okButton.pack()
	#laneRateToplevel.mainloop()

def browseFiles(): 
	directory = filedialog.askdirectory(initialdir = "../../", title = "Select a Directory")
	#print(directory)
	folderEntry.delete(0,'end')
	folderEntry.insert(0, directory)
    #Change label contents
    #label_file_explorer.configure(text="File Opened: "+filename)
"""
"""
def testImage():
		i = str(randint(1,65))
		img = directory + '/' + i + ".png"
		j = traffic_density(img, i)
		img = "/home/yash/workspace-ITMS/BEProject/output/" + str(i) + ".png"
		image = cv2.imread(img)
		cv2.imshow(("image" + str(i) + " Traffic Density: " + str(j)),image)
		if cv2.waitKey(0) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
"""
"""
def roadViewShow():

	roadView = tk.Toplevel(itms)
	roadViewPanedWindow = tk.PanedWindow(roadView, height = 800, width = 800, orient = VERTICAL)
	roadViewPanedWindow.pack()
	subPanedWindowLeft = tk.PanedWindow(roadViewPanedWindow, orient = HORIZONTAL)
	lane1Frame = tk.Frame(subPanedWindowLeft)
	lane1 = tk.Label(lane1Frame, text = 'Lane 1', relief = RAISED)
	lane1.pack()
	img = ipfile[0]
	lane1Signal = tk.Label(lane1Frame, image = img, relief = RAISED)
	lane1Signal.pack()
	subPanedWindowLeft.add(lane1Frame)

	lane2Frame = tk.Frame(subPanedWindowLeft)
	lane2 = tk.Label(lane2Frame, text = 'Lane 2', relief = RAISED)
	lane2.pack()
	img = ipfile[1]
	lane2Signal = tk.Label(lane2Frame, image = img, relief = RAISED)
	lane2Signal.pack()
	subPanedWindowLeft.add(lane2Frame)
	subPanedWindowLeft.add(lane2Frame)
	roadViewPanedWindow.add(subPanedWindowLeft)

	subPanedWindowRight = tk.PanedWindow(roadViewPanedWindow, orient = HORIZONTAL)
	lane3Frame = tk.Frame(subPanedWindowRight)
	lane3 = tk.Label(lane3Frame, text = 'Lane 3', relief = RAISED)
	lane3.pack()
	img = ipfile[2]
	lane3Signal = tk.Label(lane3Frame, image = img, relief = RAISED)
	lane3Signal.pack()
	subPanedWindowRight.add(lane3Frame)

	lane4Frame = tk.Frame(subPanedWindowRight)
	lane4 = tk.Label(lane4Frame, text = 'Lane 4', relief = RAISED)
	lane4.pack()
	img = ipfile[3]
	lane4Signal = tk.Label(lane4Frame, image = img, relief = RAISED)
	lane4Signal.pack()
	subPanedWindowRight.add(lane4Frame)
	subPanedWindowRight.add(lane4Frame)
	roadViewPanedWindow.add(subPanedWindowRight)
	#roadView.after(int(tim*1000), trafficSignal.destroy)
	itms.wait_window(roadView)
	#startButton = tk.Button(trafficSignalPanedWindow, text = 'START', command = coderun)
	#trafficSignalPanedWindow.add(startButton)
	#trafficSignal.destroy()
"""
"""
def runCode(color, tim):
	print(color, color[0])
	trafficSignal = tk.Toplevel(itms)
	trafficSignalPanedWindow = tk.PanedWindow(trafficSignal, height = 330, width = 250, orient = VERTICAL)
	trafficSignalPanedWindow.pack()
	subPanedWindowLeft = tk.PanedWindow(trafficSignalPanedWindow, orient = HORIZONTAL)
	lane1Frame = tk.Frame(subPanedWindowLeft)
	lane1 = tk.Label(lane1Frame, text = 'Lane 1', relief = RAISED)
	lane1.pack()
	img = imgfile[color[0]]
	lane1Signal = tk.Label(lane1Frame, image = img, relief = RAISED)
	lane1Signal.pack()
	subPanedWindowLeft.add(lane1Frame)

	lane2Frame = tk.Frame(subPanedWindowLeft)
	lane2 = tk.Label(lane2Frame, text = 'Lane 2', relief = RAISED)
	lane2.pack()
	img = imgfile[color[1]]
	lane2Signal = tk.Label(lane2Frame, image = img, relief = RAISED)
	lane2Signal.pack()
	subPanedWindowLeft.add(lane2Frame)
	subPanedWindowLeft.add(lane2Frame)
	trafficSignalPanedWindow.add(subPanedWindowLeft)

	
	subPanedWindowRight = tk.PanedWindow(trafficSignalPanedWindow, orient = HORIZONTAL)
	lane3Frame = tk.Frame(subPanedWindowRight)
	lane3 = tk.Label(lane3Frame, text = 'Lane 3', relief = RAISED)
	lane3.pack()
	img = imgfile[color[2]]
	lane3Signal = tk.Label(lane3Frame, image = img, relief = RAISED)
	lane3Signal.pack()
	subPanedWindowRight.add(lane3Frame)

	lane4Frame = tk.Frame(subPanedWindowRight)
	lane4 = tk.Label(lane4Frame, text = 'Lane 4', relief = RAISED)
	lane4.pack()
	img = imgfile[color[3]]
	lane4Signal = tk.Label(lane4Frame, image = img, relief = RAISED)
	lane4Signal.pack()
	subPanedWindowRight.add(lane4Frame)
	subPanedWindowRight.add(lane4Frame)
	trafficSignalPanedWindow.add(subPanedWindowRight)
	trafficSignal.after(int(tim*1000), trafficSignal.destroy)
	itms.wait_window(trafficSignal)
	#startButton = tk.Button(trafficSignalPanedWindow, text = 'START', command = coderun)
	#trafficSignalPanedWindow.add(startButton)
	#trafficSignal.destroy()
"""
"""
mainPanedWindow = tk.PanedWindow(itms, orient = HORIZONTAL)
mainPanedWindow.pack(fill=BOTH, expand=1)
subPanedWindow1 = tk.PanedWindow(mainPanedWindow, orient = VERTICAL)
laneRateFrame = tk.Frame(subPanedWindow1)
laneRateButton = tk.Button(laneRateFrame, text = 'Enter Lane Rate', width = 30, command=changelaneRate)
laneRateButton.pack(fill = X, expand=1)
subPanedWindow1.add(laneRateFrame)

directoryNameFrame = tk.Frame(subPanedWindow1)
#folderLabel = tk.Label(directoryNameFrame, text = 'Input Directory:')
#folderLabel.pack(side = LEFT)
inputFolderButton = tk.Button(directoryNameFrame, text = 'Browse Input Folder', width = 30, command = browseFiles)
inputFolderButton.pack(side = LEFT, fill = Y)
folderEntry = tk.Entry(directoryNameFrame)
folderEntry.insert(0, directory)
scrollbar = tk.Scrollbar(directoryNameFrame, orient = tk.HORIZONTAL, command = folderEntry.xview)
scrollbar.pack(side = BOTTOM, fill = X)
folderEntry.configure(xscrollcommand = scrollbar.set)
folderEntry.pack(side = LEFT)
subPanedWindow1.add(directoryNameFrame)

algorithmFrame = tk.Frame(subPanedWindow1)
testImageButton = tk.Button(algorithmFrame, text = 'Test Image Processing Algorithm', width = 30, command = testImage)
testImageButton.pack(fill = X, expand=1)
imgfile = [tk.PhotoImage(file = 'images/red1.png'), tk.PhotoImage(file = 'images/yellow1.png'), tk.PhotoImage(file = 'images/green1.png')]
trafficManageButton = tk.Button(algorithmFrame, text = 'Run Intelligent Traffic Manager', width = 30, command = codeRun)
trafficManageButton.pack(fill = X, expand=1)
subPanedWindow1.add(algorithmFrame)
mainPanedWindow.add(subPanedWindow1)



subPanedWindow2 = tk.PanedWindow(mainPanedWindow, orient = VERTICAL)
variableFrame = tk.Frame(subPanedWindow2)
variable1 = tk.Label(variableFrame, text = 'Lane 1 rate: ' + str(tlrate[0]), relief = RAISED)
variable1.pack(fill = BOTH, expand=1)
variable2 = tk.Label(variableFrame, text = 'Lane 2 rate: ' + str(tlrate[1]), relief = RAISED)
variable2.pack(fill = BOTH, expand=1)
variable3 = tk.Label(variableFrame, text = 'Lane 3 rate: ' + str(tlrate[2]), relief = RAISED)
variable3.pack(fill = BOTH, expand=1)
variable4 = tk.Label(variableFrame, text = 'Lane 4 rate: ' + str(tlrate[3]), relief = RAISED)
variable4.pack(fill = BOTH, expand=1)
subPanedWindow2.add(variableFrame)
mainPanedWindow.add(subPanedWindow2)


#imgfile = tk.PhotoImage(file = filename)
#imgfile = imgfile.zoom(0.1, 0.1)
#variable5 = tk.Label(mainPanedWindow, image = imgfile)
#mainPanedWindow.add(variable5)



ipfile = []
for i in order:
	ipfile.append(tk.PhotoImage(file = 'input/' + str(i) + '.png'))

roadViewButton = tk.Button(algorithmFrame, text = 'Show Road View', width = 30, command = roadViewShow)
roadViewButton.pack(fill = X, expand=1)
"""
itms = tk.Tk()
itms.geometry("700x290")
itms.title("ITM")
software = ITM(itms)
itms.mainloop()
