import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime


def add_weight(weight):
	scope = ['https://spreadsheets.google.com/feeds',
	         'https://www.googleapis.com/auth/drive']

	credentials = ServiceAccountCredentials.from_json_keyfile_name("CalorieCounter-ab0b4cb3bd01.json", scope)
	gc = gspread.authorize(credentials)
	ss = gc.open("Calories (Responses)")
	wks = ss.get_worksheet(3)
	now = datetime.datetime.now()
	ts = now.strftime("%d/%m/%Y %H:%M:%S")
	wks.append_row([ts, weight], value_input_option="USER_ENTERED")
