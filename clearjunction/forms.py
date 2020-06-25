from django import forms
from django.core.exceptions import ValidationError

def validate_numeric(text_number):
    try:
        text_number = int(text_number)
    except:
        raise ValidationError(f'{text_number} is not a valid numerical string')


class SendFPS(forms.Form):
    document_choices = (
        (None, ''), 
        ('passport', 'Passport'), 
        ('nationalID','National ID'),
        ('drivinglicence','Driving Licence'),

        )
    date_format = '%Y-%m-%d'
    currency = forms.ChoiceField(label= 'Currency*',choices=(('GBP', 'GBP'), ('EUR','EUR')))  #(Value, Label)
    amount = forms.IntegerField(label= 'Amount*')
    description = forms.CharField(label='Reference?*', max_length=18)
    sortCode = forms.CharField(label = 'Sort Code*', max_length=6, min_length=6, help_text='6 digit number', validators=[validate_numeric])
    accountNumber = forms.CharField(label = 'Account Number*', max_length=8, min_length=8, validators=[validate_numeric])
    firstName = forms.CharField(label= 'First Name*', max_length=30)
    lastName = forms.CharField(label= 'Last Name*', max_length=30)
    middleName = forms.CharField(label= 'Middle Name', max_length=30, initial= None, required=False)
    phone = forms.CharField(label= 'Phone Number', max_length=20, initial= None, required=False)
    birthDate = forms.DateField(label= 'Birth Date', input_formats=[date_format], initial= None, required=False)
    birthPlace = forms.CharField(label= 'Birth Place', max_length=30, initial= None, required=False, help_text='City, Country')
    
    documentType = forms.ChoiceField(label= 'Document Type', required=False, choices= document_choices, initial= None,)
    documentNumber = forms.CharField(label= 'Document Number', max_length=30, initial= None, required=False)
    documentIssuedBy = forms.CharField(label= 'Document Issued By', max_length=60, initial= None, required=False, help_text='E.G. Ministry of Interior')
    documentIssuedCountryCode = forms.CharField(label= 'Document Country Code', max_length=10, initial= None, required=False)
    documentIssueDate = forms.DateField(label= 'Document Issue Date', input_formats=[date_format], initial= None, required=False)
    documentExpiryDate = forms.DateField(label= 'Document Expiry Date', input_formats=[date_format], initial= None, required=False)

    addressCountry = forms.CharField(label= 'Address Country', max_length=30, initial= None, required=False, help_text='Code E.G. IT or UK')
    addressState = forms.CharField(label= 'Address State', max_length=30, initial= None, required=False)
    addressCity = forms.CharField(label= 'Address City', max_length=30, initial= None, required=False)
    addressZip = forms.CharField(label= 'Address Zip Code', max_length=30, initial= None, required=False)
    addressStreet = forms.CharField(label= 'Address Street', max_length=30, initial= None, required=False)







    # {"clientOrder": "1",
    #         "currency": "GBP",
    #         "amount": 210.55,
    #         "description": "reference",
    #         "payer": {"walletUuid": wallet_UUID,
    #                  },
    #         "payee": {"individual": {"phone": "34712345678",
    #                                  #"email": "peterson.julie@example.com",
    #                                  "birthDate": "1999-09-29",
    #                                  "birthPlace": "'Madrid, Spain'",
    #                                  "address": {"country": "IT",
    #                                              "zip": "123455",
    #                                              "city": "Rome",
    #                                              "street": "12 Tourin"
    #                                             },
    #                                  "document": {"type": "passport",
    #                                               "number": "AB1000222",
    #                                               "issuedCountryCode": "IT",
    #                                               "issuedBy": "Ministry of Interior",
    #                                               "issuedDate": "2016-12-21",
    #                                               "expirationDate": "2026-12-20"
    #                                              },
    #                                  "lastName": "Peterson",
    #                                  "firstName": "Julie",
    #                                  "middleName": "Maria"
    #                                 }
    #                  },
    #         "payeeRequisite": {"sortCode": "404784",
    #                            "accountNumber": "70872490"
    #                           },
    #         "payerRequisite": {#"sortCode": '',
    #                            #"accountNumber": '',
    #                            #"iban": '',
    #                            #"bankSwiftCode": ''
    #                           }
    #        }