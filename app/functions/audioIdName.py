from elevenlabs import set_api_key
import elevenlabs
import os

api_key_file_path = os.path.join("app/static/files", "ApiKey.txt")

apiKeyFile = ""

if os.path.exists(api_key_file_path):
    with open(api_key_file_path, "r") as f:
        apiKeyFile = f.readline()
else:
    generated_api_key = ""
    os.makedirs("Files", exist_ok=True)
    with open(api_key_file_path, "w") as f:
        f.write(generated_api_key)

if apiKeyFile != "":
    set_api_key(apiKeyFile)

    voices = elevenlabs.voices()
    generated_voices = [voice for voice in voices if voice.category == "generated" or voice.category == "professional"]
    voices_list = [(voice.voice_id, voice.name) for voice in generated_voices]
    stories_list = [name for _, name in voices_list]

else:
    voices_list= ""


# print(voices_list)










# from elevenlabs import set_api_key
# import elevenlabs

# set_api_key("b4f7e53b31d99548b5a46e9b0d1999a8")

# # Fetch the list of voices dynamically
# voices = elevenlabs.voices()

# # Create voices_list with voice_id and name
# voices_list = [(voice.voice_id, voice.name) for voice in voices]

# # Create stories_list with names
# stories_list = [name for _, name in voices_list]

# print(voices_list)