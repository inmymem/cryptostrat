from clients.models import Client, Transaction
from .models import User
from .models import Transaction as Transaction_old
from verifications.models import Application, IdDoc, AddressDoc, Person

users = User.objects.all()
for user in users:
    print(user.username)
    real_name = None
    try:
        person = Person.objects.get(user = user)
        real_name = person.get_real_name()
        print(real_name)
    except Person.DoesNotExist:
        print('no person')
    Client.objects.create(
        real_name = real_name,
        localbitcoins_real_name = user.real_name,
        company_name = user.company_name,
        #email = models.CharField(max_length=200, null = True, unique= True, blank= True)
        #phone_number = models.CharField(max_length=20, null = True, unique= True, blank= True)
        #telegram_username = models.CharField(max_length=20, null = True, unique= True, blank= True)

        localbitcoins_username = user.username,
        localbitcoins_feedback_score = user.feedback_score,
        localbitcoins_trade_count = user.trade_count,
        localbitcoins_country_code_phone_number = user.country_code_phone_number,
        localbitcoins_last_country_code_ip = user.last_country_code_ip,
        
        sumsub_external_user_id = user.username,

        name_match_checked  = user.name_match_checked,
        id_verified = user.id_verified,
        liveness_verified = user.liveness_verified,
        address_verified = user.address_verified,
        video_verified = user.video_verified,
        source_of_funds_verified = user.source_of_funds_verified,
        source_of_funds_limit = user.source_of_funds_limit,
        company_verified = user.company_verified,
    )

old_transactions = Transaction_old.objects.all()
for transaction in old_transactions:
    t = Transaction.objects.create(
        platform = 'LBC',
        client = Client.objects.get(localbitcoins_username = transaction.user.username),
        action = transaction.action,
        reference = transaction.reference,
        amount_fiat = transaction.amount_fiat,
        amount_btc = transaction.amount_btc,
        fee_btc = transaction.fee_btc,
        exchange_price = transaction.exchange_price,
        # client_bank_account_name = models.CharField(max_length= 50, default = None, null = True)
        # client_bank_account_number = models.CharField(max_length=8, default = None, null = True)
        # client_bank_account_sort_code = models.CharField(max_length=6, default = None, null = True)
        bank_account_name = transaction.bank_account_name,
        bank_account_number = transaction.bank_account_number,
        bank_account_sort_code = transaction.bank_account_sort_code,
        localbitcoins_contact_id = transaction.contact_id,
        #btc_txid = models.CharField(max_length = 64, editable= False, null= True, blank= True)
        #btc_address = models.CharField(max_length = 64, editable = True, null= True, blank= True)
        status = transaction.status,

        created_at = transaction.created_at,
        payment_completed_at = transaction.payment_completed_at,
        closed_at = transaction.payment_completed_at,
        pre_transaction_verification_tier = transaction.pre_transaction_verification_tier,
    )
    print(t.localbitcoins_contact_id)

print('end -------------------------')
applications = Application.objects.all()
for application in applications:
    print(application.user.username)
    application.client = Client.objects.get(localbitcoins_username = application.user.username)
    application.save()

iddocs = IdDoc.objects.all()
for iddoc in iddocs:
    iddoc.client = Client.objects.get(localbitcoins_username = iddoc.user.username)
    print(iddoc.user.username)
    iddoc.save()

addressdocs = AddressDoc.objects.all()
for addressdoc in addressdocs:
    addressdoc.client = Client.objects.get(localbitcoins_username = addressdoc.user.username)
    print(addressdoc.user.username)
    addressdoc.save()

persons = Person.objects.all()
for person in persons:
    person.client = Client.objects.get(localbitcoins_username = person.user.username)
    print(person.user.username)
    person.save()


User.objects.all().delete()