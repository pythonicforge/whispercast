# from cartesia import Cartesia
# from cartesia.tts import OutputFormat_Raw, TtsRequestIdSpecifier
# from dotenv import load_dotenv
# import os
# from pydub import AudioSegment

# load_dotenv()

# client = Cartesia(
#     api_key=os.getenv('API_KEY')
# ,
# )

# content = "Hey everyone! Welcome to WhisperCast. Today we are talking  about  a famous cricket personality, whom every Indian Cricket fan is aware of. We know him for his swags, cool mindset and immense hard hitting cricket shots. We are talking about none other than Hardik Pandya. Hardik Himanshu Pandya (born 11 October 1993) is an Indian international cricketer who plays for the Indian cricket team. He is an all-rounder who is a right-handed middle order batsman and fast-medium bowler. He is considered one of the best all-rounders in the world in white-ball cricket. Pandya has represented India in all three formats. He captains Mumbai Indians in the Indian Premier League and occasionally plays for Baroda in domestic cricket. He has captained the Indian team in white-ball cricket and was the vice captain of the team that won the 2024 T20 World Cup."
# audio_bytes = client.tts.bytes(
#     model_id="sonic-2",
#     transcript=content,
#     voice={
#         "mode": "id",
#         "id": "694f9389-aac1-45b6-b726-9d9369183238",
#     },
#     language="en",
#     output_format= {
#         "container": "mp3",
#         "bit_rate": 128000,
#         "sample_rate": 44100
#         },
#     speed= "normal"
# )

# with open("output.mp3", "wb") as f:
#     for chunk in audio_bytes:
#         f.write(chunk)

# print("✅ MP3 saved as output.mp3")

# intro = AudioSegment.from_mp3("intro.mp3")
# voice = AudioSegment.from_mp3("output.mp3")

# intro = intro.fade_out(1500)
# # Stitch together
# final = intro + voice

# # Export the final podcast
# final.export("final_podcast.mp3", format="mp3")

# print("🎧 Podcast saved as final_podcast.mp3")