#!/usr/bin/env python


# For us it will be /lists/


# client.lists.members.create_or_update(list_id, subscriber_hash, data)


# PUT /lists/{list_id}/members/{subscriber_hash}
# Add or update a list member.

# Path parameters
# list_id=LIST_ID
# subscriber_hash=subscriber_hash(email)

# Request body parameters
# email_address = row['email']
# status_if_new = 'subscribed'
# email_type = 'html'
# status = 'sbuscribed'

# PHP
# 	'merge_fields' => [
# 		'FNAME' => 'Daffy',
# 		'LNAME' => 'Duck',
# 		'ADDRESS' =>  array(
# 			'addr1' => '4000 Warner Boulevard',
# 			'city' => 'Burbank',
# 			'state' => 'California',
# 			'zip' => '91522',
# 			'country' => 'US'



# Type:
# Object
# Title:
# Member Merge Var
# Read only:
# false	An individual merge var and value for a member.
# interests
# Type:
# Object
# Title:
# Subscriber Interests
# Read only:
# false	The key of this object’s properties is the ID of the interest in question.
# language
# Type:
# String
# Title:
# Language
# Read only:
# false	If set/detected, the subscriber’s language.
# vip
# Type:
# Boolean
# Title:
# VIP
# Read only:
# false	VIP status for subscriber.
# location
# Type:
# Object
# Title:
# Location
# Read only:
# false	Subscriber location information.
# Show properties
# marketing_permissions
# Type:
# Array
# Title:
# Marketing Permissions
# Read only:
# false	The marketing permissions for the subscriber.
# Show properties
# ip_signup
# Type:
# String
# Title:
# Signup IP
# Read only:
# false	IP address the subscriber signed up from.
# timestamp_signup
# Type:
# String
# Title:
# Signup Timestamp
# Read only:
# false	The date and time the subscriber signed up for the list in ISO 8601 format.
# ip_opt
# Type:
# String
# Title:
# Opt-in IP
# Read only:
# false	The IP address the subscriber used to confirm their opt-in status.
# timestamp_opt
# Type:
# String
# Title:
# Opt-in Timestamp
# Read only:
# false	The date and time the subscriber confirmed their opt-in status in ISO 8601 format.
