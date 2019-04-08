a=client.lists.members.all(LIST_ID, get_all=True)
m=a['members']

good_tags = ['fmr_donations_count',
             'fmr_donations_amount',
             'PAID',
             'PAID_family

def
for x in m:
    ...:     for t in x['tags']:
    ...:         n = t['name']
    ...:         ns = n.split(':')
    ...:         n1 = ns[0]
    ...:         try:
    ...:             n2 = ns[1]
    ...:             tag_values[n1].add(n2)
    ...:         except:
    ...:             pass
