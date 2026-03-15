import gspread
from google.oauth2.service_account import Credentials

def append_expense_row(expense_data: dict):
    """
    Append expense data to Google Sheets
    """

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
        "credentials/service_account.json",
        scopes=SCOPES
    )


    client = gspread.authorize(creds)
    sheet = client.open_by_key("1C7DohR-yZI4S1h1rzdHeag2e7ebAjG_mz1KVy_z7TjE").worksheet("PayReport")

    row = [
        expense_data.get("document_date"),
        expense_data.get("total_amount"),
        expense_data.get("vendor_name"),
        expense_data.get("document_number"),
        expense_data.get(""),
        expense_data.get("VAT"),
        expense_data.get("WHT"),
        expense_data.get("vat_amount"),
        expense_data.get("wht_amount"),
        expense_data.get("payment_method"),
        
    ]
    sheet.append_row(row)

    if expense_data.get("VAT") == "Y":
        client = gspread.authorize(creds)
        sheetVAT = client.open_by_key("1C7DohR-yZI4S1h1rzdHeag2e7ebAjG_mz1KVy_z7TjE").worksheet("VAT")

        row = [
            expense_data.get("document_number"),
            expense_data.get("document_date"),
            expense_data.get("vendor_name"),
            expense_data.get("tax_id"),
            expense_data.get(""),
            expense_data.get("subtotal"),
            expense_data.get("vat_amount"),
            expense_data.get("total_amount"),
        ]

        sheetVAT.append_row(row)

    if expense_data.get("WHT") == "Y":
        client = gspread.authorize(creds)
        sheetWHT = client.open_by_key("1C7DohR-yZI4S1h1rzdHeag2e7ebAjG_mz1KVy_z7TjE").worksheet("WHT")

        subtotal = expense_data.get("subtotal")
        total = expense_data.get("total_amount")
        wht_rate = 0
        if subtotal:
            wht_rate = int(total / subtotal)
        else:
            wht_rate = 0
        row = [
            expense_data.get("document_number"),
            expense_data.get("document_date"),
            expense_data.get("vendor_name"),
            expense_data.get(""),
            expense_data.get("tax_id"),
            expense_data.get("subtotal"),
            expense_data.get("wht_amount"),
            expense_data.get(wht_rate),
            expense_data.get("total_amount"),
            
        ]

        sheetWHT.append_row(row)

    return {"status": "success"}
