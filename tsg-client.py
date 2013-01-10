#!/usr/bin/python
import httplib2
import sys
import xmltodict
import json

try:
    # python2.6+
    import xml.etree.cElementTree as ET
except:
    # earlier versions
    # Python 2.4+ should have iterparse
    import cElementTree as ET

#parse xml response
def parse_xml(response):
    result = {}
    element = ET.fromstring(response)
    e = element.find('result')
    result['result'] = None
    if e is not None:
        result['result'] = e.text
    e = element.find('result_code')
    result['result_code'] = None
    if e is not None:
        result['result_code'] = e.text
    e = element.find('display_message')
    result['display_message'] = None
    if e is not None:
        result['display_message'] = e.text
    e = element.find('id')
    result['id'] = None
    if e is not None:
        result['id'] = e.text
    e = element.find('authorization_code')
    result['authorization_code'] = None
    if e is not None:
        result['authorization_code'] = e.text
    e = element.find('error_code')
    result['error_code'] = None
    if e is not None:
        result['error_code'] = e.text
        
    return result

#parse json response    
def parse_json(response):
    result = {}
    element = json.loads(response)["transaction"]
    result['result'] = element.get("result", None)
    result['result_code'] = element.get("result_code", None)
    result['display_message'] = element.get("display_message", None)
    result['id'] = element.get("id", None)
    result['authorization_code'] = element.get("authorization_code", None)
    result['error_code'] = element.get("error_code", None)
           
    return result

if __name__ == '__main__':
    
    #Settings
    APIURL = ''
    APIKEY = ''
    TIMEOUT = 15
    CONN = httplib2.Http(timeout=TIMEOUT, disable_ssl_certificate_validation=True)
    LANG_TYPE = '' #'xml' or 'json'
    
    try:
        
        #Xml transaction request
        XML_TRANSACTION_REQUEST = """<?xml version="1.0" encoding="utf-8"?>
<transaction>
    <api_key>%(APIKEY)s</api_key>
    <type>%(type)s</type>
    <card>%(card_number)s</card>
    <csc>%(card_csc)s</csc>
    <exp_date>%(expiry_date)s</exp_date>
    <amount>%(amount)s</amount>
    <avs_address>%(avs_address)s</avs_address>
    <avs_zip>%(avs_zip)s</avs_zip>
    <email>%(email)s</email>
    <customer_id>%(customer_id)s</customer_id>
    <order_number>%(order_number)s</order_number>
    <purchase_order>%(purchase_order)s</purchase_order>
    <invoice>%(invoice)s</invoice>
    <client_ip>%(client_ip)s</client_ip>
    <description>%(description)s</description>
    <comments>%(comments)s</comments>
    <billing>
        <first_name>%(billing_first_name)s</first_name>
        <last_name>%(billing_last_name)s</last_name>
        <company>%(billing_company)s</company>
        <street>%(billing_address1)s</street>
        <street2>%(billing_address2)s</street2>
        <city>%(billing_city)s</city>
        <state>%(billing_state)s</state>
        <zip>%(billing_zip)s</zip>
        <country>%(billing_country)s</country>
        <phone>%(billing_phone)s</phone>
    </billing>
    <shipping>
        <first_name>%(shipping_first_name)s</first_name>
        <last_name>%(shipping_last_name)s</last_name>
        <company>%(shipping_company)s</company>
        <street>%(shipping_address1)s</street>
        <street2>%(shipping_address2)s</street2>
        <city>%(shipping_city)s</city>
        <state>%(shipping_state)s</state>
        <zip>%(shipping_zip)s</zip>
        <country>%(shipping_country)s</country>
        <phone>%(shipping_phone)s</phone>
    </shipping>
</transaction>""" % {'APIKEY' : APIKEY,
                    'type' : 'SALE',
                    'card_number' : '4111111111111111',
                    'card_csc' : '123',
                    'expiry_date' : '1121',
                    'amount' : '10.00',
                    'avs_address' : '112 N. Orion Court',
                    'avs_zip' : '20210',
                    'purchase_order' : '10',
                    'invoice' : '100',
                    'email' : 'email@tsg.com',
                    'customer_id' : '25',
                    'order_number' : '1000',
                    'client_ip' : '',
                    'description' : 'Cel Phone',
                    'comments' : 'Electronic Product',
                    'billing_first_name' : 'Joe',
                    'billing_last_name' : 'Smith',
                    'billing_company' : 'Company Inc.',
                    'billing_address1' : 'Street 1',
                    'billing_address2' : 'Street 2',
                    'billing_city' : 'Jersey City',
                    'billing_state' : 'NJ',
                    'billing_zip' : '07097',
                    'billing_country' : 'USA',
                    'billing_phone' : '123456789',
                    'shipping_first_name' : 'Joe',
                    'shipping_last_name' : 'Smith',
                    'shipping_company' : 'Company 2 Inc.',
                    'shipping_address1' : 'Street 1 2',
                    'shipping_address2' : 'Street 2 2',
                    'shipping_city' : 'Colorado City',
                    'shipping_state' : 'TX',
                    'shipping_zip' : '79512',
                    'shipping_country' : 'USA',
                    'shipping_phone' : '123456789'}
		
        if LANG_TYPE == 'json': #if JSON is chosen, convert the XML request generated to a JSON request
            temp = xmltodict.parse(XML_TRANSACTION_REQUEST) # convert previous builded XML request to a dictionary
            JSON_REQ = temp["transaction"]                  # take the value of "transaction" key into JSON_REQ
            #Server doesn't process next fields for JSON requests, so they are excluded from the request
            JSON_REQ.pop("avs_address")                     
            JSON_REQ.pop("avs_zip")
            
            TRANSACTION_REQUEST = json.dumps(JSON_REQ, sort_keys=True, indent=4, separators=(',', ': ')) #turn the JSON_REQ dictionary into a JSON well-formed string
        else: #if XML is chosen, use the generated xml transaction request
            TRANSACTION_REQUEST = XML_TRANSACTION_REQUEST
       
        print "-----------------------------------------------------"
        print "REQUEST TO URL: " + APIURL;
        print "POST DATA: \n" + TRANSACTION_REQUEST
        
        #Execute Request
        HEADERS = {"Content-type": "application/"+LANG_TYPE, "Accept": "application/"+LANG_TYPE}
        response, content = CONN.request(APIURL, method='POST', body=TRANSACTION_REQUEST, headers=HEADERS)
        
        print "-----------------------------------------------------"
        print "RESPONSE DATA: \n" + content

        #Handle Response       
        if response['status'] == '200': #http status 200
            if LANG_TYPE == 'xml': # if the chosen language was XML, then the server will respond back with XML
                if '<transaction>' in content: 
                    result = parse_xml(content) #parse xml response
            else:# if the chosen language was JSON, then the server will respond back with JSON
                 if "transaction" in content:
                    result = parse_json(content) #parse json response
            #parse response according to its content
            if result['result_code'] and result['result_code'] == '0000':
                print "-----------------------------------------------------"
                print "TRANSACTION APPROVED: " + result['authorization_code'] 
            else:
                code = ""
                if result['error_code']:
                    code = result['error_code']
                if result['result_code']:
                    code = result['result_code']
                print "-----------------------------------------------------"
                print "TRANSACTION ERROR: Code=" + code + " Message=" + result['display_message'];
            
            
            
    except Exception: 
        print "Unexpected error:", str(sys.exc_info())
