import os
import sys


class MailChimpConfig:
    def __init__(self):
        if os.path.isfile('../vault/API_KEY') == False:
            print("Please enter your API Key into the API_KEY file as mentioned in README.md")
            sys.exit()

        f = open('../vault/API_KEY', 'r+')
        apikey = f.read().strip()
        f.close()

        parts = apikey.split('-')
        if len(parts) != 2:
            print("This doesn't look like an API Key: " + apikey)
            print("The API Key should have both a key and a server name, separated by a dash, like this: abcdefg8abcdefg6abcdefg4-us1")
            sys.exit()

        self.apikey = apikey
        self.shard = parts[1]
        self.api_root = "https://" + self.shard + ".api.mailchimp.com/3.0/"
