import datetime
import hashlib
import hmac
import json
import requests
import config

host = 'webservices.amazon.com'
region = 'us-east-1'
service = 'ProductAdvertisingAPI'
endpoint = f'https://{host}/paapi5/searchitems'
target = 'com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems'
content_encoding = 'amz-1.0'
content_type = 'application/json; charset=utf-8'

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature_key(key, date_stamp, region_name, service_name):
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing

def search_amazon_deals(keywords, min_discount=20):
    if isinstance(keywords, str):
        keywords = [keywords]

    deals = []

    for keyword in keywords:
        print(f"🔍 Searching keyword: {keyword}")
        payload = {
            "Operation": "SearchItems",
            "Keywords": keyword,
            "SearchIndex": "All",
            "Resources": [
                "ItemInfo.Title",
                "Offers.Listings.Price",
                "Images.Primary.Medium"
            ],
            "PartnerTag": config.AMAZON_ASSOCIATE_TAG,
            "PartnerType": "Associates",
            "Marketplace": "www.amazon.com"
        }
        payload_json = json.dumps(payload, separators=(',', ':'))

        now = datetime.datetime.utcnow()
        amz_date = now.strftime('%Y%m%dT%H%M%SZ')
        date_stamp = now.strftime('%Y%m%d')

        canonical_uri = '/paapi5/searchitems'
        canonical_headers = (
            f'content-encoding:{content_encoding}\n'
            f'content-type:{content_type}\n'
            f'host:{host}\n'
            f'x-amz-date:{amz_date}\n'
            f'x-amz-target:{target}\n'
        )
        signed_headers = 'content-encoding;content-type;host;x-amz-date;x-amz-target'
        payload_hash = hashlib.sha256(payload_json.encode('utf-8')).hexdigest()
        canonical_request = '\n'.join([
            'POST',
            canonical_uri,
            '',
            canonical_headers,
            signed_headers,
            payload_hash
        ])

        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = f'{date_stamp}/{region}/{service}/aws4_request'
        string_to_sign = '\n'.join([
            algorithm,
            amz_date,
            credential_scope,
            hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()
        ])

        signing_key = get_signature_key(config.AMAZON_SECRET_KEY, date_stamp, region, service)
        signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

        authorization_header = (
            f'{algorithm} Credential={config.AMAZON_ACCESS_KEY}/{credential_scope}, '
            f'SignedHeaders={signed_headers}, Signature={signature}'
        )

        headers = {
            'Content-Encoding': content_encoding,
            'Content-Type': content_type,
            'Host': host,
            'X-Amz-Date': amz_date,
            'X-Amz-Target': target,
            'Authorization': authorization_header
        }

        response = requests.post(endpoint, headers=headers, data=payload_json)
        if response.status_code != 200:
            print(f"⚠️ Error fetching {keyword}:", response.status_code, response.text)
            continue

        try:
            data = response.json()
            items = data.get('SearchResult', {}).get('Items', [])
            for item in items:
                # Check if price data exists
                offers = item.get('Offers', {}).get('Listings', [])
                if not offers:
                    continue

                price_info = offers[0].get('Price', {})
                amount = price_info.get('Amount', 0)
                savings = price_info.get('Savings', {}).get('Percentage', 0)
                price = price_info.get('DisplayAmount', 'N/A')

                # Calculate original price
                if amount and savings:
                    original_price = round(amount / (1 - (savings / 100)), 2)
                    original_price_str = f"${original_price:.2f}"
                else:
                    original_price_str = None

                asin = item.get('ASIN')
                title = item.get('ItemInfo', {}).get('Title', {}).get('DisplayValue', 'No Title')
                image_url = item.get('Images', {}).get('Primary', {}).get('Medium', {}).get('URL', None)
                url = f"https://www.amazon.com/dp/{asin}/?tag={config.AMAZON_ASSOCIATE_TAG}"

                if savings >= min_discount:
                    deals.append({
                        'asin': asin,
                        'title': title,
                        'price': price,
                        'original_price': original_price_str,
                        'discount': savings,
                        'url': url,
                        'image': image_url
                    })

        except Exception as e:
            print("Error parsing response:", str(e))

    return deals
