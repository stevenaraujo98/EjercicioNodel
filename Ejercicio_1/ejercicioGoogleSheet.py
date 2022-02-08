from googleapiclient.discovery import build
from google.oauth2 import service_account
import numpy as np
import pandas as pd

# Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

## The ID spreadsheet.
SPREADSHEET_ID = ''

service = build('sheets', 'v4', credentials=creds)

## Call the Sheets API
sheet = service.spreadsheets()
sheet_metadata = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
sheets = sheet_metadata.get('sheets', '')

## ID sheet and name of sheet.
# NAME_SHEET = 'resultado'
# SHEET_ID = 601367873
SHEET_ID = sheets[1].get("properties", {}).get("sheetId", 0)
NAME_SHEET = sheets[1].get("properties", {}).get("title", 0)

# Read Sheet Reto1
print('Sheet reading...')
request = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                            range="Reto1!A1:D16")
result = request.execute()

# Process
print('Processing started...')
matriz_np = np.array(result.get('values', []))
dic_values = ({matriz_np[0,0]: matriz_np[1:,0], 
               matriz_np[0,1]: matriz_np[1:,1], 
               matriz_np[0,2]: matriz_np[1:,2], 
               matriz_np[0,3]: matriz_np[1:,3]})
df = pd.DataFrame(dic_values)
df2 = df.groupby('Author')[['Country', 'Theme']].apply(lambda g: g.values.tolist()).to_dict()

countries = list(set(matriz_np[1:, 2]))
themes = list(set(matriz_np[1:, 3]))
count_country = len(countries)
count_theme = len(themes)

write_titles = [[matriz_np[0][0], matriz_np[0][1]]]
write_titles[0].extend(countries)
write_titles[0].extend(themes)

### data structure
datas = np.full((len(df2), len(countries) + len(themes)), 'FALSO', dtype=(np.unicode_, 9))

counter = 0
for i in df2.items():
    for j in i[1]:
        datas[counter, countries.index(j[0])] = 'VERDADERO'
        datas[counter, count_country + themes.index(j[1])] = 'VERDADERO'
    counter+=1

### unique authors list
authors_np = np.array(list(df2.keys())).reshape((len(list(df2.keys())), 1))
### unique feelings list
sentiment_author = np.array(df.groupby('Author')['Sentiment'].unique().to_list())
### complete writing data
datas = np.hstack([authors_np, sentiment_author, datas])

# Write Sheet Resutado
print('Document writing...')
request_body = {
    'requests': [
      # Crear la hoja
      # {
      #     'addSheet': {
      #         'properties': {
      #             'title': NAME_SHEET,
      #         }
      #     }
      # },
      {
        "unmergeCells": {
          "range": {
            "sheetId": SHEET_ID,
            "startRowIndex": 0,
            "endRowIndex": 1,
            "startColumnIndex": 2,
            "endColumnIndex": (2+count_country)+count_theme
          }
        }
      },
      {
        "mergeCells": {
            "mergeType": "MERGE_ROWS",
            "range": {
                "sheetId": SHEET_ID,
                "startRowIndex": 0,
                "endRowIndex": 1,
                "startColumnIndex": 2,
                "endColumnIndex": 2+count_country
            }
        }
      },
      {
        "mergeCells": {
            "mergeType": "MERGE_ROWS",
            "range": {
                "sheetId": SHEET_ID,
                "startRowIndex": 0,
                "endRowIndex": 1,
                "startColumnIndex": 2+count_country,
                "endColumnIndex": (2+count_country)+count_theme
            }
        }
      },
      {
        "repeatCell": {
            "cell": {
              "userEnteredValue": {
                "stringValue": matriz_np[0][2]
              },
              "userEnteredFormat": {
                "horizontalAlignment": "CENTER",
                "verticalAlignment": "MIDDLE",
              }
            },
            "range": {
              "sheetId": SHEET_ID,
              "startRowIndex": 0,
              "endRowIndex": 1,
              "startColumnIndex": 2,
              "endColumnIndex": 2+count_country
            },
            "fields": "userEnteredValue, userEnteredFormat"
        }
      },
      {
        "repeatCell": {
            "cell": {
              "userEnteredValue": {
                "stringValue": matriz_np[0][3]
              },
              "userEnteredFormat": {
                "horizontalAlignment": "CENTER",
                "verticalAlignment": "MIDDLE",
              }
            },
            "range": {
              "sheetId": SHEET_ID,
              "startRowIndex": 0,
              "endRowIndex": 1,
              "startColumnIndex": 2+count_country ,
              "endColumnIndex": (2+count_country)+count_theme
            },
            "fields": "userEnteredValue, userEnteredFormat"
        }
      }
    ]
}
request = sheet.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=request_body)
response = request.execute()

response = sheet.values().update(spreadsheetId=SPREADSHEET_ID, 
                                range="resultado!A2",
                                valueInputOption="USER_ENTERED",
                                body={"values": write_titles}).execute()

response = sheet.values().update(spreadsheetId=SPREADSHEET_ID, 
                                range="resultado!A3",
                                valueInputOption="USER_ENTERED",
                                body={"values": datas.tolist()}).execute()

print('Finish.')
