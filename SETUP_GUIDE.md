# 🚀 Quick Setup Guide - Step by Step

Follow these steps **in order** to get your WhatsApp Resume Extractor running.

---

## ✅ CHECKLIST

- [ ] Python 3.8+ installed
- [ ] Downloaded ngrok
- [ ] Twilio account created
- [ ] Gemini API key obtained
- [ ] Google Cloud project created
- [ ] Google Sheet created

---

## 📋 STEP-BY-STEP INSTRUCTIONS

### **STEP 1: Install Python (if not installed)**

1. Download from https://www.python.org/downloads/
2. During installation, **CHECK** "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   ```

---

### **STEP 2: Get Twilio Credentials**

1. Go to https://www.twilio.com/try-twilio
2. Sign up with email (free $15 credit)
3. After signup, go to **Console Dashboard**
4. **Copy these values:**
   - Account SID (starts with `AC...`)
   - Auth Token (click to reveal)
5. Go to **Messaging** → **Try it Out** → **Send a WhatsApp message**
6. Follow instructions to join sandbox
7. **Copy:** Twilio WhatsApp Number (e.g., `whatsapp:+14155238886`)

**Keep these values handy!**

---

### **STEP 3: Get Gemini API Key**

1. Go to https://ai.google.dev/
2. Click **"Get API Key"** (top right)
3. Sign in with Google account
4. Click **"Create API Key"**
5. **Copy** the API key (starts with `AIzaSy...`)

**Save this key!**

---

### **STEP 4: Setup Google Sheets**

#### A. Enable Google Sheets API

1. Go to https://console.cloud.google.com/
2. Create new project: Name it "Resume Extractor"
3. Once created, click **"Enable APIs and Services"**
4. Search for **"Google Sheets API"** → Enable
5. Search for **"Google Drive API"** → Enable

#### B. Create OAuth Credentials

1. In Google Cloud Console, go to **APIs & Services** → **Credentials**
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. If prompted, configure consent screen:
   - User Type: **External**
   - App name: "Resume Extractor"
   - Your email in required fields
   - Save and continue through all steps
4. Back to Create OAuth client ID:
   - Application type: **Desktop app**
   - Name: "Resume Extractor Desktop"
   - Click **Create**
5. **Download JSON** file
6. Rename it to `credentials.json`

#### C. Create Google Sheet

1. Go to https://sheets.google.com/
2. Create a **new blank spreadsheet**
3. Name it "Resume Data"
4. In the first sheet, rename it to **"Resumes"** (bottom tab)
5. **Copy the Sheet ID** from URL:
   ```
   https://docs.google.com/spreadsheets/d/COPY_THIS_PART_HERE/edit
   ```

**Save the Sheet ID!**

---

### **STEP 5: Download ngrok**

1. Go to https://ngrok.com/download
2. Download for Windows
3. Extract `ngrok.exe` to `C:\ngrok`
4. (Optional) Sign up at ngrok.com and get authtoken:
   ```bash
   cd C:\ngrok
   ngrok config add-authtoken YOUR_TOKEN
   ```

---

### **STEP 6: Setup Project**

1. Open **Command Prompt**
2. Navigate to project folder:

   ```bash
   cd C:\Users\sri_j\OneDrive\Desktop\clg_assignment
   ```

3. Create virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate virtual environment:

   ```bash
   venv\Scripts\activate
   ```

   You should see `(venv)` in your prompt

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   This will take 2-3 minutes

---

### **STEP 7: Configure Environment Variables**

1. Create a file named `.env` in your project folder
2. Copy content from `env_template.txt`
3. Fill in your actual values:

   ```
   TWILIO_ACCOUNT_SID=AC123abc456def...
   TWILIO_AUTH_TOKEN=your_actual_token
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   GEMINI_API_KEY=AIzaSy123abc456def...
   GOOGLE_SHEETS_ID=1a2b3c4d5e6f7g8h9i0j
   ```

4. **Place `credentials.json`** (from Step 4B) in project root folder

Your folder should look like:

```
clg_assignment/
├── app.py
├── extract_resume.py
├── sheets_handler.py
├── requirements.txt
├── .env                    ← You created this
├── credentials.json        ← You placed this
├── env_template.txt
├── venv/
└── README.md
```

---

### **STEP 8: Initialize Google Sheets**

1. In Command Prompt (with venv activated):

   ```bash
   python sheets_handler.py
   ```

2. Browser will open automatically
3. **Select your Google account**
4. Click **"Allow"** (it's safe, it's your own app)
5. You should see:

   ```
   ✅ Connected to Google Sheet
   ✅ Headers created in Google Sheet
   ```

6. Check your Google Sheet - it should now have headers!

---

### **STEP 9: Start the Server**

Open **TWO** Command Prompt windows:

#### **Terminal 1: Flask App**

```bash
cd C:\Users\sri_j\OneDrive\Desktop\clg_assignment
venv\Scripts\activate
python app.py
```

You should see:

```
🚀 WhatsApp Resume Extractor Starting...
📱 Waiting for WhatsApp messages...
 * Running on http://0.0.0.0:5000
```

#### **Terminal 2: ngrok**

```bash
cd C:\ngrok
ngrok http 5000
```

You should see:

```
Forwarding    https://abc123def456.ngrok.io -> http://localhost:5000
```

**Copy the `https://...ngrok.io` URL**

---

### **STEP 10: Configure Twilio Webhook**

1. Go to https://console.twilio.com/
2. Navigate to **Messaging** → **Settings** → **WhatsApp Sandbox Settings**
3. Find **"When a message comes in"** field
4. Paste your ngrok URL + `/webhook`:
   ```
   https://abc123def456.ngrok.io/webhook
   ```
5. Method: **HTTP POST**
6. Click **Save**

---

### **STEP 11: Test It!**

1. **Join WhatsApp Sandbox** (if not already):

   - Twilio console shows instructions
   - Send `join [code]` to the sandbox number

2. **Send a test message** to Twilio WhatsApp number:

   ```
   Hi! My name is Sarah Johnson
   Email: sarah.j@example.com
   Phone: +1-555-9876
   Skills: Python, Data Science, SQL
   Experience: 3 years as Data Analyst
   Education: M.S. in Computer Science
   ```

3. **Watch Terminal 1** - you should see:

   ```
   ✅ New WhatsApp Message Received!
   🤖 Extracting resume data with Gemini...
   ✅ Data extracted
   📊 Saving to Google Sheets...
   ✅ Confirmation sent to user
   ```

4. **Check your Google Sheet** - new row should appear!

5. **Check WhatsApp** - you'll get a confirmation message

---

## 🎉 SUCCESS!

You now have a working WhatsApp Resume Extractor!

### **What to do next:**

1. **Test with a PDF resume** - send any resume PDF to WhatsApp
2. **Test with an image** - take a photo of a resume
3. **Record your demo video** (2-3 minutes showing the system working)

---

## 🎥 Demo Video Tips

Show these in your video:

1. ✅ Your Google Sheet (empty at start)
2. ✅ Send a text resume via WhatsApp
3. ✅ Terminal showing processing
4. ✅ Google Sheet auto-populating
5. ✅ Send a PDF resume
6. ✅ WhatsApp confirmation messages
7. ✅ Final Google Sheet with all data

**Recording tools:**

- Windows Game Bar (Win + G) - built-in
- OBS Studio (free) - https://obsproject.com/
- Loom (browser-based) - https://loom.com/

---

## ⚠️ Common Issues

| Problem                  | Solution                                             |
| ------------------------ | ---------------------------------------------------- |
| `pip: command not found` | Python not in PATH, reinstall with PATH option       |
| `Module not found`       | Make sure venv is activated                          |
| No messages received     | Check ngrok URL in Twilio webhook                    |
| Google auth error        | Delete `token.pickle`, run `sheets_handler.py` again |
| Gemini quota exceeded    | Wait a minute, free tier has rate limits             |
| ngrok expired            | Restart ngrok, update Twilio webhook URL             |

---

## 📞 Need Help?

1. Check both terminal windows for error messages
2. Verify all API keys are correct in `.env`
3. Make sure ngrok URL is updated in Twilio (it changes each restart)
4. Check `README.md` for detailed troubleshooting

---

## 🎯 For Your Assignment Submission

Submit these:

1. **APPROACH.md** - Explains your approach and tools (already created)
2. **Demo video** (2-3 minutes) showing the system working
3. **Google Sheet link** (set to "Anyone with link can view")
4. **(Optional) GitHub repo** with code

---

**Good luck with your assignment! 🚀**





