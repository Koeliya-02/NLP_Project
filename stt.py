
import speech_recognition as sr
import pyaudio
import nltk
import pickle 
import sys
from moviepy.editor import VideoFileClip, concatenate_videoclips
nltk.download('punkt')
nltk.download('stopwords')

# stop_words = set(stopwords.words('english'))

def speech_to_text():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Use the microphone as source for input
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        print("Listening... Please speak.")

        # Capture the audio from the microphone
        audio = recognizer.listen(source)

        try:
            # Convert speech to text using Google Speech Recognition
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")

            # Save the text to a file
            with open("output.txt", "w") as file:
                file.write(text)
            print("Text saved to 'output.txt'")

            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")

if __name__ == "__main__":
    # Run the speech-to-text function and store the output
    output_text = speech_to_text()

    if output_text:
        print("Final output: ", output_text)
if output_text == None:
    sys.exit()
    
    
#tokenise the output and find if it is in the bag_of_words

with open('bag_of_words.pkl', 'rb') as f:
    bag_of_words = pickle.load(f)
tokens = nltk.tokenize.word_tokenize(output_text, language='english', preserve_line=False)
# filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

fl =0
final_tokens=[]
for each_token in tokens:
    if not(each_token in bag_of_words):
        fl=1
    else:
        final_tokens.append(each_token.lower())
        
with open('video_ids.pkl', 'rb') as f:
    videos_ID = pickle.load(f)

videos =[]
directory= "videos/"
extension = ".mp4"
for each_token in final_tokens:
    video_path = directory + videos_ID[each_token] + extension
    print(video_path)
    video = VideoFileClip(video_path)
    
    videos.append(video)
    
# Concatenate the video clips end-to-end
final_video = concatenate_videoclips(videos)

# Write the result to a file
final_video.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac")

if(fl==0):
    print("text has been successfully converted to sign language")