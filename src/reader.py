#!/usr/bin/env python

import csv
import hashlib
import pprint

from mailchimp3 import MailChimp

from phone import nanp_phone

with open('../vault/LIST_ID', 'r') as f:
    LIST_ID = f.read().strip()

with open('../vault/API_KEY', 'r') as f:
    API_KEY = f.read().strip()

with open('../vault/USER', 'r') as f:
    USER = f.read().strip()

DATA_FILE = "../data/original.tsv"

with open(DATA_FILE, 'r') as f:
    reader = csv.DictReader(f, delimiter='\t')
    raw = [row for row in reader]

client = MailChimp(mc_api=API_KEY, mc_user=USER)

# members ID within MC is subscriber hash
# which is the MD5 of the lowercase of the email address

def subscriber_hash(email):
    m = hashlib.md5()
    m.update(email.lower().encode('utf-8'))
    return m.hexdigest()

def generate_tags(r):
    tags = r['tag_list kee'].split(',')
    tags = [tag.strip(' ') for tag in tags]
    tags = [tag.replace(' ', '_') for tag in tags]
    return tags

COLUMNS = ["ID No", "prefix", "first_name", "middle_name", "last_name", "suffix", "full_name", "email", "website", "facebook_username", "twitter_login", "email_opt_in", "email1", "email2", "phone_number", "work_phone_number", "mobile_number", "mobile_opt_in", "primary_address1", "primary_address2", "primary_city", "primary_state", "primary_zip", "primary_country_code", "primary_country", "vecinos gmail", "tag_list kee", "Spouse / Notes", "donations_count", "donations_amount", "employer", "occupation"]

def make_data(row):

    return {'email_address': row['email'],
            'status_if_new': 'subscribed',
            'email_type': 'html',
            'status': 'subscribed',
            'merge_fields': {
                'FNAME': row['first_name'] or "UNKNOWN",
                'LNAME': row['last_name'] or "UNKNOWN",
                'ADDRESS': {'addr1': row['primary_address1'] or "UNKNOWN",
                            # might be wrong
                            'addr2': row['primary_address2'],
                            'city': row['primary_city'] or "UNKNOWN",
                            'state': row['primary_state'] or "UNKNOWN",
                            'zip': row['primary_zip'] or "UNKNOWN",
                            'country': row['primary_country'] or "UNKNOWN"},
                'PHONE': row['phone_number']
                }
            }

def make_data2(row):

    return {'email_address': row['email'],
            'status_if_new': 'subscribed',
            'email_type': 'html',
            'status': 'subscribed',
            'merge_fields': {
                'FNAME': row['first_name'] or "UNKNOWN",
                'LNAME': row['last_name'] or "UNKNOWN",
                'ADDRESS': {'addr1': row['primary_address1'] or "UNKNOWN",
                            # might be wrong
                            'addr2': row['primary_address2'],
                            'city': row['primary_city'] or "UNKNOWN",
                            'state': row['primary_state'] or "UNKNOWN",
                            'zip': row['primary_zip'] or "UNKNOWN",
                            'country': row['primary_country'] or "UNKNOWN"},
                'PHONE': row['phone_number'],
                'MOBILE': row['mobile_number']
                }
            }

def subscribe(row, list_id=LIST_ID):
    data = make_data(row)
    client.lists.members.create_or_update(list_id=LIST_ID,
                                          subscriber_hash=subscriber_hash(row['email']),
                                          data=data)

def update_phone(row, list_id=LIST_ID):
    phone_number = row['phone_number']
    ph = nanp_phone(phone_number)
    if ph:
        ph = str(ph)
        fmt = ("({area}) {prefix}-{suffix}"
               .format(area=ph[0:3],
                       prefix=ph[3:6],
                       suffix=ph[6:10]))
        data = {'email_address': row['email'],
                'status_if_new': 'subscribed',
                'email_type': 'html',
                'status': 'subscribed',
                'merge_fields': {
                    'PHONE': fmt}
               }
        client.lists.members.create_or_update(list_id=LIST_ID,
                                              subscriber_hash=subscriber_hash(row['email']),
                                              data=data)
    else:
        if phone_number:
            print("Not able to convert {p} to a 10-digit phone number"
                  .format(p=ph))
        # data = {'merge_fields': {
        #     'PHONE': ph}
        #         }
        # client.lists.members.create_or_update(list_id=LIST_ID,
        #                                       subscriber_hash=subscriber_hash(row['email']),
        #                                       data=data)


def translate_row(r):
    """Anything in 'tag_list kee' will become a regular tag, prefixed with tag_
Any column not otherwise handled will be transformed into a value tag fmr_{column}:{value}"""
    tags = generate_tags(r)
    def add_tag(col, converter=str):
        v = r[col]
        if v:
            ccol = 'fmr_' + col.lower().replace(" / ", "_").replace(" ", "_")
            tags.append(ccol + ":" + converter(v))
    add_tag("ID No")
    add_tag("prefix")
    # add_tag("first_name")
    add_tag("middle_name")
    # add_tag("last_name")
    add_tag("suffix")
    add_tag("full_name")
    # add_tag("email")
    add_tag("website")
    add_tag("facebook_username")
    add_tag("twitter_login")
    add_tag("email_opt_in")
    add_tag("email1")
    add_tag("email2")
    # add_tag("phone_number")
    add_tag("work_phone_number")
    add_tag("mobile_number")
    add_tag("mobile_opt_in")
    # add_tag("primary_address1")
    # add_tag("primary_address2")
    # add_tag("primary_city")
    # add_tag("primary_state")
    # add_tag("primary_zip")
    add_tag("primary_country_code")
    # add_tag("primary_country")
    add_tag("vecinos gmail")
    # add_tag("tag_list kee")
    add_tag("Spouse / Notes")
    add_tag("donations_count")
    add_tag("donations_amount")
    add_tag("employer")
    add_tag("occupation")
    return [tag for tag in tags if tag]


def update_tags(email, list_id=LIST_ID):
    data = {'tags': [{'name': 'aaaa'}]}
    client.lists.members.create_or_update(list_id=LIST_ID,
                                          subscriber_hash=subscriber_hash(email),
                                          data=data)


def update_tags(email, list_id=LIST_ID, add=None, delete=None):
    # delete
    if delete:
        data = {
            'tags': [{"name": tag, "status": "inactive"}
                     for tag in delete]
            }
        try:
            client.lists.members.tags.update(list_id=LIST_ID,
                                             subscriber_hash=subscriber_hash(email),
                                             data=data)
        except Exception as e:
            print("Failed to delete {data}: {e}"
                  .format(data=data, e=e))
    # add
    if add:
        data = {
            'tags': [{"name": tag, "status": "active"}
                     for tag in add]
            }
        try:
            client.lists.members.tags.update(list_id=LIST_ID,
                                             subscriber_hash=subscriber_hash(email),
                                             data=data)
        except Exception as e:
            print("Failed to delete {data}: {e}"
                  .format(data=data, e=e))



def update_mobile(email, list_id=LIST_ID, mobile=None):
    assert mobile
    shash = subscriber_hash(email)
    data = client.lists.members.get(list_id=LIST_ID, subscriber_hash=shash)

    useful = {"id": data["id"],
              "email_address": data["email_address"],
              "merge_fields": data["merge_fields"]}
    useful['merge_fields']['MOBILE'] = mobile
    client.lists.members.update(list_id=LIST_ID,
                                subscriber_hash=subscriber_hash(email),
                                data=data)

def update_website(email, list_id=LIST_ID, website=None):
    assert website
    shash = subscriber_hash(email)
    data = client.lists.members.get(list_id=LIST_ID, subscriber_hash=shash)

    useful = {"id": data["id"],
              "email_address": data["email_address"],
              "merge_fields": data["merge_fields"]}
    useful['merge_fields']['WEBSITE'] = website
    client.lists.members.update(list_id=LIST_ID,
                                subscriber_hash=subscriber_hash(email),
                                data=data)
