
import sys
import hashlib
import hmac
import base64
import json
import requests

class FirmamexServices:
    def __init__(self, webId, apikey):
        self.webId = webId
        self.apikey = apikey.encode('utf8');
        self.baseUrl = 'https://firmamex.com'

    def hashAndGet(self, path):
        dig = hmac.new(self.apikey, path.encode('utf8'), hashlib.sha256).digest()
        b64 = str(base64.b64encode(dig), 'utf8')
        url = self.baseUrl + path
        return str(self.get(b64, url), 'utf8')

    def hashAndPost(self, jsonParams, path):
        #print self.baseUrl, path        
        json_string = json.dumps(jsonParams, separators=(',', ':'))
        dig = hmac.new(self.apikey, json_string.encode('utf8'), hashlib.sha256).digest()
        b64 = str(base64.b64encode(dig), 'utf8')
        url = self.baseUrl + path
        return str(self.post(jsonParams, b64, url), 'utf8')

    def get(self, hmacb64, path):

        header = {
            "Authorization": "signmage " + self.webId + ":" + hmacb64,
            "Content-Type": "application/json"
        }

        resp = requests.get(path, headers=header)
        resp.raise_for_status()
        return resp.content
        
    def post(self, params, hmacb64, path):
        
        header = {
            "Authorization": "signmage " + self.webId + ":" + hmacb64,
            "Content-Type": "application/json"
        }

        resp = requests.post(path, json=params, headers=header)
        resp.raise_for_status()
        return resp.content

    def saveTemplate(self, params):
        return self.hashAndPost(params, '/developers/template/save')

    def getData(self, params):
        return self.hashAndPost(params, '/developers/webhook')

    def getDocument(self, docType, ticket):
        return self.hashAndGet('/api/document/' + docType + '/' + ticket)

    def getDocumentFromWebhook(self, params):
        return self.hashAndPost(params, '/developers/webhook')

    def docs(self, params):
        return self.hashAndPost(params, '/developers/docs')

    def deleteDocument(self, params):
        return self.hashAndPost(params, '/developers/delete/')    

    def restoreDocument(self, params):
        return self.hashAndPost(params, '/developers/restore/')

    def request(self, params):
       return self.hashAndPost(params, '/developers/json')

    def timestamp(self, hash):
        params = {
            "hash": hash
        }
        return json.loads(self.hashAndPost(params, '/api/timestamp'))

    def timestampValidateHash(self, hash, timestamp):
        params = {
            "hash": hash,
            "timestamp": str(base64.b64encode(timestamp), 'utf8')
        }
        return json.loads(self.hashAndPost(params, '/api/timestamp/validate'))

    def timestampValidate(self, file, timestamp):
        params = {
            "file": str(base64.b64encode(file), 'utf8'),
            "timestamp": str(base64.b64encode(timestamp), 'utf8')
        }
        return json.loads(self.hashAndPost(params, '/api/timestamp/validate'))

    def fileHash(self, binaryFile): 
        BLOCKSIZE = 65536
        hasher = hashlib.sha256()
        buf = binaryFile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = binaryFile.read(BLOCKSIZE)
        return hasher.digest()

    def hashAndPostFormData(self, binaryFile, path):
        sha256Base64 = str(base64.b64encode(hashlib.sha256(binaryFile).digest()), 'utf8')
        hmacDig = hmac.new(self.apikey, sha256Base64.encode('utf8'), hashlib.sha256).digest()
        hmacb64 = str(base64.b64encode(hmacDig), 'utf8')

        header = {
            "Authorization": "signmage " + self.webId + ":" + hmacb64,
            "Content-SHA256": sha256Base64
        }

        files = {
            "file": binaryFile
        }

        resp = requests.post(self.baseUrl + path, headers=header, files=files)
        resp.raise_for_status()
        return resp.json()

    def nom151Stamp(self, binaryFile):
        return self.hashAndPostFormData(binaryFile, '/api/nom151/stamp')

    def nom151Validate(self, binaryFile): 
        return self.hashAndPostFormData(binaryFile, '/api/nom151/validate')
    
    def report(self, ticket):
        return self.hashAndGet('/api/report/' + ticket)

    def downloadDocument(self, docType, ticket):
        return self.hashAndGet('/api/document/' + docType + '/' + ticket)

    def getReport(self, ticket):
        return self.hashAndGet('/api/report/' + ticket)



