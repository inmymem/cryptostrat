from celery import shared_task
from .lbc import conn_call, send_message
import telegram.bot as telegram
import os

#Within limits
@shared_task
def send_within_limits_starting_message(contact_id, real_name, bank_account, reference):
    message = f"""Hi, welcome back! We hope you are doing well, it is great to see you again. 

    The payment must come from a bank account in your name ({real_name}).  Third party or in branch payments are not allowed. Payments from business accounts are also not allowed unless we have verified you as a business previously and consented to it.

    Please make the payment to the following details:

    Payee Name: {bank_account['name']}
    Sort Code: {bank_account['sort_code']}
    Account Number: {bank_account['number']}
    Reference: {reference}

    Regarding the reference, please make sure to use the correct reference provided above (composed of numbers). If you are unable to set or change your reference please go ahead but it may take longer to release your coins. 

    Please don’t forget to press ‘I have paid’ once you have paid to speed-up the process. As soon as your payment is received by us (usually takes seconds), you will instantly get your bitcoins. 
    """
    send_message(contact_id,message)
@shared_task
def send_within_limits_ending_message(contact_id):
    message = """And as usual, you have your Bitcoins now! 

    We hope it was a pleasant experience as usual and would be grateful if you could leave a trusted feedback (if you haven’t already). This will allow us both to enhance our reputation on localbitcoins and more importantly it will allow you to see our ‘trusted only’ advertisements, which only our trusted customers can see and are priced much lower than the normal advertisements. You already have access to our 24/7 automated (and cheaper) service to trade when it suits you – just look for the starred offers!
    """

    message_2 = """To access our offer more easily and directly from our profile, bookmark us: 

    https://localbitcoins.com/accounts/profile/Cryptostrat.co.uk/
    
    Feel free to drop us a message on Whatsapp or Telegram (+447751189354) especially if you have any questions or want to negotiate pricing! We do special offers, prices and discounts for our regular customers and bulk buyers/sellers.

    Thank you for the trade and we hope to see you again soon.
    """

    send_message(contact_id,message)
    send_message(contact_id,message_2)



####################### Starting at ST0 ########################################################################
#ST0 to ST1
@shared_task
def send_st0_to_st1_verification_required(contact_id, verification_url):
    message = """Hi, thank you for choosing to trade with us. We hope you are doing well. Welcome to your first trade with Cryptostrat.co.uk, we always promise to offer the best service and price.

    Due to regulation (called 5AMLD implemented on the 10/01/2020), we are going to need to perform an ID verification. The good news is that it is smooth (takes less than 2 minutes of your time) and thousands of our customers have already done it. Furthermore, once it is completed, you will never have to do it again and our future trades will happen in seconds. 

    After verification is done, we will send you our bank details for you to send us the payment. As soon as your payment is received, we will release your bitcoins. 
    """
    message_2 = f"""Please visit the link below on your smartphone or computer browser and follow the instructions provided on the screen to upload your document there (please make sure you copy the whole link):

    {verification_url}

    ----------------------------------------------------------------------

    To speed-up the verification process, please take the following into consideration:

    - Upload a good quality picture (clear picture taken in good lighting conditions). 
    - The picture of your document should show all corners.
    - Your UK proof of address needs to be less than 3 months old.
    - Your UK proof of address document can also be downloaded (not screenshot) from your online banking, utility provider’s website, etc…
    - You can use your driving licence as proof of address but you have to use another document as proof of ID (passport, national ID, residence permit, etc.).
    """
    send_message(contact_id,message)
    send_message(contact_id,message_2)

@shared_task
def send_st0_to_st1_verification_passed(contact_id, real_name, bank_account, reference):
    message = f"""Your verification was successful! We officially welcome you as a verified customer of cryptostrat.co.uk. We are proud to have you amongst our customers and hope that we will always meet all your expectations.

    Now it is time for you to send us the payment. The payment must come from a bank account in your name ({real_name}). Third party or in branch payments are not allowed and will just waste both our times as they will have to be refunded to the same account they came from. Payments from business accounts are also not allowed unless we have verified you as a business previously and consented to it. 
    """
    message_2 = f"""Please make the payment to the following details:

    Payee Name: {bank_account['name']}
    Sort Code: {bank_account['sort_code']}
    Account Number: {bank_account['number']}
    Reference: {reference}

    Regarding the reference, please make sure to use the correct reference provided above (composed of numbers). If you are unable to set or change your reference please go ahead but it may take longer to release your coins. 

    Please don’t forget to press ‘I have paid’ once you have paid to speed-up the process.
    """
    send_message(contact_id,message)
    send_message(contact_id,message_2)

@shared_task
def send_st0_to_st1_ending_message(contact_id):
    message = """And just like that you have your Bitcoins! 

    Remember, we will never ask for your ID again. Our future trades should be lightning fast! 

    We hope it was a pleasant experience and would be grateful if you could leave a trusted feedback (you can click on it on the right of the screen) and we will do the same. This will allow us both to enhance our reputation on localbitcoins and more importantly it will allow you to see our ‘trusted only’ advertisements, which only our trusted customers can see and are priced much lower than the normal advertisements. Furthermore, you now have access to our 24/7 automated (and cheaper) service to trade when it suits you – just look for the starred offers!
    """
    message_2 = """To access our offer more easily and directly from our profile, bookmark us: 

    https://localbitcoins.com/accounts/profile/Cryptostrat.co.uk/
    
    Feel free to drop us a message on Whatsapp or Telegram (+447751189354) especially if you have any questions or want to negotiate pricing! We do special offers, prices and discounts for our regular customers and bulk buyers/sellers.

    Thank you for the trade and we hope to see you again. 
    """
    send_message(contact_id,message)
    send_message(contact_id,message_2)




#ST0 over 2K transaction
@shared_task
def send_st0_to_st2_2K_transaction_verification_required(contact_id, verification_url):
    message = """Hi, thank you for choosing to trade with us. We hope you are doing well. Welcome to your first trade with Cryptostrat.co.uk, we always promise to offer the best service and price.

    Due to regulation (called 5AMLD implemented on the 10/01/2020), we are going to need to perform verification. The good news is that it is smooth (takes less than 5 minutes of your time) and thousands of our customers have already done it. Furthermore, after you complete the 2 steps of verification, you will never have to do them again with us. Which means our future trades will happen in seconds without the need for those verifications again. 

    After verification is completed, we will then send you our bank details for you to send us the payment. As soon as your payment is received, we will release your bitcoins. 

    Let’s start with the first step of verification which is the ID one.
    """
    message_2 = f"""Please visit the link below on your smartphone or computer browser and follow the instructions provided on the screen to upload your document there (please make sure you copy the whole link):

    {verification_url}

    ----------------------------------------------------------------------


    To speed-up the verification process, please take the following into consideration:

    - Upload a good quality picture (clear picture taken in good lighting conditions). 
    - The picture of your document should show all corners.
    - Your UK proof of address needs to be less than 3 months old (except for driving licence).
    - Your UK proof of address document can also be downloaded (not screenshot) from your online banking, utility provider’s website, etc…
    - You can use your driving licence as proof of address but you have to use another document as proof of ID (passport, national ID, residence permit, etc.).
    """

    send_message(contact_id,message)
    send_message(contact_id,message_2)

@shared_task
def send_st0_to_st2_2K_transaction_id_verification_passed(contact_id):
    message = """First step completed successfully! Now onto the second and last step. You can do it in 2 ways, either:

    1) A recorded video of yourself sent to our Whatsapp or Telegram or Skype (+447751189354) saying:

    ‘My name is [your full name]. I am verifying my identity to buy bitcoins for myself from M5 Fintech Limited and confirm no third parties are involved. I am not giving over control of my computer to anyone. I alone hold the password to my bank account. No account of mine is held ransom and I am not pressured into making this statement in any way. I acknowledge my legal and financial responsibility in making the purchase.’

    OR

    2) We can video call each other quickly in Skype or Zoom and that would work too. You would have to just say the same text as what is written above and we will record it for you. If you choose this second option, please just tell us what is your Skype or Zoom id/email/phone number and we will add you and take it from there.
    """
    send_message(contact_id,message)

@shared_task
def send_st0_to_st2_2K_transaction_video_verification_passed(contact_id, real_name, bank_account, reference):
    message = f"""Your video verification was also successful! We officially welcome you as a verified customer of cryptostrat.co.uk. We are proud to have you amongst our customers and hope that we will always meet all your expectations.

    Now it is time for you to send us the payment. The payment must come from a bank account in your name ({real_name}). Third party or in branch payments are not allowed and will just waste both our times as they will have to be refunded to the same account they came from. Payments from business accounts are also not allowed unless we have verified you as a business previously and consented to it.

    Regarding the reference, please make sure to use the correct reference provided (composed of numbers). If you are unable to set or change your reference please go ahead but it may take longer to release your coins. 
    """

    message_2 = f"""Please make the payment to the following details:

    Payee Name: {bank_account['name']}
    Sort Code: {bank_account['sort_code']}
    Account Number: {bank_account['number']}
    Reference: {reference}

    Please don’t forget to press ‘I have paid’ once you have paid to speed-up the process.
    """

    send_message(contact_id,message)
    send_message(contact_id,message_2)

@shared_task
def send_st0_to_st2_2K_transaction_ending_message(contact_id):
    message = """And just like that you have your Bitcoins! 

    Remember, we will never ask for these verifications again. Our future trades should be lightning fast! 

    We hope it was a pleasant experience and would be grateful if you could leave a trusted feedback (you can click on it on the right of the screen) and we will do the same. This will allow us both to enhance our reputation on localbitcoins and more importantly it will allow you to see our ‘trusted only’ advertisements, which only our trusted customers can see and are priced much lower than the normal advertisements. Furthermore, you now have access to our 24/7 automated (and cheaper) service to trade when it suits you – just look for the starred offers!
    """
    message_2 = """To access our offer more easily and directly from our profile, bookmark us: 

    https://localbitcoins.com/accounts/profile/Cryptostrat.co.uk/
    
    Feel free to drop us a message on Whatsapp or Telegram (+447751189354) especially if you have any questions or want to negotiate pricing! We do special offers, prices and discounts for our regular customers and bulk buyers/sellers.

    Thank you for the trade and we hope to see you again. Take care
    """
    send_message(contact_id,message)
    send_message(contact_id,message_2)




#ST0 to ST2
@shared_task
def send_st0_to_st2_transaction_verification_required(contact_id, verification_url):
    message = """Hi, thank you for choosing to trade with us. We hope you are doing well. Welcome to your first trade with Cryptostrat.co.uk, we always promise to offer the best service and price.

    Due to regulation (called 5AMLD implemented on the 10/01/2020), we are going to need to perform verification. The good news is that it is smooth (takes less than 5 minutes of your time) and thousands of our customers have already done it. Furthermore, after you complete the 2 steps of verification, you will never have to do them again with us. Which means our future trades will happen in seconds without the need for those verifications again. 

    After verification is completed, we will then send you our bank details for you to send us the payment. As soon as your payment is received, we will release your bitcoins. 

    Let’s start with the first step of verification which is the ID one.
    """

    message_2 = f"""Please visit the link below on your smartphone or computer browser and follow the instructions provided on the screen to upload your document there (please make sure you copy the whole link):

    {verification_url}

    ----------------------------------------------------------------------


    To speed-up the verification process, please take the following into consideration:

    - Upload a good quality picture (clear picture taken in good lighting conditions). 
    - The picture of your document should show all corners.
    - Your UK proof of address needs to be less than 3 months old (except for driving licence).
    - Your UK proof of address document can also be downloaded (not screenshot) from your online banking, utility provider’s website, etc…
    - You can use your driving licence as proof of address but you have to use another document as proof of ID (passport, national ID, residence permit, etc.).
    """

    send_message(contact_id,message)
    send_message(contact_id,message_2)

@shared_task
def send_st0_to_st2_transaction_id_verification_passed(contact_id):
    message = """First step completed successfully! Now onto the second and last step. You can do it in 2 ways, either:

    1) A recorded video of yourself sent to our Whatsapp or Telegram or Skype (+447751189354) saying:

    ‘My name is [your full name]. I am verifying my identity to buy bitcoins for myself from M5 Fintech Limited and confirm no third parties are involved. I am not giving over control of my computer to anyone. I alone hold the password to my bank account. No account of mine is held ransom and I am not pressured into making this statement in any way. I acknowledge my legal and financial responsibility in making the purchase.’

    OR

    2) We can video call each other quickly in Skype or Zoom and that would work too. You would have to just say the same text as what is written above and we will record it for you. If you choose this second option, please just tell us what is your Skype or Zoom id/email/phone number and we will add you and take it from there.
    """
    send_message(contact_id,message)

@shared_task
def send_st0_to_st2_transaction_video_verification_passed(contact_id, real_name, bank_account, reference):
    message = f"""Your video verification was also successful! We officially welcome you as a verified customer of cryptostrat.co.uk. We are proud to have you amongst our customers and hope that we will always meet all your expectations.

    Now it is time for you to send us the payment. The payment must come from a bank account in your name ({real_name}). Third party or in branch payments are not allowed and will just waste both our times as they will have to be refunded to the same account they came from. Payments from business accounts are also not allowed unless we have verified you as a business previously and consented to it.

    Regarding the reference, please make sure to use the correct reference provided (composed of numbers). If you are unable to set or change your reference please go ahead but it may take longer to release your coins. 
    """
    message_2 = f"""Please make the payment to the following details:

    Payee Name: {bank_account['name']}
    Sort Code: {bank_account['sort_code']}
    Account Number: {bank_account['number']}
    Reference: {reference}

    Please don’t forget to press ‘I have paid’ once you have paid to speed-up the process.
    """
    send_message(contact_id,message)
    send_message(contact_id,message_2)

@shared_task
def send_st0_to_st2_transaction_ending_message(contact_id):
    message = """And just like that you have your Bitcoins! 

    Remember, we will never ask for these verifications again. Our future trades should be lightning fast! 

    We hope it was a pleasant experience and would be grateful if you could leave a trusted feedback (you can click on it on the right of the screen) and we will do the same. This will allow us both to enhance our reputation on localbitcoins and more importantly it will allow you to see our ‘trusted only’ advertisements, which only our trusted customers can see and are priced much lower than the normal advertisements. Furthermore, you now have access to our 24/7 automated (and cheaper) service to trade when it suits you – just look for the starred offers!
    """

    message_2 = """To access our offer more easily and directly from our profile, bookmark us: 

    https://localbitcoins.com/accounts/profile/Cryptostrat.co.uk/
    
    Feel free to drop us a message on Whatsapp or Telegram (+447751189354) especially if you have any questions or want to negotiate pricing! We do special offers, prices and discounts for our regular customers and bulk buyers/sellers.

    Thank you for the trade and we hope to see you again. Take care
    """
    send_message(contact_id,message)
    send_message(contact_id,message_2)




#ST0 to ST3
@shared_task
def send_st0_to_st3_transaction_verification_required(contact_id, verification_url):
    message = """Hi, thank you for choosing to trade with us. We hope you are doing well. Welcome to your first trade with Cryptostrat.co.uk, we always promise to offer the best service and price.

    Due to regulation (called 5AMLD implemented on the 10/01/2020), we are going to need to perform verification. The good news is that it is smooth (takes less than 10 minutes of your time) and thousands of our customers have already done it. Furthermore, after you complete the 3 steps of verification, you will never have to do them again with us. Which means our future trades will happen in seconds without the need for verifications again. 

    After verification is completed, we will then send you our bank details for you to send us the payment. As soon as your payment is received, we will release your bitcoins. 

    Let’s start with the first step of verification which is the ID one.
    """
    message_2 = f"""Please visit the link below on your smartphone or computer browser and follow the instructions provided on the screen to upload your document there (please make sure you copy the whole link):

    {verification_url}

    ----------------------------------------------------------------------


    To speed-up the verification process, please take the following into consideration:

    - Upload a good quality picture (clear picture taken in good lighting conditions). 
    - The picture of your document should show all corners.
    - Your UK proof of address needs to be less than 3 months old (except for driving licence).
    - Your UK proof of address document can also be downloaded (not screenshot) from your online banking, utility provider’s website, etc…
    - You can use your driving licence as proof of address but you have to use another document as proof of ID (passport, national ID, residence permit, etc.).
    """
    send_message(contact_id,message)
    send_message(contact_id,message_2)

@shared_task
def send_st0_to_st3_transaction_id_verification_passed(contact_id):
    message = f"""First step completed successfully! Now onto the second step. You can do it in 2 ways, either:

    1) A recorded video of yourself sent to our Whatsapp or Telegram or Skype (+447751189354) saying:

    ‘My name is [your full name]. I am verifying my identity to buy bitcoins for myself from M5 Fintech Limited and confirm no third parties are involved. I am not giving over control of my computer to anyone. I alone hold the password to my bank account. None of my accounts are held ransom and I am not pressured into making this statement in any way. I acknowledge my legal and financial responsibility in making the purchase.’

    OR

    2) We can video call each other quickly in Skype or Zoom and that would work too. You would have to just say the same text as what is written above and we will record it for you. If you choose this second option, please just tell us what is your Skype or Zoom id/email/phone number and we will add you and take it from there.
    """
    send_message(contact_id,message)

@shared_task
def send_st0_to_st3_transaction_video_verification_passed(contact_id):
    message = """Your video verification was also successful! Now onto the third and last step that is the proof of funds verification. Please send your proof(s) of funds to our email ‘ contact@cryptostrat.co.uk ’ or by Whatsapp (+447751189354). Examples of Proof of funds can be or show: 

    - Bank statement(s) 
    - Dividends 
    - Employment(s) income 
    - Pay slips 
    - Crypto currency mining income
    - Trading income
    - Inheritance
    - Investment profits
    - Savings
    - Letter from bank
    - Sale of property
    - Loan/Credit
    - Donations
    - Grants
    - Crowdfunding
    - Subsidies

    Or any other official document or information that proves the source of your funds. The government wants us to make sure that we check for every single customer (who has bought 10,000£ or more in one go or accumulated) that their funds have not come from proceeds of crime. All we need is a proof of funds and we are good to go.
    """
    send_message(contact_id,message)
@shared_task
def send_st0_to_st3_transaction_proof_of_funds_verification_passed(contact_id, real_name, bank_account, reference):
    message = f"""We officially welcome you as a fully verified customer of cryptostrat.co.uk. We are proud to have you amongst our customers and hope that we will always meet all your expectations.

    Now it is time for you to send us the payment. The payment must come from a bank account in your name ({real_name}). Third party or in branch payments are not allowed and will just waste both our times as they will have to be refunded to the same account they came from. Payments from business accounts are also not allowed unless we have verified you as a business previously and consented to it.

    Regarding the reference, please make sure to use the correct reference provided (composed of numbers). If you are unable to set or change your reference please go ahead but it may take longer to release your coins. 
    """
    message_2 = f"""Please make the payment to the following details:

    Payee Name: {bank_account['name']}
    Sort Code: {bank_account['sort_code']}
    Account Number: {bank_account['number']}
    Reference: {reference}

    Please don’t forget to press ‘I have paid’ once you have paid to speed-up the process.
    """

    send_message(contact_id,message)
    send_message(contact_id,message_2)
@shared_task
def send_st0_to_st3_transaction_ending_message(contact_id):
    message = """And just like that you have your Bitcoins! 

    Remember, we will never ask for these verifications again. Our future trades should be lightning fast! 

    We hope it was a pleasant experience and would be grateful if you could leave a trusted feedback (you can click on it on the right of the screen) and we will do the same. This will allow us both to enhance our reputation on localbitcoins and more importantly it will allow you to see our ‘trusted only’ advertisements, which only our trusted customers can see and are priced much lower than the normal advertisements. Furthermore, you now have access to our 24/7 automated (and cheaper) service to trade when it suits you – just look for the starred offers!
    """
    message_2 = """To access our offers more easily and directly from our profile, bookmark us: 

    https://localbitcoins.com/accounts/profile/Cryptostrat.co.uk/
    
    Feel free to drop us a message on Whatsapp or Telegram (+447751189354) especially if you have any questions or want to negotiate pricing! We do special offers, prices and discounts for our regular customers and bulk buyers/sellers.

    Thank you for the trade and we hope to see you again. Take care
    """
    send_message(contact_id,message)
    send_message(contact_id,message_2)
###############################################################################################################################

####################### Starting at ST1 ########################################################################

#ST1 to ST2 over 2K transaction
@shared_task
def send_st1_to_st2_2K_transaction_verification_required(contact_id):
    message = """Hi, welcome back. We hope you are doing well and it is great to see you again. 

    We can see that you have already provided ID verification with us but that you are attempting to buy over 2,000£ in one go now, and for that we are required by regulation and law to perform a quick video verification. The good news is that it is simple and should take less than 5 minutes of your time. Furthermore, after we receive the video recording this time, you will never have to do it again with us. Which means our future trades will happen in seconds as they always did before.

    We would have liked it to be otherwise and not ask for more verification (only more cost and time spent on our side and a hassle for our customers). Unfortunately due to law, we are going to need one of the two video verifications to proceed:
    """

    message_2 = """1) A recorded video of yourself sent to our Whatsapp or Telegram or Skype (+447751189354) saying:

    ‘My name is [your full name]. I am verifying my identity to buy bitcoins for myself from M5 Fintech Limited and confirm no third parties are involved. I am not giving over control of my computer to anyone. I alone hold the password to my bank account. No account of mine is held ransom and I am not pressured into making this statement in any way. I acknowledge my legal and financial responsibility in making the purchase.’

    OR

    2) We can video call each other quickly in Skype or Zoom and that would work too. You would have to just say the same text as what is written above and we will record it for you. If you choose this second option, please just tell us what is your Skype or Zoom id/email/phone number and we will add you and take it from there.

    Once we finish one of the two steps above we will send you our bank details and proceed as usual. Thank you
    """
    send_message(contact_id,message)
    send_message(contact_id,message_2)

@shared_task
def send_st1_to_st2_2K_transaction_verification_passed(contact_id, real_name, bank_account, reference):
    message = f"""Thank you for your cooperation and sorry for the hassle. The video was well received! We can now proceed to the payment.

    The payment must come from a bank account in your name ({real_name}) and no third party or in branch payments are allowed. Payments from business accounts are also not allowed unless we have verified you as a business previously and consented to it.

    Please make the payment to the following details:

    Payee Name: {bank_account['name']}
    Sort Code: {bank_account['sort_code']}
    Account Number: {bank_account['number']}
    Reference: {reference}

    Regarding the reference, please make sure to use the correct reference provided above (composed of numbers). If you are unable to set or change your reference please go ahead but it may take longer to release your coins. 

    Please don’t forget to press ‘I have paid’ once you have paid to speed-up the process. As soon as your payment is received (usually takes seconds), you will instantly get your bitcoins.
    """
    send_message(contact_id,message)

@shared_task
def send_st1_to_st2_2K_transaction_ending_message(contact_id):
    message = """And as usual, you have your Bitcoins now! We know these verifications are a hassle, but the good news is now you will never have to do them again and our trades will happen in seconds. Our future trades should be lightning fast!

    To access our offers more easily and directly from our profile, bookmark us: 

    https://localbitcoins.com/accounts/profile/Cryptostrat.co.uk/
    
    Feel free to drop us a message on Whatsapp or Telegram (+447751189354) especially if you have any questions or want to negotiate pricing! We do special offers, prices and discounts for our regular customers and bulk buyers/sellers. 

    Thank you for the trade, it is always a pleasure trading with you. We hope to see you again soon for a fast trade. Take care
    """
    send_message(contact_id,message)

#ST1 to ST2
@shared_task
def send_st1_to_st2_verification_required(contact_id):
    message = """Hi, welcome back. We hope you are doing well and it is great to see you again. 

    We can see that you have already provided ID verification with us but that your accumulated volume with us has gone past 5,000£, and for that we are required by regulation and law to perform further verification. The good news is that it is simple and should take less than 3 minutes of your time. Furthermore, after we receive the video recording this time, you will never have to do it again with us. Which means our future trades will happen in seconds as they always did before.

    We would have liked it to be otherwise and not ask for more verification (only more cost and time spent on our side and a hassle for our customers). Unfortunately due to law, we are going to need one of the two video verifications to proceed:
    """
    message_2 = """A recorded video of yourself sent to our Whatsapp or Telegram or Skype (+447751189354) saying:

    ‘My name is [your full name]. I am verifying my identity to buy bitcoins for myself from M5 Fintech Limited and confirm no third parties are involved. I am not giving over control of my computer to anyone. I alone hold the password to my bank account. None of my accounts are held in ransom and I am not pressured into making this statement in any way. I acknowledge my legal and financial responsibility in making the purchase.’

    OR

    2) We can video call each other quickly in Skype or Zoom and that would work too. You would have to just say the same text as what is written above and we will record it for you. If you choose this second option, please just tell us what is your Skype or Zoom id/email/phone number and we will add you and take it from there.

    Once we finish one of the two steps above we will send you our bank details and proceed as usual. Thank you
        """
    send_message(contact_id,message)
    send_message(contact_id,message_2)

@shared_task
def send_st1_to_st2_verification_passed(contact_id, real_name, bank_account, reference):
    message = f"""Thank you for your cooperation and sorry for the hassle. The video was well received! We can now proceed to the payment.

    The payment must come from a bank account in your name [your full name] and no third party or in branch payments are allowed. Payments from business accounts are also not allowed unless we have verified you as a business previously and consented to it.

    Please make the payment to the following details:

    Payee Name: {bank_account['name']}
    Sort Code: {bank_account['sort_code']}
    Account Number: {bank_account['number']}
    Reference: {reference}

    Regarding the reference, please make sure to use the correct reference provided above (composed of numbers). If you are unable to set or change your reference please go ahead but it may take longer to release your coins. 

    Please don’t forget to press ‘I have paid’ once you have paid to speed-up the process. As soon as your payment is received (usually takes seconds), you will instantly get your bitcoins.
    """
    send_message(contact_id,message)

@shared_task
def send_st1_to_st2_ending_message(contact_id):
    message = """And as usual, you have your Bitcoins now! We know these verifications are a hassle, but the good news is now you will never have to do them again and our trades will happen in seconds. Our future trades should be lightning fast!

    To access our offers more easily and directly from our profile, bookmark us: 

    https://localbitcoins.com/accounts/profile/Cryptostrat.co.uk/
    
    Feel free to drop us a message on Whatsapp or Telegram (+447751189354) especially if you have any questions or want to negotiate pricing! We do special offers, prices and discounts for our regular customers and bulk buyers/sellers. You are officially one of them now with more than 5,000£ bought.

    Thank you for the trade, it is always a pleasure trading with you. We hope to see you again soon for a fast trade. Take care
    """
    send_message(contact_id,message)




#ST1 to ST3
@shared_task
def send_st1_to_st3_verification_required(contact_id):
    message = """Hi, welcome back. We hope you are doing well and it is great to see you again. 

    We can see that you already provided ID verification but that your accumulated volume with us is 10,000£ or more and for that we are required by regulation and law to perform further verification. The good news is that it is simple and should take less than 7 minutes of your time. Furthermore, after we receive these 2 verifications, you will never have to do another verification with us. Which means our future trades will happen in seconds as they always did before.

    We would have liked it to be otherwise and not ask for more verifications (only more cost and time spent on our side and a hassle for our customers). Unfortunately due to law, we are going to need to perform them in two steps. Let’s start with the first step.
    """
    message_2 = """You can do the first step in 2 ways, either:

    1) A recorded video of yourself sent to our Whatsapp or Telegram or Skype (+447751189354) saying:

    ‘My name is [your full name]. I am verifying my identity to buy bitcoins for myself from M5 Fintech Limited and confirm no third parties are involved. I am not giving over control of my computer to anyone. I alone hold the password to my bank account. None of my accounts are held ransom and I am not pressured into making this statement in any way. I acknowledge my legal and financial responsibility in making the purchase.’

    OR

    2) We can video call each other quickly in Skype or Zoom and that would work too. You would have to just say the same text as what is written above and we will record it for you. If you choose this second option, please just tell us what is your Skype or Zoom id/email/phone number and we will add you and take it from there.
    """
    send_message(contact_id,message)
    send_message(contact_id,message_2)

@shared_task
def send_st1_to_st3_st3_verification_required(contact_id):
    message = """Your video verification was successful! Now onto the second and last step which is the proof of funds verification. Please send your proof(s) of funds to our email ‘ contact@cryptostrat.co.uk ’ or by Whatsapp (+447751189354). Examples of Proof of funds can be or show: 

    - Bank statement(s) 
    - Dividends 
    - Employment(s) income 
    - Pay slips 
    - Crypto currency mining income
    - Trading income
    - Inheritance
    - Investment profits
    - Savings
    - Letter from bank
    - Sale of property
    - Loan/Credit
    - Donations
    - Grants
    - Crowdfunding
    - Subsidies

    Or any other official document or information that proves the source of your funds. The government wants us to make sure that we check for every single customer (who has bought 10,000£ or more in one go or accumulated) that their funds have not come from proceeds of crime. All we need is a proof of funds and we are good to go.
    """
    send_message(contact_id,message)
@shared_task
def send_st1_to_st3_verification_passed(contact_id, real_name, bank_account, reference):
    message = f"""We officially welcome you as a fully verified customer of cryptostrat.co.uk. We are proud to have you amongst our customers and hope that we will always meet all your expectations.

    Now it is time for you to send us the payment. The payment must come from a bank account in your name ({real_name}). Third party or in branch payments are not allowed. Payments from business accounts are also not allowed unless we have verified you as a business previously and consented to it.

    Regarding the reference, please make sure to use the correct reference provided (composed of numbers). If you are unable to set or change your reference please go ahead but it may take longer to release your coins. 
    """

    message_2 = f"""Please make the payment to the following details:

    Payee Name: {bank_account['name']}
    Sort Code: {bank_account['sort_code']}
    Account Number: {bank_account['number']}
    Reference: {reference}


    Please don’t forget to press ‘I have paid’ once you have paid to speed-up the process.
    """
    send_message(contact_id,message)
    send_message(contact_id,message_2)
@shared_task
def send_st1_to_st3_ending_message(contact_id):
    message = """And as usual, you have your Bitcoins now! We know these verifications are a hassle, but the good news is now you will never have to do them again and our trades will happen in seconds. Our future trades should be lightning fast!

    To access our offers more easily and directly from our profile, bookmark us: 

    https://localbitcoins.com/accounts/profile/Cryptostrat.co.uk/
    
    Feel free to drop us a message on Whatsapp or Telegram (+447751189354) especially if you have any questions or want to negotiate pricing! We do special offers, prices and discounts for our regular customers and bulk buyers/sellers. You are officially one of them now with more than 10,000£ bought.

    Thank you for the trade, it is always a pleasure trading with you. We hope to see you again soon for a fast trade. Take care
    """
    send_message(contact_id,message)
###############################################################################################################################

####################### Starting at ST2 ########################################################################

#ST2 to ST3
@shared_task
def send_st2_to_st3_verification_required(contact_id):
    message = """Hi, welcome back. We hope you are doing well and it is great to see you again as usual. 

    We can see that you have already provided us with ID and video verification but that your accumulated volume with us is 10,000£ or more, and for that we are required by the UK AML (Anti Money Laundering) regulation to ask you for proof of funds. The good news is that it can be simple and fast. Furthermore, and even better news is that after we receive document(s) from you for proof of funds, you will be good to go as usual. Which means our future trades will happen in seconds as they did before without further requirements.

    We would have liked it to be otherwise and not ask for proof of funds (only more cost and time spent on our side and a pain for our customers). Unfortunately due to law, we are going to need any type of official document(s) to prove your source of funds. 
    """

    message_2 = """Please send your proof(s) of funds to our email ‘ contact@cryptostrat.co.uk ’ or by Whatsapp (+447751189354). Examples of Proof of funds can be or show: 

    - Bank statement(s) 
    - Dividends 
    - Employment(s) income 
    - Pay slips 
    - Crypto currency mining income
    - Trading income
    - Inheritance
    - Investment profits
    - Savings
    - Letter from bank
    - Sale of property
    - Loan/Credit
    - Donations
    - Grants
    - Crowdfunding
    - Subsidies

    Or any other official document or information that proves the source of your funds. The government wants us to make sure that we check for every single customer (who has bought 10,000£ accumulated or more) that their funds have not come from proceeds of crime. Not that we believe that that is the case for you, quite the opposite. We have gotten used to trading with you, appreciate you as our customer and want to continue trading with you. All we need is a proof of funds and we are good to go as usual.
    """
    send_message(contact_id,message)
    send_message(contact_id,message_2)
@shared_task
def send_st2_to_st3_verification_passed(contact_id, real_name, bank_account, reference):
    message = f"""Thank you for your cooperation and sorry for the hassle. The source of funds was received and accepted. We can now proceed to the payment.

    The payment must come from a bank account in your name ({real_name}) and no third party or in branch payments are allowed. Payments from business accounts are also not allowed unless we have verified you as a business previously and consented to it.

    Please make the payment to the following details:

    Payee Name: {bank_account['name']}
    Sort Code: {bank_account['sort_code']}
    Account Number: {bank_account['number']}
    Reference: {reference}

    Regarding the reference, please make sure to use the correct reference provided above (composed of numbers). If you are unable to set or change your reference please go ahead but it may take longer to release your coins. 

    Please don’t forget to press ‘I have paid’ once you have paid to speed-up the process. As soon as your payment is received (usually takes seconds), you will instantly get your bitcoins. 
    """
    send_message(contact_id,message)
@shared_task
def send_st2_to_st3_ending_message(contact_id):
    message = """And as usual, you have your Bitcoins now! We know these verifications are a hassle, but the good news is now you will never have to do them again and our trades will happen in seconds. Our future trades should be lightning fast!

    To access our offers more easily and directly from our profile, bookmark us: 

    https://localbitcoins.com/accounts/profile/Cryptostrat.co.uk/
    
    Feel free to drop us a message on Whatsapp or Telegram (+447751189354) especially if you have any questions or want to negotiate pricing! We do special  offers, prices and discounts for our regular customers and bulk buyers/sellers. You are officially one of them now with more than 10,000£ bought.

    Thank you for the trade, it is always a pleasure trading with you. We hope to see you again soon for a fast trade. Take care
    """
    send_message(contact_id,message)

####################### Starting at ST3 ########################################################################
#need to add message for when above source of funds
##########--------------------------------------------------------------------------------------------
#------------------------------Buying -----------------------------------------------------------------------------------
####################### Buying T0 ########################################################################
@shared_task
def send_bt0_to_bt1_verification_required(contact_id, verification_url):
    message = """Hi, thank you for choosing to trade with us. We hope you are doing well. Welcome to your first trade with Cryptostrat.co.uk, we always promise to offer the best service and price.

    Due to regulation (called 5AMLD implemented on the 10/01/2020), we are going to need to perform an ID verification. The good news is that it is smooth (takes less than 2 minutes of your time) and thousands of our customers have already done it. Furthermore, once it is completed, you will never have to do it again and our future trades will happen in seconds. 

    After the verification is completed, we will initiate the payment to your bank account and it should be with you a few moments later (usually within seconds). 
    """
    message_2 = f"""Please visit the link below on your smartphone or computer browser and follow the instructions provided on the screen to upload your document there (please make sure you copy the whole link):

    {verification_url}

    ----------------------------------------------------------------------


    To speed-up the verification process, please take the following into consideration:

    - Upload a good quality picture (clear picture taken in good lighting conditions). 
    - The picture of your document should show all corners.
    - Your UK proof of address needs to be less than 3 months old (except for driving licence).
    - Your UK proof of address document can also be downloaded (not screenshot) from your online banking, utility provider’s website, etc…
    - You can use your driving licence as proof of address  but you have to use another document as proof of ID (passport, national ID, residence permit, etc.).
    """

    message_3 = """At the end of verification, please refresh the page as sometimes it does not automatically do that. It will then display any feedback if you need to amend something. 

    As per our trade terms, the trade number (composed of random numbers) will be written in the payment reference unless you ask us here to write another reference that is not misleading before you finish verification.
    """
    send_message(contact_id,message)
    send_message(contact_id,message_2)
    send_message.apply_async((contact_id,message_3), countdown = 60)

@shared_task
def send_bt0_to_bt1_verification_passed(contact_id):
    message = """Your verification was successful! We officially welcome you as a verified customer of cryptostrat.co.uk. We are proud to have you amongst our customers and hope that we will always meet all your expectations. Bare with us please whilst we make the payment to your account."""
    send_message(contact_id,message)

@shared_task
def send_bt0_to_bt1_payment_sent(contact_id):
    message = """The payment has been initiated and should be with you any moment now. Please don’t forget to release the bitcoins when you receive the payment."""
    send_message(contact_id,message)
    

@shared_task
def send_bt0_to_bt1_ending_message(contact_id):
    message = """And just like that our trade has ended successfully! 

    Remember, we will never again ask for your ID next time you sell to us (or even if you want to buy from us). Our future trades should be lightning fast! 

    We hope it was a pleasant experience and would be grateful if you could leave a trusted feedback (you can click on it on the right of the screen) and we will do the same. This will allow us both to enhance our reputation on localbitcoins and more importantly it will allow you to see our ‘trusted only’ buying advertisements, which only our trusted customers can see and are priced higher than the normal advertisements (just look for the starred offers)!
    """
    message_2 = """To access our offers more easily and directly from our profile, bookmark us: 

    https://localbitcoins.com/accounts/profile/Cryptostrat.co.uk/
    
    Feel free to drop us a message on Whatsapp or Telegram (+447751189354) especially if you have any questions or want to negotiate pricing! We do special offers, prices and discounts for our regular customers and bulk buyers/sellers.

    Thank you for the trade and we hope to see you again. Take care
    """

    send_message(contact_id,message)
    send_message(contact_id,message_2)
####################### Buying T1 ########################################################################
@shared_task
def send_bt1_initial_message(contact_id):
    message = """Hi, welcome back. We hope you are doing well and it is great to see you again. We are initiating the payment to your account as we speak!"""
    send_message(contact_id,message)


@shared_task
def send_bt1_payment_sent_message(contact_id):
    message = """The payment has been initiated and should be with you any moment now. Please don’t forget to release the bitcoins when you receive the payment."""
    send_message(contact_id,message)


@shared_task
def send_bt1_ending_message(contact_id):
    message = """And as usual, our trade has ended successfully! 

    We hope it was a pleasant experience and (if you haven’t already) would be grateful if you could leave a trusted feedback (you can click on it on the right of the screen) and we will do the same. This will allow us both to enhance our reputation on localbitcoins and more importantly it will allow you to see our ‘trusted only’ buying advertisements, which only our trusted customers can see and are priced higher than the normal advertisements (just look for the starred offers)!
    """
    message_2 = """To access our offers more easily and directly from our profile, bookmark us: 

    https://localbitcoins.com/accounts/profile/Cryptostrat.co.uk/
    
    Feel free to drop us a message on Whatsapp or Telegram (+447751189354) especially if you have any questions or want to negotiate pricing! We do special offers, prices and discounts for our regular customers and bulk buyers/sellers.

    Thank you for the trade and we hope to see you again. Take care
    """

    send_message(contact_id,message)
    send_message(contact_id,message_2)
