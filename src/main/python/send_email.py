import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_payment_reminder(api_key, to, sender_company_name, company_name, invoice_no, po_no, remaining_payment):

    message = Mail(
        from_email='sarthakjariwala1@gmail.com',
        to_emails=to,
        subject=f"Payment Reminder from {sender_company_name}",
        plain_text_content=f"""
        Dear {company_name},

        This is a payment reminder for your pending payment with {sender_company_name}.

        Invoice No :
            {invoice_no}
        P/O No :
            {po_no}
        Pending Payment :
            Rs. {remaining_payment}
        
        Your ontime payment is greatly appreciated.
        """
        
        )
    try:
        sg = SendGridAPIClient(api_key) # os.environ.get('SENDGRID_API_KEY')
        response = sg.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except Exception as e:
        print(e.body)

    return response