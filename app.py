from flask import Flask, request
from twilio.rest import Client
import os
from dotenv import load_dotenv
from extract_resume import extract_resume_data
from sheets_handler import append_to_sheet
import requests

load_dotenv()

app = Flask(__name__)

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def download_media(media_url):
    """Download media file from Twilio"""
    try:
        response = requests.get(
            media_url,
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
            timeout=30
        )
        if response.status_code == 200:
            return response.content
        return None
    except Exception as e:
        print(f"Error downloading media: {e}")
        return None


@app.route('/webhook', methods=['POST'])
def webhook():
    """Receives WhatsApp messages from Twilio"""
    
    # Get message data
    incoming_msg = request.values.get('Body', '')
    sender = request.values.get('From', '')
    media_url = request.values.get('MediaUrl0', '')
    media_type = request.values.get('MediaContentType0', '')
    
    print(f"\n{'='*60}")
    print(f"✅ New WhatsApp Message Received!")
    print(f"{'='*60}")
    print(f"From: {sender}")
    print(f"Message: {incoming_msg}")
    print(f"Media URL: {media_url}")
    print(f"Media Type: {media_type}")
    print(f"{'='*60}\n")
    
    try:
        # Extract resume data
        media_content = None
        if media_url:
            print("📥 Downloading media file...")
            media_content = download_media(media_url)
        
        print("🤖 Extracting resume data with Gemini...")
        extracted_data = extract_resume_data(incoming_msg, media_content, media_type)
        
        if extracted_data:
            print(f"✅ Data extracted: {extracted_data}")
            
            # Add sender info
            extracted_data['whatsapp_number'] = sender
            
            # Save to Google Sheets
            print("📊 Saving to Google Sheets...")
            append_to_sheet(extracted_data)
            
            # Send success confirmation
            candidate_name = extracted_data.get('name', 'there')
            
            client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                to=sender,
                body=f"Thank you {candidate_name} for sending your resume! 🎉\n\n"
                     f"We have received your application and will review it shortly."
            )
            print("✅ Confirmation sent to user\n")
        else:
            # Send error message
            client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                to=sender,
                body="❌ Sorry, couldn't extract resume data. Please send a clear resume or text with your details."
            )
            print("❌ Extraction failed\n")
            
    except Exception as e:
        print(f"❌ Error processing message: {e}")
        
        # Send error notification
        client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=sender,
            body=f"❌ Error processing your request: {str(e)}"
        )
    
    return '', 200


@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return """
    <html>
        <head><title>WhatsApp Resume Extractor</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>🤖 WhatsApp Resume Extractor</h1>
            <p style="color: green; font-size: 20px;">✅ System is running!</p>
            <hr>
            <p>Send resumes via WhatsApp to automatically extract and store data.</p>
            <p><strong>Powered by:</strong> Twilio + Gemini AI + Google Sheets</p>
        </body>
    </html>
    """, 200


@app.route('/health', methods=['GET'])
def health():
    """Simple health check"""
    return {"status": "healthy", "service": "whatsapp-resume-extractor"}, 200


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 WhatsApp Resume Extractor Starting...")
    print("="*60)
    print("📱 Waiting for WhatsApp messages...")
    print("🔗 Make sure ngrok is running on port 5000")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000, host='0.0.0.0')

