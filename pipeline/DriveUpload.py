import gspread
import csv
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
 
def upload2Drive():
	# use creds to create a client to interact with the Google Drive API
	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
	creds = ServiceAccountCredentials.from_json_keyfile_name('Synapto-3969fc4f7704.json', scope)
	client = gspread.authorize(creds)
	service = discovery.build('sheets', 'v4', credentials=creds)
	# Find a workbook by name and open the first sheet
	# Make sure you use the right name here.
	# sheet = client.open_by_key("1dVWTJy_9UpKwfmbVs6RajNohwYTuGxyZBBAVzm_VefA")
	# worksheet =sheet.get_worksheet(0)
	# print type(worksheet)
	spreadsheet_id = '1dVWTJy_9UpKwfmbVs6RajNohwYTuGxyZBBAVzm_VefA'
	# Extract and print all of the values
	#list_of_hashes = sheet.get_all_values()
	#print(list_of_hashes)
	f = open("output_pipeline.csv",'r')
	results_reader=csv.reader(f,delimiter=',')
	results_lines=list(results_reader)
	batch_update_values_request_body = {
    # How the input data should be interpreted.
    'value_input_option': 'RAW',  # TODO: Update placeholder value.

    # The new values to apply to the spreadsheet.
    'data': {
		"range": "A1:X"+str(len(results_lines)),
		"majorDimension": "ROWS",
		"values": results_lines,
		},  # TODO: Update placeholder value.

    # TODO: Add desired entries to the request body.
	}
	print len(results_lines[0])
	#k=f.read()
	#print k
	#client.import_csv("1ZRhTB_t_9cpjtdUhUpY5TkSPqHxrZ3fItpI2BIp8tvo",k)
	request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=batch_update_values_request_body)
	response = request.execute()

upload2Drive()