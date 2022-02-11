from __future__ import print_function
from google.oauth2 import service_account
import googleapiclient.discovery

class authService():
    def __init__(self,scopes,jsonfile,email=None):
            self.userEmail = email
            self.SERVICE_ACCOUNT_FILE = jsonfile
            self.SCOPES = scopes
    def getService(self,*args,**kwargs):
            credentials = service_account.Credentials.from_service_account_file(
                    self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
            if self.userEmail is not None:                
                delegated_credentials = credentials.with_subject(self.userEmail)
                credentials = delegated_credentials

            return googleapiclient.discovery.build(args[0], args[1], credentials=credentials)
    def setScope(self,scopes):
            pass      