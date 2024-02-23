##Creates an interface between python code and comfyUI using websockets

import random
import websockets
import uuid
import json
import urllib.request
import urllib.parse
from PIL import Image
import io

server_address = "127.0.0.1:8188"
client_id = str(uuid.uuid4())
uri = f"ws://{server_address}/ws?clientId={client_id}"
ws = None
def queue_prompt(prompt, client_id):
    p = {"prompt": prompt, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://{}/prompt".format(server_address), data=data)
    return json.loads(urllib.request.urlopen(req).read())
def get_image(filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("http://{}/view?{}".format(server_address, url_values)) as response:

        return response.read()

def get_history(prompt_id):
    with urllib.request.urlopen("http://{}/history/{}".format(server_address, prompt_id)) as response:
        return json.loads(response.read())


async def connect():
    global ws
    ##ensures that there exists a connection
    ws = await websockets.connect(uri)

async def close():
    global ws
    if ws:
        await ws.close()

async def get_images(prompt):
    if not ws:
        await connect()

    prompt_id = queue_prompt(prompt, client_id)['prompt_id']
    currently_Executing_Prompt = None
    output_images = {}
    async for out in ws:
        try:
            message = json.loads(out)
            if message['type'] == 'execution_start':
                currently_Executing_Prompt = message['data']['prompt_id']
            if message['type'] == 'executing' and prompt_id == currently_Executing_Prompt:
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break
        except ValueError as e:
            print("An error has occured");

    history = get_history(prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images
async def generate_image(prompt_):
    prompt = json.load(open('workflow_api.json'))
    prompt["6"]["inputs"]["text"] = prompt_
    prompt["3"]["inputs"]["seed"] = random.randint(0, 999999999999999)
    await connect()
    images = await get_images(prompt)
    await close()
    for node_id in images:
        for image_data in images[node_id]:
            image = Image.open(io.BytesIO(image_data))
            image.save("output.png")
            return "output.png"


