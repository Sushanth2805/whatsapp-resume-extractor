
```markdown
# 📱 WhatsApp Resume Extractor

An automated system that receives resumes via WhatsApp, extracts structured data using AI, and stores them in Google Sheets.

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd clg_assignment
   ```

2. **Install dependencies**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Setup environment**
   - Copy `env_template.txt` to `.env`
   - Fill in your API credentials
   - Place `credentials.json` in project root

4. **Initialize Google Sheets**
   ```bash
   python sheets_handler.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

## 📋 Requirements

- Python 3.8+
- Twilio account
- Google Gemini API key
- Google Cloud project with Sheets API enabled
- ngrok (for local testing)

## 🛠️ Tools Used

• **Twilio WhatsApp API** - Message handling
• **Google Gemini AI** - Data extraction  
• **Google Sheets API** - Data storage
• **Flask** - Web framework
• **ngrok** - Local tunneling
• **Python** - Backend language

## 🎯 Features

- ✅ Multi-format support (text, PDF, images)
- ✅ Real-time processing (3-5 seconds)
- ✅ Structured data extraction
- ✅ Automatic Google Sheets storage
- ✅ WhatsApp confirmation messages

## 📊 Data Extracted

- Personal information (name, email, phone)
- Professional details (LinkedIn, experience, education)
- Skills and summary
- Timestamp and status

## 🔧 Configuration

Create `.env` file with:
```
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
GEMINI_API_KEY=your_gemini_key
GOOGLE_SHEETS_ID=your_sheet_id
```

## 📖 Usage

1. Send resume as text message or file attachment to Twilio WhatsApp number
2. System automatically extracts and stores data
3. Receive confirmation with extracted information

## 📁 Project Structure

```
clg_assignment/
├── app.py                 # Main Flask application
├── extract_resume.py      # AI extraction logic
├── sheets_handler.py      # Google Sheets integration
├── requirements.txt       # Python dependencies
├── SETUP_GUIDE.md         # Detailed setup instructions        
```
## 📝 Documentation

- [Setup Guide](SETUP_GUIDE.md) - Detailed installation steps
  
## 📄 License

MIT License - see LICENSE file for details
```

This README is clean, professional, and covers all the essential information someone would need to understand and use your project!
