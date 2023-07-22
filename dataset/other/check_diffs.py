import difflib
comms_neg = {'d6a51edc3e1cc7e7890b551c4f85d996e208153a', 'a5335eb51e6f26be07617599aa100fa18e5c3bb3', '7626b811492867af0eb76972135fd9e57f89badf', '4f38cab0095951af83ea628611c27363b3038c93', 'ac5035cb0c469261b27bbc1b290deb2d211bf0eb'}
neg = ds.filter(lambda x: x["commit"] in comms_neg)
diff = difflib.ndiff(neg[1]["old_contents"], neg[1]["new_contents"])
for i,s in enumerate(diff):
    if s[0]==' ': continue
    elif s[0]=='-':
        print(u'Delete "{}" from position {}'.format(s[-1],i))
    elif s[0]=='+':
        print(u'Add "{}" to position {}'.format(s[-1],i))  