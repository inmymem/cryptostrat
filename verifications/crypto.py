import json
import requests 
from .sumsub import sign_and_send_request, api_url
from .models import CryptoAddressAnalysis, CryptoTransactionAnalysis


def analyse_address(address):
    """To analyse"""
#
    end_url = f'/resources/standalone/crypto/btc/wallet/{address}/info'
    request_method = 'GET'
    parameters = None
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        }
    body = ''
    body = json.dumps(body)
    request = requests.Request(request_method, url=(api_url+end_url),headers= headers, data = body, params = parameters)
    response = sign_and_send_request(request)
    if response.status_code == 200:
        analysis_result = response.json()['data']
        address_analysis = create_address_analysis(analysis_result)
        return address_analysis
    return None


def analyse_transaction(txid, address):
    end_url = f'/resources/standalone/crypto/btc/txn/{txid}/info'
    request_method = 'GET'
    parameters = None
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        }
    body = ''#{'currency': currency, 'direction': direction, 'txn': txn, 'address': address}
    body = json.dumps(body)

    request = requests.Request(request_method, url=(api_url+end_url),headers= headers, data = body, params = parameters)
    response = sign_and_send_request(request)
    if response.status_code == 200:
        analysis_result = response.json()['data']
        transaction_analysis = create_transaction_analysis(analysis_result, txid, address)
    return transaction_analysis

# def analyse_address2(address):
#     x = {'data': {'address': 'bc1qjl8uwezzlech723lpnyuza0h2cdkvxvh54v3dn', 'balance': 28468059509, 'owner': {'id': 332249289, 'name': 'BTC.com', 'slug': 'BTC.com', 'type': 'miner', 'size': 125, 'grade': 2, 'status': 'active', 'subtype': None, 'website': None, 'firstActivity': '2017-08-25 04:02:49', 'lastActivity': '2020-06-10 14:05:01'}, 'received': 20226263725874, 'riskscore': {'value': 0.0, 'signals': {'dark_market': 0.0, 'dark_service': 0.0, 'exchange': 0.0, 'gambling': 0.0, 'illegal_service': 0.0, 'marketplace': 0.0, 'miner': 1.0, 'mixer': 0.0, 'payment': 0.0, 'ransom': 0.0, 'scam': 0.0, 'stolen_coins': 0.0, 'trusted_exchange': 0.0, 'wallet': 0.0}, 'updated': [{'time': 1591453213, 'type': 'global'}, {'time': 1591797103, 'type': 'fast'}]}, 'status': 'active', 'firstActivity': '2018-07-31 16:02:50', 'lastActivity': '2020-06-10 14:05:01', 'nTx': 16586, 'sharedBalance': 0, 'sharedReceived': 0, 'type': None}, 'meta': {'calls_left': 5247, 'calls_used': 14753, 'error_code': 0, 'error_message': '', 'server_time': 1591798100}}
#     analysis_result =x['data']
#     address_analysis = create_address_analysis(analysis_result)
#     return address_analysis
# def analyse_transaction2(txid, address):
#     x = {
#     'data': {
#         'additional': {}, 
#         'block': {
#             'hash': '0000000000000000000c89805f0455c7dc77d51b5b7cac2202ae7c6e23f58714', 
#             'height': 634089
#             }, 
#         'block_time': 1591816101, 
#         'confirmations': 1, 
#         'count_in': 1, 
#         'count_out': 2, 
#         'fiat_rate': 9837.396, 
#         'hash': '765c3acf95cacc9651f7934df3a64ca8b6c148bc64bf2a780da130ca7cb10df0', 
#         'inputs': [
#             {
#                 'address': 'bc1qwqdg6squsna38e46795at95yu9atm8azzmyvckulcc7kytlcckxswvvzej', 
#                 'amount': 5012676, 
#                 'owner': {
#                     'id': '434359850', 
#                     'name': 'bitFlyer', 
#                     'slug': 'bitFlyer', 
#                     'subtype': None, 
#                     'type': 'trusted_exchange'
#                     }, 
#                 'riskscore': 0
#                 }
#             ], 
#         'outputs': [
#             {
#                 'address': '3PXkjiH28kswvJxuH6ym3j3gT5zdVfp7wN', 
#                 'amount': 2403788, 
#                 'riskscore': 0.0
#                 }, 
#             {
#                 'address': 'bc1qwqdg6squsna38e46795at95yu9atm8azzmyvckulcc7kytlcckxswvvzej', 
#                 'amount': 2568888, 
#                 'owner': {
#                     'id': '434359850', 
#                     'name': 'bitFlyer', 
#                     'slug': 'bitFlyer', 
#                     'subtype': None, 
#                     'type': 'trusted_exchange'
#                     }, 
#                 'riskscore': 0
#                 }
#             ], 
#         'pool_time': 1591815896, 
#         'riskscore': {
#             'signals': {
#                 'atm': 0.0, 
#                 'dark_market': 0.0, 
#                 'dark_service': 0.0, 
#                 'exchange': 0.0, 
#                 'gambling': 0.0, 
#                 'illegal_service': 0.0, 
#                 'marketplace': 0.0, 
#                 'miner': 0.0, 
#                 'mixer': 0.0, 
#                 'payment': 0.0, 
#                 'ransom': 0.0, 
#                 'risky_exchange': 0.0, 
#                 'scam': 0.0, 
#                 'stolen_coins': 0.0, 
#                 'trusted_exchange': 1.0, 
#                 'wallet': 0.0
#                 }, 
#             'value': 0.0
#             }, 
#         'size': 380, 
#         'total_in': 5012676, 
#         'total_out': 4972676, 
#         'untangled': {
#             'type': 'individual'
#             }, 
#         'weight': 760
#         }, 
#     'meta': {
#         'calls_left': 5010, 
#         'calls_used': 14990, 
#         'error_code': 0, 
#         'error_message': '', 
#         'fiat_code': 'usd', 
#         'riskscore_profile': {
#             'id': 0, 
#             'name': 'Default'
#             }, 
#         'server_time': 1591816370
#         }
#     }
    
#     analysis_result = x['data']
#     transaction_analysis = create_transaction_analysis(analysis_result, txid, address)
#     return transaction_analysis


def create_transaction_analysis(analysis_result, txid, address):
    transaction_analysis = CryptoTransactionAnalysis.objects.create(
        txid = txid,
        address = address,
        risk_score = analysis_result['riskscore']['value'],
        dark_market_signal = analysis_result['riskscore']['signals']['dark_market'],
        dark_service_signal = analysis_result['riskscore']['signals']['dark_service'],
        exchange_signal = analysis_result['riskscore']['signals']['exchange'],
        gambling_signal = analysis_result['riskscore']['signals']['gambling'],
        illegal_service_signal = analysis_result['riskscore']['signals']['illegal_service'],
        marketplace_signal = analysis_result['riskscore']['signals']['marketplace'],
        miner_signal = analysis_result['riskscore']['signals']['miner'],
        mixer_signal = analysis_result['riskscore']['signals']['mixer'],
        payment_signal = analysis_result['riskscore']['signals']['payment'],
        ransom_signal = analysis_result['riskscore']['signals']['ransom'],
        scam_signal = analysis_result['riskscore']['signals']['scam'],
        stolen_coins_signal = analysis_result['riskscore']['signals']['stolen_coins'],
        trusted_exchange_signal = analysis_result['riskscore']['signals']['trusted_exchange'],
        wallet_signal = analysis_result['riskscore']['signals']['wallet'],
        atm_signal = analysis_result['riskscore']['signals']['atm'],
        risky_exchange_signal = analysis_result['riskscore']['signals']['risky_exchange'],
    )
    return transaction_analysis

# analyse_transaction('765c3acf95cacc9651f7934df3a64ca8b6c148bc64bf2a780da130ca7cb10df0')
#analyse_address('bc1qjl8uwezzlech723lpnyuza0h2cdkvxvh54v3dn')
def create_address_analysis(analysis_result):
    updates = analysis_result['riskscore']['updated']
    last_updated_global = None
    last_updated_fast = None
    for update in updates:
        if update['type'] == 'global':
            last_updated_global = update['time']
        elif update['type'] == 'fast':
            last_updated_fast = update['time']
        

    crypto_address_analysis = CryptoAddressAnalysis.objects.create(
        address = analysis_result['address'],
        risk_score = analysis_result['riskscore']['value'],
        dark_market_signal = analysis_result['riskscore']['signals']['dark_market'],
        dark_service_signal = analysis_result['riskscore']['signals']['dark_service'],
        exchange_signal = analysis_result['riskscore']['signals']['exchange'],
        gambling_signal = analysis_result['riskscore']['signals']['gambling'],
        illegal_service_signal = analysis_result['riskscore']['signals']['illegal_service'],
        marketplace_signal = analysis_result['riskscore']['signals']['marketplace'],
        miner_signal = analysis_result['riskscore']['signals']['miner'],
        mixer_signal = analysis_result['riskscore']['signals']['mixer'],
        payment_signal = analysis_result['riskscore']['signals']['payment'],
        ransom_signal = analysis_result['riskscore']['signals']['ransom'],
        scam_signal = analysis_result['riskscore']['signals']['scam'],
        stolen_coins_signal = analysis_result['riskscore']['signals']['stolen_coins'],
        trusted_exchange_signal = analysis_result['riskscore']['signals']['trusted_exchange'],
        wallet_signal = analysis_result['riskscore']['signals']['wallet'],
        last_updated_global = last_updated_global,
        last_updated_fast = last_updated_fast,
    )
    return crypto_address_analysis


# print('hiiiiii')
#analyse_transaction('37757922b10c25bba087f2eb2d7ffdde02f7a1ffd8dc6090672bf51ce84cf470', '3Kn3QmNhcEb4Qqkr4q46ZNCHLXLiZ4H2w7')
#analyse_address('3Kn3QmNhcEb4Qqkr4q46ZNCHLXLiZ4H2w7')

# For the ones attached to an applicant if you want to use them in the future
# def scan_address(applicantId, currency, direction, txn, address):
#     """To get the detailed applicant data that was extracted after the review process. 
#     E.G ID doc details, address details..."""
# #
#     end_url = f'/resources/applicantActions/-/forApplicant/{applicantId}/cryptoTransaction'
#     request_method = 'POST'
#     parameters = None
#     headers = {
#         'Accept': 'application/json',
#         'Content-Type': 'application/json',
#         }
#     body = {'currency': currency, 'direction': direction, 'txn': txn, 'address': address}
#     body = json.dumps(body)

    


#     request = requests.Request(request_method, url=(api_url+end_url),headers= headers, data = body, params = parameters)
#     response = sign_and_send_request(request)
#     print(response.json())
#     analysis_result = response.json()
#     update_or_create_crypto_analysis(analysis_result)
#     return None

# def update_or_create_crypto_analysis(analysis_result):
#     CryptoAnalysis.objects.update_or_create(
#         #user = ##########
#         applicant_id = analysis_result['applicantId'],
#         currency = analysis_result['input']['cryptoTxnInfo']['currency'],
#         txn = analysis_result['input']['cryptoTxnInfo']['txn'],
#         address = analysis_result['input']['cryptoTxnInfo']['address'],
#         direction = analysis_result['input']['cryptoTxnInfo']['direction'],
#         defaults = {
#             'review_answer': analysis_result['review']['reviewResult']['reviewAnswer'],
#             'review_status': analysis_result['review']['reviewStatus'],
#             'autochecked': analysis_result['review']['autoChecked'],
#             'risk_score': analysis_result['paymentChecks']['cryptoTxnRiskScoreInfo']['riskScore'],
#             'dark_market_signal': analysis_result['paymentChecks']['cryptoTxnRiskScoreInfo']['txnMonitorData']['signals']['dark_market'],
#             'dark_service_signal': analysis_result['paymentChecks']['cryptoTxnRiskScoreInfo']['txnMonitorData']['signals']['dark_service'],
#             'exchange_signal': analysis_result['paymentChecks']['cryptoTxnRiskScoreInfo']['txnMonitorData']['signals']['exchange'],
#             'gambling_signal': analysis_result['paymentChecks']['cryptoTxnRiskScoreInfo']['txnMonitorData']['signals']['gambling'],
#             'illegal_service_signal': analysis_result['paymentChecks']['cryptoTxnRiskScoreInfo']['txnMonitorData']['signals']['illegal_service'],
#             'marketplace_signal': analysis_result['paymentChecks']['cryptoTxnRiskScoreInfo']['txnMonitorData']['signals']['marketplace'],
#             'miner_signal': analysis_result['paymentChecks']['cryptoTxnRiskScoreInfo']['txnMonitorData']['signals']['miner'],
#             'mixer_signal': analysis_result['paymentChecks']['cryptoTxnRiskScoreInfo']['txnMonitorData']['signals']['mixer'],
#             'payment_signal': analysis_result['paymentChecks']['cryptoTxnRiskScoreInfo']['txnMonitorData']['signals']['payment'],
#             'ransom_signal': analysis_result['paymentChecks']['cryptoTxnRiskScoreInfo']['txnMonitorData']['signals']['ransom'],
#             'scam_signal': analysis_result['paymentChecks']['cryptoTxnRiskScoreInfo']['txnMonitorData']['signals']['scam'],
#             'stolen_coins_signal': analysis_result['paymentChecks']['cryptoTxnRiskScoreInfo']['txnMonitorData']['signals']['stolen_coins'],
#             'trusted_exchange_signal': analysis_result['paymentChecks']['cryptoTxnRiskScoreInfo']['txnMonitorData']['signals']['trusted_exchange'],
#             'wallet_signal': analysis_result['paymentChecks']['cryptoTxnRiskScoreInfo']['txnMonitorData']['signals']['wallet'],
#             'status': analysis_result['paymentChecks']['cryptoTxnRiskScoreInfo']['txnMonitorData']['status'],
#         }