import speech_recognition as sr
import nltk
import pickle
import sys
import cv2
import os

nltk.download('punkt')
nltk.download('stopwords')

# Function for speech recognition
def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... Please speak.")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")

            with open("output.txt", "w") as file:
                file.write(text)
            print("Text saved to 'output.txt'")

            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")

if __name__ == "__main__":
    output_text = speech_to_text()

    if output_text:
        print("Final output: ", output_text)
    if output_text is None:
        sys.exit()

    # Tokenize the output and find if it is in the bag_of_words
    with open('bag_of_words.pkl', 'rb') as f:
        bag_of_words = pickle.load(f)

    tokens = nltk.tokenize.word_tokenize(output_text, language='english', preserve_line=False)

    fl = 0
    final_tokens = []
    for each_token in tokens:
        if each_token not in bag_of_words:
            fl = 1
        else:
            final_tokens.append(each_token.lower())

    with open('video_ids.pkl', 'rb') as f:
        videos_ID = pickle.load(f)

    videos = []
    directory = "videos/"
    extension = ".mp4"
    for each_token in final_tokens:
        video_path = os.path.join(directory, videos_ID[each_token] + extension)
        if not os.path.isfile(video_path):
            print(f"Error: Video file not found: {video_path}")
            continue
        print(video_path)
        videos.append(video_path)

    if not videos:
        print("No valid videos found. Exiting.")
        sys.exit()

    # Define the codec and create a VideoWriter object to write the concatenated video
    output_file = "output_video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Initialize the video writer with properties from the first video
    first_video = cv2.VideoCapture(videos[0])
    if not first_video.isOpened():
        print(f"Error: Cannot open the first video: {videos[0]}")
        sys.exit()

    frame_width = int(first_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(first_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = first_video.get(cv2.CAP_PROP_FPS)
    first_video.release()

    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))
    if not out.isOpened():
        print(f"Error: Cannot open video writer for file: {output_file}")
        sys.exit()

    # Function to write frames from a video capture to the video writer
    def write_frames(video_path, out):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Cannot open video file: {video_path}")
            return
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        cap.release()

    # Write frames from each video to the output video
    for video_path in videos:
        write_frames(video_path, out)

    # Release the video writer
    out.release()
    cv2.destroyAllWindows()

    if fl == 0:
        print("Text has been successfully converted to sign language")
