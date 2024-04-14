import websocket 
import uuid
import json
import urllib.request
import urllib.parse
import requests
from PIL import Image
import io
import random

# these functions are mostly lifted from the comfyui github repo, but adapted for our purposes

# server_address = "127.0.0.1:8188"
server_address = "lab:8188"
# server_address = "host.zzimm.com:8188"
client_id = str(uuid.uuid4())

def queue_prompt(prompt):
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

def get_images(ws, prompt):
    prompt_id = queue_prompt(prompt)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            continue #previews are binary data

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


def upload_file(file, subfolder="", overwrite=False):
    try:
        # Wrap file in formdata so it includes filename
        body = {"image": file}
        data = {}
        
        if overwrite:
            data["overwrite"] = "true"
  
        if subfolder:
            data["subfolder"] = subfolder

        resp = requests.post(f"http://{server_address}/upload/image", files=body,data=data)
        
        if resp.status_code == 200:
            data = resp.json()
            # Add the file to the dropdown list and update the widget value
            path = data["name"]
            if "subfolder" in data:
                if data["subfolder"] != "":
                    path = data["subfolder"] + "/" + path
            

        else:
            print(f"{resp.status_code} - {resp.reason}")
    except Exception as error:
        print(error)
    return path

def generate(base_image, id, sub_id, landmark_type = "post offie building", theme_prompt = "americana", num_images = 1, mode = "fast"):

    model_name = "realisticFantasy_v20.safetensors"

    with open(base_image, "rb") as f:
        comfyui_path_image = upload_file(f,"",True)

    #load workflow from file
    if mode == "fast":
        workflow_name = "workflow_api_fast.json"
    else:
        workflow_name = "workflow_api.json"
    with open(workflow_name, "r", encoding="utf-8") as f:
        workflow_data = f.read()

    workflow = json.loads(workflow_data)
    # theme_prompt = "ancient roman"
    # landmark_type = "post office building"
    # landmark_type = "student union building"
    # theme_prompt = "meanacing architecture"
    # theme_prompt = "illustration"
    # theme_prompt = "americana"
    lora_clip_strength = 0.7
    additional_text = ""
    if theme_prompt == "modernist architecture":
        lora_name = "AuthoritarianArchitecture(AD).safetensors"
        lora_clip_strength = 0.7
    if theme_prompt == "ancient roman":
        additional_text = ", year 20 AD"
        lora_clip_strength = 0.75
        lora_name = "RomanArchitecture-10.safetensors"
    if theme_prompt == "illustration":
        lora_name = "illustratearchitecture.safetensors"
        lora_clip_strength = 0.6
    if theme_prompt == "americana":
        lora_name = "AmericanaArchitecture-10.safetensors"
        lora_clip_strength = 0.7


    #set the text prompt for our positive CLIPTextEncode
    workflow["21"]["inputs"]["text"]  = "(masterpiece:1.2), (best quality,:1.2), 8k, HDR, ultra detailed, " + theme_prompt + additional_text +", " + landmark_type + ", blue sky"
    workflow["12"]["inputs"]["text"]  = "embedding:easynegative, watermark, text, (cars)"

    seed = random.randint(1, 9999999999)
    #set the image name for our LoadImage node
    workflow["15"]["inputs"]["image"] = comfyui_path_image
    
    #set model
    workflow["10"]["inputs"]["ckpt_name"] = model_name

    # workflow["14"]["inputs"]["denoise"] = 0.4
    workflow["14"]["inputs"]["denoise"] = 0.25

    workflow["20"]["inputs"]["lora_name"] = lora_name
    workflow["20"]["inputs"]["strength_clip"] = lora_clip_strength

    # num_images = 3
    # workflow["31"]["inputs"]["amount"] = num_images

    ws = websocket.WebSocket()
    image_paths = []

    # loop for num_images times
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    num_images = 1
    for i in range(num_images):
        workflow["14"]["inputs"]["seed"] = seed
        seed += 1
        images = get_images(ws, workflow)

        for node_id in images:
            for image_data in images[node_id]:
                image = Image.open(io.BytesIO(image_data)).convert("RGBA")
                output_path = f"generated/{id}-{sub_id}.png"
                image.save("static/" + output_path)
                image_paths.append(output_path)

    ws.close()
    return image_paths

def composite_images(base_image_path, sub_image_path, id, sub_id, sub_x, sub_y):
    print("Base Image: "+base_image_path)
    
    with open(base_image_path, "rb") as f:
        base_image_path = upload_file(f,"",True)

    print("Sub Image: "+sub_image_path)

    with open(sub_image_path, "rb") as f:
        sub_image_path = upload_file(f,"",True)

    #load workflow from file
    workflow_name = "workflow_compositemap_api.json"
    with open(workflow_name, "r", encoding="utf-8") as f:
        workflow_data = f.read()

    workflow = json.loads(workflow_data)

    workflow["15"]["inputs"]["image"] = base_image_path
    workflow["33"]["inputs"]["image"] = sub_image_path
    workflow["36"]["inputs"]["x"] = sub_x
    workflow["36"]["inputs"]["y"] = sub_y

    ws = websocket.WebSocket()
    image_paths = []

    # loop for num_images times
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))

    images = get_images(ws, workflow)

    for node_id in images:
        for image_data in images[node_id]:
            image = Image.open(io.BytesIO(image_data)).convert("RGBA")
            output_path = f"generated/composited_map-{id}-{sub_id}.png"
            image.save("static/" + output_path)
            image_paths.append("static/" + output_path)

    ws.close()
    return image_paths

def final_pass(base_image_path, id):

    print(base_image_path)

    # base_image = Image.open(base_image_path)
    with open(base_image_path, "rb") as f:
        base_image_path = upload_file(f,"",True)


    #load workflow from file
    workflow_name = "workflow_finalpass_api.json"
    with open(workflow_name, "r", encoding="utf-8") as f:
        workflow_data = f.read()

    workflow = json.loads(workflow_data)

    workflow["15"]["inputs"]["image"] = base_image_path
    

    ws = websocket.WebSocket()
    image_paths = []

    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))

    images = get_images(ws, workflow)

    for node_id in images:
        for image_data in images[node_id]:
            image = Image.open(io.BytesIO(image_data)).convert("RGBA")
            output_path = f"generated/composited_map_final-{id}.png"
            image.save("static/" + output_path)
            image_paths.append(output_path)

    ws.close()
    return image_paths

def create_map_background(id, theme_prompt):
    print("Creating map background")
    additional_text = ""
    if theme_prompt == "modernist architecture":
        lora_name = "AuthoritarianArchitecture(AD).safetensors"
        lora_clip_strength = 0.7
    if theme_prompt == "ancient roman":
        additional_text = ", year 20 AD"
        lora_clip_strength = 0.75
        lora_name = "RomanArchitecture-10.safetensors"
    if theme_prompt == "illustration":
        lora_name = "illustratearchitecture.safetensors"
        lora_clip_strength = 0.6
    if theme_prompt == "americana":
        lora_name = "AmericanaArchitecture-10.safetensors"
        lora_clip_strength = 0.7

    #load workflow from file
    workflow_name = "workflow_bigmap_api.json"
    with open(workflow_name, "r", encoding="utf-8") as f:
        workflow_data = f.read()

    workflow = json.loads(workflow_data)
    positive_prompt = "(masterpiece:1.2), (best quality,:1.2), 8k, HDR, aesthetically pleasing, map of a large area, arial, (high up),"+ additional_text+", RPG map, mostly land, single river from north to south, trees, board game style"

    negative_prompt = "embedding:easynegative, watermark, blurry, text, cars, ocean, mostly empty, (buildings), empty space"
    seed = random.randint(1, 9999999999)
    workflow["14"]["inputs"]["seed"] = seed

    workflow["21"]["inputs"]["text"] = positive_prompt
    workflow["12"]["inputs"]["text"] = negative_prompt
    # workflow["20"]["inputs"]["lora_name"] = lora_name !!find the correct node id
    # workflow["20"]["inputs"]["strength_clip"] = lora_clip_strength
    

    ws = websocket.WebSocket()
    image_paths = []

    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))

    images = get_images(ws, workflow)

    for node_id in images:
        for image_data in images[node_id]:
            image = Image.open(io.BytesIO(image_data)).convert("RGBA")
            output_path = f"generated/background_map-{id}.png"
            image.save("static/" + output_path)
            image_paths.append(output_path)

    ws.close()
    return image_paths

def create_placeholder(id, theme_prompt):
    print("Creating placeholder image")
    additional_text = ""
    if theme_prompt == "modernist architecture":
        lora_name = "AuthoritarianArchitecture(AD).safetensors"
        lora_clip_strength = 0.7
    if theme_prompt == "ancient roman":
        additional_text = ", year 20 AD"
        lora_clip_strength = 0.75
        lora_name = "RomanArchitecture-10.safetensors"
    if theme_prompt == "illustration":
        lora_name = "illustratearchitecture.safetensors"
        lora_clip_strength = 0.6
    if theme_prompt == "americana":
        lora_name = "AmericanaArchitecture-10.safetensors"
        lora_clip_strength = 0.7

    #load workflow from file
    workflow_name = "workflow_questionmark_api.json"
    with open(workflow_name, "r", encoding="utf-8") as f:
        workflow_data = f.read()

    workflow = json.loads(workflow_data)
    positive_prompt = "(masterpiece:1.2), (best quality,:1.2), 8k, HDR, aesthetically pleasing, (giant floating red question mark), " + additional_text

    negative_prompt = "embedding:easynegative, watermark, blurry, reflections"
    seed = random.randint(1, 9999999999)
    workflow["14"]["inputs"]["seed"] = seed

    workflow["21"]["inputs"]["text"] = positive_prompt
    workflow["12"]["inputs"]["text"] = negative_prompt

    workflow["20"]["inputs"]["lora_name"] = lora_name
    workflow["20"]["inputs"]["strength_clip"] = lora_clip_strength
    

    ws = websocket.WebSocket()
    image_paths = []

    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))

    images = get_images(ws, workflow)

    for node_id in images:
        for image_data in images[node_id]:
            image = Image.open(io.BytesIO(image_data)).convert("RGBA")
            output_path = f"generated/questionmark-{id}.png"
            image.save("static/" + output_path)
            image_paths.append(output_path)

    ws.close()
    return image_paths