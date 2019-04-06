--- lists.py	(original)
+++ lists.py	(refactored)
@@ -5,7 +5,7 @@
 import requests
 import json
 try:
-    import urlparse
+    import urllib.parse
 except ImportError:
     from urllib import parse as urlparse
 from config import MailChimpConfig
@@ -13,7 +13,7 @@
 
 config = MailChimpConfig()
 
-endpoint = urlparse.urljoin(config.api_root, 'lists')
+endpoint = urllib.parse.urljoin(config.api_root, 'lists')
 params = {
     # With Partial Response, you choose which fields you want to see
     'fields': 'lists.id,lists.name,lists.stats.member_count',
@@ -31,11 +31,11 @@
       response.raise_for_status()
       body = response.json()
     except requests.exceptions.HTTPError as err:
-        print "Error: {} {}".format(str(response.status_code), err)
-        print json.dumps(response.json(), indent=4)
+        print("Error: {} {}".format(str(response.status_code), err))
+        print(json.dumps(response.json(), indent=4))
         break
     except ValueError:
-        print "Cannot decode json, got %s" % response.text
+        print("Cannot decode json, got %s" % response.text)
         break
 
     if len(body['lists']) == 0:
@@ -44,11 +44,11 @@
     total_lists += len(body['lists'])
 
     for user_list in body['lists']:
-        print u'%s: %s (Subscribers: %s)' % (
+        print('%s: %s (Subscribers: %s)' % (
             user_list['id'],
             user_list['name'],
-            user_list['stats']['member_count'])
+            user_list['stats']['member_count']))
 
     params['offset'] += params['count']
 
-print "\n" + str(total_lists) + " lists found."
+print("\n" + str(total_lists) + " lists found.")
