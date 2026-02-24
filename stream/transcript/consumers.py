import whisper
import tempfile
import os
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

model = whisper.load_model("base")

class TranscriptConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        print("WebSocket connected")

    async def receive(self, bytes_data=None, text_data=None):

        if bytes_data:
            print("Received bytes:", len(bytes_data))   

            loop = asyncio.get_event_loop()

            transcript = await loop.run_in_executor(None, self.transcribe_audio, bytes_data)
            
            print("Transcription done:", transcript)   

            await self.send(text_data=transcript)

    def transcribe_audio(self, audio_bytes):
        print("Saving temp file...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
            f.write(audio_bytes)
            temp_path = f.name
            print("Temp file path:", temp_path)

        try: 
            print("Running Whisper...")
            result = model.transcribe(temp_path, language="en")
            return result["text"]
        finally:
            os.remove(temp_path)

    async def disconnect(self, close_code):
        print("WebSocket disconnected")