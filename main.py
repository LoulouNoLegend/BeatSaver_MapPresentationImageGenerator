import requests
import json
import os
from html2image import Html2Image

hti = Html2Image(size=(1086, 506), output_path='results')

choosedDifficulty = -1

base_url = "https://beatsaver.com/api"

path = "results"

# Ask the ID of the map to the user
choosedID = input("Enter the map ID: ")

# Ask the beat saver api for the infos of a map based on the id given
response = requests.get(f'{base_url}/maps/id/{choosedID}')

# Check whether the specified path exists or not
isExist = os.path.exists(path)

#printing if the path exists or not
if not isExist:
   # Create a new directory because it does not exist
   os.makedirs(path)
   print("\nFolder 'results' created.\n")

# If the api response is 200 (OK), then write the whole map infos to data.json. Else, print an error with the code.
if response.status_code == 200:
    data = response.json()
    with open('results/generated_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    print('\nMap informations saved!')
else:
    print('Request Error', response.status_code, '. Please retry.')
    exit()

print('\nPreparing the HTML file... \n')
with open('results/generated_data.json', 'r') as f:
    data = json.load(f)

showDifficulty = input("Do you want to show a certain difficulty with the informations related to it? (y/n) ")

# Get difficulties
diffs = data['versions'][0]['diffs']

# See how many difficulties there is
num_of_choosedDifficulty = len(diffs)
#print("Il y a {} éléments dans 'diffs', donc 'choosedDifficulty' peut être de 0 à {}.".format(num_of_choosedDifficulty, num_of_choosedDifficulty-1))

# Ask the user the difficulty of the map if the person said yes (but if there's only one difficulty, it'll show it as default). Else, don't ask or re-ask if he answered wrong.
if showDifficulty == 'y':
    if num_of_choosedDifficulty == 1:
        print("\nOnly one difficulty was detected, it will be used for the image. (" + data['versions'][0]['diffs'][0]['difficulty'] + ")")
    else:
        print("\nDifficulties: ")
        for i in range(num_of_choosedDifficulty):
            difficulty_name = diffs[i]['difficulty']
            print("{}: {}".format(i, difficulty_name))
        while True:
            choosedDifficulty = input("\nDifficulty to show: ")
            if choosedDifficulty.isdigit() and 0 <= int(choosedDifficulty) < num_of_choosedDifficulty:
                choosedDifficulty = int(choosedDifficulty)
                break
            else:
                print("Invalid input. Please enter a number between 0 and {}.".format(num_of_choosedDifficulty-1))
    print("\nConfiguration finished.")

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

# Difficulty info
bs_notes = data['versions'][0]['diffs'][choosedDifficulty]['notes']
bs_bombs = data['versions'][0]['diffs'][choosedDifficulty]['bombs']
bs_obstacles = data['versions'][0]['diffs'][choosedDifficulty]['obstacles']
bs_njs = data['versions'][0]['diffs'][choosedDifficulty]['njs']
bs_nps = data['versions'][0]['diffs'][choosedDifficulty]['nps']
bs_lights = data['versions'][0]['diffs'][choosedDifficulty]['events']
bs_difficultyname = data['versions'][0]['diffs'][choosedDifficulty]['difficulty']

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

# The whole html it's gonna write (using mapimage.css) based on if you choosed to show a difficulty or not
if showDifficulty == 'y':
    with open('results/generated_page.html', 'w') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Image</title>

    <link rel="stylesheet" href="mapimage.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Teko">
</head>

<body>
    <div class="container">
        <div class="cover">
            <img src="{bs_coverURL}" alt="">
        </div>

        <div class="info">
            <h1 class="mapname">{bs_name}</h1>
            
            <h2>Mapped by </h2> <a href=""><h2>{bs_uploader_name}</h2></a>

            <br>

            <h2>Map ID: </h2><h2>{bs_id}</h2>
            
            <div class="difficulty_info">
                <div class="di_1">
                    <p class="difftitle"> {bs_difficultyname}</p>
                </div>

                <div class="di_2">
                    <p class="notes"> Notes: {bs_notes}</p>
                    <p class="njs"> NJS: {bs_njs}</p>
                </div>
                
                <div class="di_3">
                    <p class="bombs"> Bombs: {bs_bombs}</p>
                    <p class="nps"> NPS: {bs_nps}</p>
                </div>

                <div class="di_4">
                    <p class="obstacles"> Obstacles: {bs_obstacles}</p>
                    <p class="lights"> Lights: {bs_lights}</p>
                </div>
            </div>
            
        </div>
    </div>
</body>

</html>""")
else:
    with open('results/generated_page.html', 'w') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Image</title>

    <link rel="stylesheet" href="mapimage.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Teko">
</head>

<body>
    <div class="container">
        <div class="cover">
            <img src="{bs_coverURL}" alt="">
        </div>

        <div class="info">
            <h1 class="mapname">{bs_name}</h1>
            
            <h2>Mapped by </h2> <a href=""><h2>{bs_uploader_name}</h2></a>

            <br>

            <h2>Map ID: </h2><h2>{bs_id}</h2>
        </div>
    </div>
</body>

</html>""")
        
print('\nHTML file saved! \n')

with open('results/generated_page.html', 'r') as f:
    html = f.read()
    
with open('mapimage.css', 'r') as f:
    css = f.read()

print('Converting HTML to PNG... \n')
# Screenshot an HTML (CSS is optional)
hti.screenshot(html_str=html, css_str=css, save_as='generated_image.png')

input("""\nConversion successfull! \nEvery files can be found in the results folder!
Press enter to close the program.""")

#print('HTML converted to png and saved here: results/generated_image.png!')

# Wonderfull! Now you are left with your picture, your html for the picture and the json.