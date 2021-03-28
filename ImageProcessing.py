# USAGE
# python yolo.py --image images/baggage_claim.jpg --yolo yolo-coco

# import the necessary packages
import numpy as np
import argparse
import time
import cv2
import os

class TrafficDensity:
	def __init__(self):
		return
		#print(self.trafficDensity(image_loc, image_name))
		#print(self.trafficType())
	
	def trafficType(self):
		print([self.LABELS[i] for i in self.classIDs])
		return [self.LABELS[i] for i in self.classIDs]

	def trafficDensity(self, image_loc, image_name):
		# construct the argument parse and parse the arguments
		"""ap = argparse.ArgumentParser()
		ap.add_argument("-i", "--image", required=True, help="path to input image")
		ap.add_argument("-y", "--yolo", required=True, help="base path to YOLO directory")
		ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probability to filter weak detections")
		ap.add_argument("-t", "--threshold", type=float, default=0.3, help="threshold when applyong non-maxima suppression")
		args = vars(ap.parse_args())"""
		args = {"image":(image_loc),"yolo":"yolo-coco","confidence":float(0.5),"threshold":float(0.3)}
		# load the COCO class labels our YOLO model was trained on
		labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
		self.LABELS = open(labelsPath).read().strip().split("\n")
		
		# initialize a list of colors to represent each possible class label
		np.random.seed(42)
		COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3), dtype="uint8")
		
		# derive the paths to the YOLO weights and model configuration
		weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
		configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])

		# load our YOLO object detector trained on COCO dataset (80 classes)
		#print("[INFO] loading YOLO from disk...")
		net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
		# load our input image and grab its spatial dimensions
		image = cv2.imread(args["image"])
		(H, W) = image.shape[:2]
		
		# determine only the *output* layer names that we need from YOLO
		ln = net.getLayerNames()
		ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
		
		# construct a blob from the input image and then perform a forward
		# pass of the YOLO object detector, giving us our bounding boxes and
		# associated probabilities
		blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
		net.setInput(blob)
		start = time.time()
		layerOutputs = net.forward(ln)
		end = time.time()
		
		# show timing information on YOLO
		#print("[INFO] YOLO took {:.6f} seconds".format(end - start))
		
		# initialize our lists of detected bounding boxes, confidences, and
		# class IDs, respectively
		boxes = []
		confidences = []
		self.classIDs = []
		
		# loop over each of the layer outputs
		for output in layerOutputs:
		# loop over each of the detections
			for detection in output:
				# extract the class ID and confidence (i.e., probability) of
				# the current object detection
				scores = detection[5:]
				classID = np.argmax(scores)
				confidence = scores[classID]
				if classID == 0:
					continue
					# filter out weak predictions by ensuring the detected
					# probability is greater than the minimum probability
				if confidence > args["confidence"]:
					# scale the bounding box coordinates back relative to the
					# size of the image, keeping in mind that YOLO actually
					# returns the center (x, y)-coordinates of the bounding
					# box followed by the boxes' width and height
					box = detection[0:4] * np.array([W, H, W, H])
					(centerX, centerY, width, height) = box.astype("int")

					# use the center (x, y)-coordinates to derive the top and
					# and left corner of the bounding box
					x = int(centerX - (width / 2))
					y = int(centerY - (height / 2))
		
					# update our list of bounding box coordinates, confidences,
					# and class IDs
					boxes.append([x, y, int(width), int(height)])
					confidences.append(float(confidence))
					self.classIDs.append(classID)
		
		# apply non-maxima suppression to suppress weak, overlapping bounding
		# boxes
		idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],	args["threshold"])
		#print(self.LABELS)
		#print(type(self.classIDs))
		#abcdttt = np.empty(len(self.classIDs), dtype = object)
		#for i in range(len(self.classIDs)):
		#abcdttt[i] = self.LABELS[self.classIDs[i]]
		#print(len(idxs), ([self.LABELS[i] for i in self.classIDs]))#confidences, args["confidence"], args["threshold"])
		
		# ensure at least one detection exists
		if len(idxs) > 0:
			# loop over the indexes we are keeping
			for i in idxs.flatten():
				# extract the bounding box coordinates
				(x, y) = (boxes[i][0], boxes[i][1])
				(w, h) = (boxes[i][2], boxes[i][3])
		
				# draw a bounding box rectangle and label on the image
				color = [int(c) for c in COLORS[self.classIDs[i]]]
				cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
				text = "{}: {:.4f}".format(self.LABELS[self.classIDs[i]], confidences[i])
				cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
		
		# show the output image
		cv2.imwrite("output/"+ str(image_name) + ".png", image)
		#print(len(idxs))
		#cv2.imshow('image',image)
		#cv2.waitKey(0)
		#print(len(idxs))
		return len(idxs)
"""
#start = time.time()
a = TrafficDensity()
print(a.trafficDensity('input/1.png',1))
im = cv2.imread('output/1.png')
cv2.imshow('image', im)
cv2.waitKey(0)
#end = time.time()
#print(end - start)"""
