import multiprocessing
import gradio
import asyncio
import websockets
import cv2
import base64
import numpy as np
import time
import facefusion.globals
import os

from facefusion.uis.components import about, frame_processors, frame_processors_options, execution, execution_thread_count, webcam_options, source, webcam
import threading


def pre_check() -> bool:
	return True


def pre_render() -> bool:
	return True

imageInUse = 'None'

def switchToNana() -> None:
	print('Na na')
	facefusion.globals.source_paths = ['./images/nana.jpg']
	return 'Nana'
def switchToRose() -> None:
	print('Rose')
	facefusion.globals.source_paths = ['./images/rose.webp']
	return 'Rose'
def switchToJisoo() -> str:
	print('Jisoo')
	facefusion.globals.source_paths = ['./images/jiso.jpg']
	return 'Jisoo'

def reset() -> None:
	print('Reset')
	facefusion.globals.source_paths = []
	return 'None'
 
gradioLabel = None

def render() -> gradio.Blocks:
	with gradio.Blocks() as layout:
		with gradio.Row(equal_height=True, elem_classes='container'):
			with gradio.Column(scale = 1, visible=False):
				with gradio.Blocks():
					about.render()
				with gradio.Blocks():
					frame_processors.render()
				with gradio.Blocks():
					frame_processors_options.render()
				with gradio.Blocks():
					execution.render()
					execution_thread_count.render()
			with gradio.Column(scale = 6):
				with gradio.Blocks():
					webcam.render()
			with gradio.Column(scale=1):
				with gradio.Blocks():
					gradioLabel = gradio.Label(label='Image in use: ',value=imageInUse)
				with gradio.Row():
					with gradio.Blocks():
						gradio.Button(value='Na na').click(switchToNana, outputs=gradioLabel)
				with gradio.Row():
					with gradio.Blocks():
						gradio.Button(value='Rose').click(switchToRose, outputs=gradioLabel)
				with gradio.Row():
					with gradio.Blocks():
						gradio.Button(value='Jisoo').click(switchToJisoo, outputs=gradioLabel)
				with gradio.Row():
					with gradio.Blocks():
						source.render()
				with gradio.Row():
					with gradio.Blocks():
						gradio.Button(value='Reset').click(reset, outputs=gradioLabel)
			with gradio.Column(scale=1, visible=False):
				# with gradio.Blocks():
				# 	source.render()
				with gradio.Blocks():
					webcam_options.render()
	return layout


def listen() -> None:
	frame_processors.listen()
	frame_processors_options.listen()
	execution.listen()
	execution_thread_count.listen()
	source.listen()
	webcam.listen()


async def server(websocket, path):
    # cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    message_count = 0
    start_time = time.time()

    while True:
        try:
            message = await websocket.recv()
            if message == "start":
                print("Starting")
                facefusion.globals.isRunning = True
            elif message == "stop":
                print("Stopping")
                facefusion.globals.isRunning = False
                facefusion.globals.streamImage = None
            else: 
                rawImg = message.split(",")[1]
				# Decode the base64 string to bytes
                # image_bytes = base64.b64decode(rawImg)
				
				# Convert the bytes to numpy array
                image_array = np.fromstring(base64.b64decode(rawImg), np.uint8)
				
                # image_array = np.reshape(image_array, (-1, 1))
				# Reshape the numpy array
				# Decode the numpy array to an image
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                # image = cv2.resize(image, (1280, 960))
                facefusion.globals.streamImage = image
				
				# Increment the message count
                message_count += 1


            
            # Check if 1 second has passed
            if time.time() - start_time >= 1:
                print("Number of messages received in 1 second:", message_count)
                # Reset the message count and start time
                message_count = 0
                start_time = time.time()
                
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")
            break

    cv2.destroyAllWindows()

def start_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    socketServer = os.environ.get('SOCKET_SERVER', 'localhost')
    start_server = websockets.serve(server, socketServer, 8000)
    print("Server started: ",socketServer)
    loop.run_until_complete(start_server)
    print("Server running")
    loop.run_forever()


def runUi(ui : gradio.Blocks):
    concurrency_count = min(2, multiprocessing.cpu_count())
    server_name = os.environ.get('SERVER_NAME', '127.0.0.1')
    print("Running UI")
    ui.queue(concurrency_count = concurrency_count).launch(show_api = False, quiet = True,server_name=server_name)
	
 
def run(ui : gradio.Blocks) -> None:
    # create new thread for the websocket server
	thread = threading.Thread(target=start_server)
	thread.start()
	print("Thread started")
	# thread.join()
	runUi(ui)
