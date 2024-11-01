import json
import pickle
# Read JSON data from a file
with open('WLASL_v0.3.json', 'r') as file:
    data = json.load(file)

# Create a dictionary with gloss as the key and the first video_id as the value
gloss_video_ids = {item["gloss"]: item["instances"][0]["video_id"] for item in data}

# Print the dictionary
print(gloss_video_ids)

with open('video_ids.pkl', 'wb') as f:
    pickle.dump(gloss_video_ids, f)