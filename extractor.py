import cv2
import json
import progressbar
import csv
import easyocr

def croppedFrame(frame, x, y, width, height):
	img = frame[y:y+height, x:x+width]
	if saveFrames:
		cv2.imwrite(f'debug/frame_img_{x}_{y}_{width}_{height}.jpg', img)
	grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	if saveFrames:
		cv2.imwrite(f'debug/frame_gray_{x}_{y}_{width}_{height}.jpg', grayImage)
	_, binaryImage = cv2.threshold(grayImage, 200, 255, cv2.THRESH_BINARY_INV)
	if saveFrames:
		cv2.imwrite(f'debug/frame_{x}_{y}_{width}_{height}.jpg', binaryImage)
	return binaryImage

def extractDots(frame):
	#TODO: Por hacer algún día
	pass

def extractBarPercentage(frame):
	#TODO: Por hacer algún día
	pass

def extractText(pos, frame):
	region = croppedFrame(frame, pos['x'], pos['y'], pos['width'], pos['heigth'])
	result = reader.readtext(region)
	if len(result) <1:
		return 'N/A'
	return result[0][1]

def normalizeTimestamp(text:str):
	#TODO: Mejorar esto
	text = text.lower().replace('i','1').replace(';',':').replace('.',':').replace('::',':').replace('o','0').replace(' ','')
	counter = 0
	final = ''
	for i in text:
		if counter == 2:
			counter = -1
			if i != ':':
				final += ':'+i
			else:
				final += i
		else:
			if i != ':':
				final += i
		counter +=1
	return final

def writeRectangeZone(frame,points):
	x1=points['x']
	y1=points['y']
	x2=x1+points['width']
	y2=y1+points['heigth']
	print((x1,y2),(x2,y2))
	return cv2.rectangle(frame, (x1,y1),(x2,y2), (255, 0, 0) , 2) 

def saveCsv(path, header, rows):
	with open(path, 'w') as f:
		write = csv.writer(f)
		write.writerow(header)
		write.writerows(rows)
saveFrames = False
metadata_file = open('videos/metadata.json')
metadata = json.load(metadata_file)

reader = easyocr.Reader(['en'])
dataHeaders = ['time', 'seconds', 'altitude', 'speed']

for data in metadata:
	if data['skip']:
		continue
	print('Starting analysis for', data['id'])

	video = cv2.VideoCapture(data['path'])
	fps = video.get(cv2.CAP_PROP_FPS)

	currect_frame = int(data['booster_start'] * fps)
	starship_end_frame = int(data['starship_end'] * fps)
	starship_start_frame = int(data['starship_start'] * fps)
	booster_end_frame = int(data['booster_end'] * fps)
	saveFrames = bool(data['save_frames'])
	booster = []
	starship = []

	widgets = [
		' [',
		progressbar.Timer(format='elapsed time: %(elapsed)s'),
		'] ',
		progressbar.Bar('*'),
		' (',
		progressbar.ETA(), 
		') ',
	]
	bar = progressbar.ProgressBar(widgets=widgets, min_value=currect_frame, max_value=starship_end_frame).start()
	recolectionRate = data['recolection_rate']
	while 1:
		video.set(cv2.CAP_PROP_POS_FRAMES, currect_frame)

		ret, frame = video.read()
		if not ret:
			print('Fail extracting data!')
			bar.finish()
			break

		timer = normalizeTimestamp(extractText(data['timer_pos'], frame))
		sections = timer.split(':')
		seconds = (currect_frame - int(data['booster_start'] * fps)) / fps
		
		if currect_frame <= booster_end_frame:
			booster_altitude = extractText(data['booster_altitude_pos'], frame)
			booster_speed = extractText(data['booster_speed_pos'], frame)

			booster.append([timer, seconds, booster_altitude, booster_speed])

		if currect_frame >= starship_start_frame:
			starship_altitude = extractText(data['starship_altitude_pos'], frame)
			starship_speed = extractText(data['starship_speed_pos'], frame)
			starship.append([timer, seconds, starship_altitude, starship_speed])

		if data['recolection_increse'] is not None:
			recolectionRate = data['recolection_rate'] + seconds*data['recolection_increse']
		currect_frame += recolectionRate
		
		if saveFrames:
			frame = writeRectangeZone(frame,data['starship_altitude_pos'])
			frame = writeRectangeZone(frame,data['starship_speed_pos'])
			frame = writeRectangeZone(frame,data['timer_pos'])
			cv2.imwrite(f'debug/frame.jpg', frame)

		# TODO: terminar el analisis con la sharship no es correcto del todo.
		if currect_frame > starship_end_frame:
			bar.finish()
			print('Analysis completed!')
			break
		bar.update(currect_frame)
		#break
	print("Final recolection rate",recolectionRate )
	saveCsv('outputs/booster-{}.csv'.format(data['id']), dataHeaders, booster)
	saveCsv('outputs/starship-{}.csv'.format(data['id']), dataHeaders, starship)


