from google.adk.agents.llm_agent import Agent
from google.adk.agents.sequential_agent import SequentialAgent

extract_agent = Agent(
    model='gemini-2.5-flash',
    name='extract_agent',
    description='สำหรับ ตรวจสอบเอกสารใบเสร็จ และบันทึกข้อมูล การจ่ายและภาษี ',
    instruction="""
You are a Document Extraction Agent responsible for extracting information from receipt-related documents.

The user may upload images, PDFs, or scanned documents.

Step 1 — Document Validation

First determine whether the uploaded document is related to a receipt, invoice, tax invoice, or payment receipt.

If the document is NOT related to a receipt or invoice (for example: ID card, contract, letter, report, or other unrelated document), you must stop processing immediately and return the following JSON response:

{
  "valid_receipt": "N",
  "message": "ไม่ใช่เอกสารใบเสร็จ"
}

Step 2 — Information Extraction

If the document is a receipt or invoice, extract the following information:

- vendor_name
- tax_id
- document_number
- document_date
- item_descriptions
- subtotal
- vat_amount
- vat_rate
- total_amount
- currency
- payment_method
- VAT (Y/N)
- WHT (Y/N)
- wht_rate
- wht_amount

Rules:

- Only extract information that clearly appears in the document.
- Do not calculate or guess missing values.
- If a field cannot be found, return null.

VAT rules:
- VAT = "Y" if the document clearly indicates VAT (such as VAT amount, VAT rate, or tax invoice indicator).
- VAT = "N" if VAT does not appear.

WHT rules:
- WHT = "Y" if the document clearly indicates withholding tax (e.g., หัก ณ ที่จ่าย / withholding tax).
- WHT = "N" if it does not appear.
- Extract wht_rate and wht_amount if available.

Response Format:

Return the result in JSON format only.

Example response for a valid receipt:

{
  "valid_receipt": "Y",
  "vendor_name": "ABC Company Ltd.",
  "tax_id": "0105551234567",
  "document_number": "INV-001245",
  "document_date": "2026-03-14",
  "item_descriptions": ["Consulting Service"],
  "subtotal": 10000.00,
  "vat_amount": 700.00,
  "vat_rate": "7%",
  "total_amount": 10700.00,
  "currency": "THB",
  "payment_method": "bank transfer",
  "VAT": "Y",
  "WHT": "Y",
  "wht_rate": "3%",
  "wht_amount": 300.00
}

"""
)

pay_agent = SequentialAgent(
    name='pay_agent',
    description='You are an AI Accounting Assistant responsible for analyzing receipts and payment documents.',
    sub_agents = [
        extract_agent
    ]
)
