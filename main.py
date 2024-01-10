import requests
import json
import os
from html2image import Html2Image
hti = Html2Image(size=(1087, 507), output_path='results')

mapID = input("Enter the map ID: ")

base_url = "https://beatsaver.com/api"

path = "results"

# Ask the beat saver api for the infos of a map based on the id given
response = requests.get(f'{base_url}/maps/id/{mapID}')

# Check whether the specified path exists or not
isExist = os.path.exists(path)
#printing if the path exists or not
if not isExist:

   # Create a new directory because it does not exist
   os.makedirs(path)
   print("\nThe directory 'results' was created.\n")

# If the api response is 200 (OK), then write the whole map infos to data.json. Else, print an error with the code.
if response.status_code == 200:
    data = response.json()
    with open('results/generated_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    print('Map informations saved here: results/generated_data.json!\n')
else:
    print('Request Error', response.status_code)

print('Preparing the HTML file... \n')
with open('results/generated_data.json', 'r') as f:
    data = json.load(f)

# Main elements
bs_id = data['id']
# bs_songName = data['metadata']['songName']
bs_name = data['name']
bs_songSubName = data['metadata']['songSubName']
bs_description = data['description']
bs_mapduration = data['metadata']['duration']
bs_coverURL = data['versions'][0]['coverURL']
bs_uploader = data['uploader']
bs_uploaded = data['uploaded']
#bs_tags = data['tags']

# Ranking info
bs_ranked = data['ranked']
bs_qualified = data['qualified']

# Technical Info
bs_automapper = data['automapper']
bs_declaredAi = data['declaredAi']
bs_bookmarked = data['bookmarked']

# Other dates
bs_createdAt = data['createdAt']
bs_updatedAt = data['updatedAt']
bs_lastPublishedAt = data['lastPublishedAt']

# Secondary Elements
bs_uploader_id = data['uploader']['id']
bs_uploader_name = data['uploader']['name']
bs_metadata_bpm = data['metadata']['bpm']

# # Read the HTML file
# with open('mapimage.html', 'r') as file:
#     html_content = file.read()

# # Write the content to a new file
# with open('results/generated_page.html', 'w') as file:
#     file.write(html_content)

# The whole html it's gonna write (using mapimage.css)!
with open('results/generated_page.html', 'w') as f:
    f.write(f"""
<!DOCTYPE html>
<head>
    <link rel="stylesheet" href="mapimage.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Teko">
</head>

<body>
    <div class="container">
        <div class="image">
            <img src="{bs_coverURL}" alt="">
        </div>

        <div class="info">
            <h1 class="mapname">{bs_name}</h1>

            <br>
            
            <h2>Mapped by </h2> <a href="https://beatsaver.com/profile/{bs_uploader_id}"><h2>{bs_uploader_name}</h2></a>
            
            <br>

            <h2>Map ID: </h2><h2>{bs_id}</h2>
        </div>
    </div>
</body>

</html>
               """)
print('HTML file saved here: results/generated_page.html! \n')

with open('results/generated_page.html', 'r') as f:
    html = f.read()
    
with open('mapimage.css', 'r') as f:
    css = f.read()

print('Converting HTML to PNG... \n')
# Screenshot an HTML (CSS is optional)
hti.screenshot(html_str=html, css_str=css, save_as='generated_image.png')

#print('HTML converted to png and saved here: results/generated_image.png!')

# Wonderfull! Now you are left with your picture, your html for the picture and the json.