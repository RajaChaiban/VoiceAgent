# VoiceAI - OBGYN Clinic Voice Assistant

An AI-powered voice assistant for Women's Care Ashburn that handles patient inquiries, appointment scheduling, emergency triage, and call routing using Deepgram's speech-to-speech API with GPT-4o-mini.

## Features

- **Voice-First Design**: Natural conversation with patients via phone
- **Emergency Detection**: Automatic routing for severe medical situations (bleeding, chest pain, fainting)
- **Intelligent Triage**: Categorizes calls into emergency, urgent, or routine care pathways
- **Appointment Scheduling**: Patients can book appointments directly with the AI
- **Live Agent Transfer**: Seamless transfer to human agents when needed
- **HIPAA-Compliant Architecture**: All calls recorded securely for training and verification

## Tech Stack

- **Language**: Python 3.13+
- **Speech Recognition**: Deepgram Nova-3 (STT)
- **Language Model**: OpenAI GPT-4o-mini
- **Text-to-Speech**: Deepgram Aura-2-Thalia-En
- **WebSocket**: Python websockets library
- **Audio Format**: mulaw 8kHz (Twilio compatible)

## Prerequisites

- Python 3.13 or higher
- Deepgram API key ([Get it here](https://console.deepgram.com))
- Twilio account with a phone number (for production)
- ngrok (for local development/testing)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/voice-ai.git
   cd voice-ai
   ```

2. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env and add your Deepgram API key
   # DEEPGRAM_API_KEY=your_actual_api_key
   ```

3. **Install dependencies**
   ```bash
   # Using pip
   pip install -r requirements.txt

   # Or using uv (faster)
   uv sync
   ```

4. **Start the WebSocket server**
   ```bash
   python main.py
   ```

   You should see:
   ```
   Started server.
   ```

## Development Setup (Local Testing)

### Using ngrok to expose localhost

1. **Start ngrok** (in another terminal)
   ```bash
   ngrok http 5000
   ```

   Note the URL: `https://abc123.ngrok.io`

2. **Configure Twilio webhook**
   - Go to Twilio Console
   - Select your phone number
   - Set Voice webhook to: `https://YOUR_NGROK_URL/`
   - Method: POST
   - Protocol: WebSocket

3. **Start your application**
   ```bash
   python main.py
   ```

4. **Make a test call** to your Twilio number

## Project Structure

```
voice-ai/

