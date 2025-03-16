# Configurations 

import os
from dotenv import load_dotenv

load_dotenv()

hugging_face_token=os.getenv("hugging_face_token")
Gemini_key=os.getenv("Gemini_key")

news="DB/News.txt"