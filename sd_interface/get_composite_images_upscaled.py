import img_endpoint
import os

def lat_lon_to_pixels(lat, lon, min_lat, max_lat, min_lon, max_lon, width, height):
    # Convert latitude and longitude to pixels
    x = (lon - min_lon) / (max_lon - min_lon) * width
    # y = (lat - min_lat) / (max_lat - min_lat) * height
    y = (max_lat - lat) / (max_lat - min_lat) * height
    return x, y

def adjust_for_padding_and_size(x, y, image_width, image_height, map_width, map_height, padding):
    # Adjust for padding
    x_adj = x * (map_width - 2 * padding) / map_width + padding
    y_adj = y * (map_height - 2 * padding) / map_height + padding
    
    # Adjust to position the center of the building image at the coordinate
    x_adj -= image_width / 2
    y_adj -= image_height / 2
    
    return x_adj, y_adj

def find_max_min_lat_lon(coordList):
    max_lat = -1000
    min_lat = 1000
    max_lon = -1000
    min_lon = 1000
    for coord in coordList:
        lat = coord[0]
        lon = coord[1]
        if lat > max_lat:
            max_lat = lat
        if lat < min_lat:
            min_lat = lat
        if lon > max_lon:
            max_lon = lon
        if lon < min_lon:
            min_lon = lon
    return max_lat, min_lat, max_lon, min_lon

def generate(id, coordList, image_path_list, theme_prompt):
    map_resolution = 4096  # Example map size
    building_size = 768    # Building image size
    padding = 768

    if not os.path.exists(f"static/generated/background_map-{id}.png"):
        print(f"Creating map background image for {id} with theme {theme_prompt}")
        base_image_path = "static/" + img_endpoint.create_map_background(id, theme_prompt)[0]
    else:
        base_image_path = f"static/generated/background_map-{id}.png"
    print(f"Map background image path: {base_image_path}")  

    if not os.path.exists(f"static/generated/questionmark-{id}.png"):
        questionmark_path = "static/" + img_endpoint.create_placeholder(id, theme_prompt)[0]
    else:
        questionmark_path = f"static/generated/questionmark-{id}.png"
    # base_image_path = f"background_map-{id}.png"

    for i, coords in enumerate(coordList):
        # Convert real-world coordinates to map pixel coordinates
        max_lat, min_lat, max_lon, min_lon = find_max_min_lat_lon(coordList)
        x_pixel, y_pixel = lat_lon_to_pixels(coords[0], coords[1], min_lat, max_lat, min_lon, max_lon, map_resolution, map_resolution)

        # Adjust for padding and image size
        adj_x, adj_y = adjust_for_padding_and_size(x_pixel, y_pixel, building_size, building_size, map_resolution, map_resolution, padding)

        print(f"Compositing {base_image_path} with {image_path_list[i]}")        

        #check if image_path_list[i] exists on disk, not a placeholder
        if not os.path.exists(image_path_list[i]):
            image_path_list[i] = questionmark_path

        # Composite the images
        image_paths = img_endpoint.composite_images(base_image_path, image_path_list[i], id, str(i), adj_x, adj_y)
        base_image_path = image_paths[0]
    # Final pass
    upscaled_final_image_path = img_endpoint.final_pass(base_image_path, id) 
    return upscaled_final_image_path

# Eldoraodo : 39.52911124124199, -119.81464350282953
# Student Union: 39.544530529209325, -119.81596644482357
# Post Office : 39.52477038568993, -119.81168921141675
# Ballpark: 39.52872911862602, -119.80805431706192