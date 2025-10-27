from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Google Sheets configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = os.getenv('GOOGLE_SHEETS_ID')

# The range where data will be appended
SHEET_NAME = 'Resumes'  # You can change this
RANGE_NAME = f'{SHEET_NAME}!A:K'  # Columns A through K


def get_sheets_service():
    """Authenticate and return Google Sheets service"""
    creds = None
    
    # Token file stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('sheets', 'v4', credentials=creds)
    return service


def initialize_sheet():
    """Create headers if sheet is empty"""
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        
        # Check if sheet exists and has headers
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f'{SHEET_NAME}!A1:K1'
        ).execute()
        
        values = result.get('values', [])
        
        # If no headers, create them
        if not values:
            headers = [[
                'Timestamp',
                'Name',
                'Email',
                'Phone',
                'LinkedIn',
                'Skills',
                'Experience',
                'Education',
                'Summary',
                'WhatsApp Number',
                'Status'
            ]]
            
            sheet.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=f'{SHEET_NAME}!A1:K1',
                valueInputOption='RAW',
                body={'values': headers}
            ).execute()
            
            print("✅ Headers created in Google Sheet")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing sheet: {e}")
        return False


def append_to_sheet(data):
    """
    Append extracted resume data to Google Sheet
    
    Args:
        data: dict with extracted resume information
    """
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        
        # Prepare row data
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        skills_str = ', '.join(data.get('skills', [])) if isinstance(data.get('skills'), list) else str(data.get('skills', ''))
        
        row = [
            timestamp,
            data.get('name', 'N/A'),
            data.get('email', 'N/A'),
            data.get('phone', 'N/A'),
            data.get('linkedin', 'N/A'),
            skills_str,
            data.get('experience', 'N/A'),
            data.get('education', 'N/A'),
            data.get('summary', 'N/A'),
            data.get('whatsapp_number', 'N/A'),
            'Processed'
        ]
        
        # Append to sheet
        body = {'values': [row]}
        
        result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        
        print(f"✅ Data appended to Google Sheet: {result.get('updates').get('updatedCells')} cells updated")
        return True
        
    except Exception as e:
        print(f"❌ Error appending to sheet: {e}")
        return False


def test_connection():
    """Test Google Sheets connection"""
    try:
        service = get_sheets_service()
        sheet = service.spreadsheets()
        
        result = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
        print(f"✅ Connected to Google Sheet: {result.get('properties').get('title')}")
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False


if __name__ == "__main__":
    # Test the connection
    print("Testing Google Sheets connection...")
    
    if test_connection():
        print("\nInitializing sheet...")
        initialize_sheet()
        
        # Test data
        test_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+1-555-0123',
            'linkedin': 'linkedin.com/in/johndoe',
            'skills': ['Python', 'JavaScript', 'React'],
            'experience': '5 years',
            'education': 'B.S. Computer Science',
            'summary': 'Experienced software engineer',
            'whatsapp_number': 'whatsapp:+1234567890'
        }
        
        print("\nAppending test data...")
        append_to_sheet(test_data)
        print("\n✅ Test complete! Check your Google Sheet.")



