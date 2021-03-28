# Import pandas package
import pandas as pd
from ImageProcessing import *
import matplotlib
import matplotlib.pyplot as plt
#from matplotlib.widgets import Slider

# Define a dictionary containing employee data
data = {'Image':[], 'No. of Vehicles':[], 'Vehicle Type':[]}
s = 1
#size = 0
def setDatasetSize(datasetSize):
	size = datasetSize
	#print(size)

def create(inputFolder):
	for i in range(1, 66):
		img = inputFolder + str(i) + ".png"
		data['Image'].append(str(i) + ".png")
		data['No. of Vehicles'].append(ip.trafficDensity(img, i))
		data['Vehicle Type'].append(':'.join(ip.trafficType()))
		print(str(round(i/0.65)) + '%')
		#print(data['Vehicle Type'], ip.trafficType())
		#break
		#img = outputFolder + str(i) + ".png"
	# Convert the dictionary into DataFrame 
	df = pd.DataFrame(data)
	df.index = np.arange(1, len(df)+1)
	# select two columns
	df.to_csv('dataset/ImageProcessingData.csv', index = False)
	#print(df[['Image', 'No. of Vehicles']])

def getData(i):
	# making data frame from csv file
	data = pd.read_csv("dataset/ImageProcessingData.csv")
	#data = data.drop("Unnamed: 0", axis = 1)
	data.index = np.arange(1, len(data)+1)
	# retrieving columns by indexing operator
	#print(data["No. of Vehicles"][i])
	return [data["No. of Vehicles"][i], data["Vehicle Type"][i]]

class graph():
	def __init__(self, datasetSize):
		self.size = datasetSize

	def createGraphs_vehicleNumber(self):
		fig, axs = plt.subplots(2, 2)
		laneNumber = 1
		data  = (pd.read_csv('dataset/TrafficDataset' + str(self.size) + '.csv').astype(float))
		for i in range(2):
			for j in range(2):
				colName = 'Number of Vehicles in Lane ' + str(laneNumber)
				vehicles = [round(sum(data[colName].values[s*k:s*(k+1)])/s) for k in range(len(data[colName].values)/s)]
				axs[i, j].set_title(colName)
				axs[i, j].bar(range(len(vehicles)), vehicles)
				laneNumber += 1
				#axs.show()
		plt.show()

	def createGraphs_trafficFlow(self):
		fig, axs = plt.subplots(2, 2)
		laneNumber = 1
		data  = (pd.read_csv('dataset/TrafficDataset' + str(self.size) + '.csv').astype(float))
		for i in range(2):
			for j in range(2):
				colName = 'Lane ' + str(laneNumber) +  ' Traffic Flow'
				vehicles = [round(sum(data[colName].values[s*k:s*(k+1)])/s) for k in range(len(data[colName].values)/s)]
				axs[i, j].set_title(colName)
				axs[i, j].bar(range(len(vehicles)), vehicles)
				laneNumber += 1
				#axs.show()
		plt.show()

	def createGraphs_onTime(self):
		fig, axs = plt.subplots(2, 2)
		laneNumber = 1
		data  = (pd.read_csv('dataset/TrafficDataset' + str(self.size) + '.csv').astype(float))
		for i in range(2):
			for j in range(2):
				colName = 'Lane ' + str(laneNumber) +  ' On Time'
				vehicles = [round(sum(data[colName].values[s*k:s*(k+1)])/s) for k in range(len(data[colName].values)/s)]
				axs[i, j].set_title(colName)
				axs[i, j].bar(range(len(vehicles)), vehicles)
				laneNumber += 1
				#axs.show()
		plt.show()

	def createGraphs_flowRatio(self):
		fig, axs = plt.subplots(2, 2)
		laneNumber = 1
		data  = (pd.read_csv('dataset/TrafficDataset' + str(self.size) + '.csv').astype(float))
		for i in range(2):
			for j in range(2):
				colName = 'Lane ' + str(laneNumber) +  ' Flow Ratio'
				vehicles = [sum(data[colName].values[s*k:s*(k+1)])/s for k in range(len(data[colName].values)/s)]
				axs[i, j].set_title(colName)
				axs[i, j].bar(range(len(vehicles)), vehicles)
				laneNumber += 1
				#axs.show()
		plt.show()

	def createGraphs_totalTrafficFlow(self):
		colName = 'Total Flow Ratio'
		data  = (pd.read_csv('dataset/TrafficDataset' + str(self.size) + '.csv'))
		vehiclesLane1 = [sum(data[colName].values[s*i:s*(i+1)])/s for i in range(len(data[colName].values)/s)]
		plt.title(colName)
		plt.bar(range(len(vehiclesLane1)), vehiclesLane1)
		plt.show()

	def createGraphs_optimumCycleTime(self):
		colName = 'Optimum Cycle Time'
		data  = (pd.read_csv('dataset/TrafficDataset' + str(self.size) + '.csv'))
		vehiclesLane1 = [sum(data[colName].values[s*i:s*(i+1)])/s for i in range(len(data[colName].values)/s)]
		plt.title(colName)
		plt.bar(range(len(vehiclesLane1)), vehiclesLane1)
		plt.show()


#ip = TrafficDensity()
#create('input/')
#print(type(getData(24)[1]))
#createGraphs_optimumCycleTime()
