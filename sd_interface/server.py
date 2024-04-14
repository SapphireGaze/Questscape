from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from typing import Optional
import os
import websocket
import uuid
import json
import urllib.request
import urllib.parse
import requests
from pydantic import BaseModel
import img_endpoint
import shutil
from PIL import Image
import get_composite_images_upscaled 
import io
import json
from fastapi.middleware.cors import CORSMiddleware

# FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount the generated images directory
# app.mount("/generated", StaticFiles(directory="generated"), name="generated")

# Optionally, create a redirect from /demo.html to /static/demo.html
@app.get("/demo.html")
async def redirect_demo_html():
    return RedirectResponse(url="/static/demo.html")

# Define a request model for your API
class GenerateRequest(BaseModel):
    base_image: Optional[str] = None
    id: Optional[str] = "1"
    sub_id: Optional[str] = "1"
    landmark_type: Optional[str] = "post office building"
    theme_prompt: Optional[str] = "americana"
    num_images: Optional[int] = 1
    mode: Optional[str] = "fast"

@app.post("/get-map/")
async def get_map(
    id: str = Form("1")):
    if not os.path.exists(f"static/generated/composited_map_final-{id}.png"):
        print(f"Creating map background image for {id}")
        # base_image_path = "static/" + img_endpoint.create_map_background(id, "americana")[0]
        base_image_path = f"static/generated/composited_map_final-661bc17b0b06c14495d10159.png"
    else:
        base_image_path = f"static/generated/composited_map_final-{id}.png"
    
    return JSONResponse(content={"status": "success", "image": base_image_path})
    

# POST endpoint for generating images
@app.post("/generate-images/")
async def generate_images(
    image: UploadFile = File(...),
    id: str = Form("1"),
    sub_id: str = Form("1"),
    landmark_type: str = Form("post office building"),
    theme_prompt: str = Form("americana"),
    num_images: int = Form(1),
    mode: str = Form("fast")):
    # Save the uploaded image to a directory
    file_path = f"imports/{image.filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Call the generate function
    try:
        generated_image_paths = img_endpoint.generate(
            base_image=file_path,
            id=id,
            sub_id=sub_id,
            landmark_type=landmark_type,
            theme_prompt=theme_prompt,
            num_images=num_images,
            mode=mode
        )
        # For demonstration, returning JSON with the list of image paths
        for generated_image_path in generated_image_paths:
            generated_image_path = generated_image_path.replace("generated/", "http://host.zzimm.com:8080/static/generated/")
        return JSONResponse(content={"status": "success", "images": "static/"+generated_image_paths[0]})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/composite-images/")
async def composite_images(
    
    id: str = Form("1"),
    theme_prompt: str = Form("americana"),
    ):

    post_data = {
        "waypoints": [{"latitude": 39.5291, "longitude": -119.8146, "clue": "Eldorado", "_id": "661acbbf944eaed13d747eb0"}, {"latitude": 39.5445, "longitude": -119.8159, "clue": "Student Union", "_id": "661acbbf944eaed13d747eb1"}, {"latitude": 39.5247, "longitude": -119.8116, "clue": "Post Office", "_id": "661acbbf944eaed13d747eb2"}, {"latitude": 39.5287, "longitude": -119.808, "clue": "Ballpark", "_id": "661acbbf944eaed13d747eb3"}],
    }
    headers = {'Content-Type': 'application/json'}
    # response = requests.post(f"http://127.0.0.1:8081/v1/api/create/", json=post_data, headers=headers)
    # print(response.text)
    
    api_data = requests.get(f"http://127.0.0.1:8081/v1/api/play/{id}")
    # Simulate reading the JSON data from a database or an API response
#     api_data = """
# {
#   "_id": "661acbbf944eaed13d747eae",
#   "waypoints": [
#     {"latitude": 39.5291, "longitude": -119.8146, "clue": "Eldorado", "_id": "661acbbf944eaed13d747eb0"},
#     {"latitude": 39.5445, "longitude": -119.8159, "clue": "Student Union", "_id": "661acbbf944eaed13d747eb1"},
#     {"latitude": 39.5247, "longitude": -119.8116, "clue": "Post Office", "_id": "661acbbf944eaed13d747eb2"},
#     {"latitude": 39.5287, "longitude": -119.8080, "clue": "Ballpark", "_id": "661acbbf944eaed13d747eb3"}
#   ], "__v": 0
# }
# """
    data = json.loads(api_data.text)
    id = data["_id"]
    coord_list = []
    image_path_list = []
    for waypoint in data["waypoints"]:
        coord_list.append((waypoint["latitude"], waypoint["longitude"]))
        
        # Use the inner "_id" for image path
        waypoint_id = waypoint["_id"]
        image_path = f"static/generated/{id}-{waypoint_id}.png"
        image_path_list.append(image_path)
        
        print(f"Waypoint ID: {waypoint_id}, Image Path: {image_path}")

    try:
        generated_image_path = get_composite_images_upscaled.generate(id, coord_list, image_path_list, theme_prompt)
        return JSONResponse(content={"status": "success", "image": "static/"+generated_image_path[0]})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Running Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
