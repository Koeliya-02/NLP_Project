# import json
# import pickle
# # Read JSON data from a file
# with open('WLASL_v0.3.json', 'r') as file:
#     data = json.load(file)

# # Create a dictionary with gloss as the key and the first video_id as the value

# gloss_video_ids = {item["gloss"]: item["instances"][0]["video_id"] for item in data}

# # Print the dictionary
# print(gloss_video_ids)

# with open('video_ids.pkl', 'wb') as f:
#     pickle.dump(gloss_video_ids, f)

import json
import pickle

# Read JSON data from a file
with open('WLASL_v0.3.json', 'r') as file:
    data = json.load(file)

# Read missing video_ids from a text file
with open('missing.txt', 'r') as file:
    missing_video_ids = set(line.strip() for line in file)

# Create a dictionary with gloss as the key and the first video_id not in the missing list as the value
gloss_video_ids = {}

for item in data:
    gloss = item["gloss"]
    for instance in item["instances"]:
        video_id = instance["video_id"]
        if video_id not in missing_video_ids:
            gloss_video_ids[gloss] = video_id
            break

# Print the dictionary
print(gloss_video_ids)

# Save the dictionary to a pickle file
with open('video_ids.pkl', 'wb') as f:
    pickle.dump(gloss_video_ids, f)
