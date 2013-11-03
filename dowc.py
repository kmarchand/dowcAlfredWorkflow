#!/usr/bin/python

import os
import plistlib
from datetime import datetime, timedelta
from sys import argv
import tempfile
import xml.etree.ElementTree as ET

keywords = []

if len('{query}') < 2:
    keywords.append('All words')
else:
    for kw in '{query}'.split():
        keywords.append(kw)

keywords = [kw for kw in keywords if argv[0] not in kw]


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


# find day one's dayone.plist config file

do_config = find('dayone.plist', os.environ['HOME'] + '/Library')


# parse dayone.plist to find location of active journal and list entries

config_dict = plistlib.readPlist(do_config)
journal_path = config_dict['JournalPackageURL'] + '/entries/'
entries_list = os.listdir(journal_path)

date_content = {}

for entry in entries_list:
    try:
        entry_dict = plistlib.readPlist(journal_path + entry)
        timestamp = entry_dict['Creation Date']
        date_content[timestamp] = entry_dict['Entry Text']
    except:
        pass

keyword_count = {}

for kw in keywords:

    keyword_count[kw + ' - past week'] = 0
    keyword_count[kw + ' - past month'] = 0
    keyword_count[kw + ' - past year'] = 0
    keyword_count[kw + ' - all time'] = 0

    for timestamp in date_content.keys():
        if timestamp > datetime.now() - timedelta(weeks=1):
            for word in date_content[timestamp].replace("'s", '').split():
                if kw.lower() in [word.lower().strip(",."), 'all words']:
                    keyword_count[kw + ' - past week'] += 1
                else:
                    pass
        else:
            pass
        if timestamp > datetime.now() - timedelta(weeks=4):
            for word in date_content[timestamp].replace("'s", '').split():
                if kw.lower() in [word.lower().strip(",."), 'all words']:
                    keyword_count[kw + ' - past month'] += 1
                else:
                    pass
        else:
            pass
        if timestamp > datetime.now() - timedelta(weeks=52):
            for word in date_content[timestamp].replace("'s", '').split():
                if kw.lower() in [word.lower().strip(",."), 'all words']:
                    keyword_count[kw + ' - past year'] += 1
                else:
                    pass
        else:
            pass
        for word in date_content[timestamp].replace("'s", '').split():
            if kw.lower() in [word.lower().strip(",."), 'all words']:
                keyword_count[kw + ' - all time'] += 1
            else:
                pass


# Generate Alfred's XML

# root = ET.Element('items')

# for kw in keywords:

#     for period in ['past week', 'past month', 'past year', 'all time']:

#         item = ET.SubElement(root, 'item')
#         item.set('uid', "'%s' in %s" % (kw, period))
#         item.set('arg', '/Applications/Day One.app')

#         title = ET.SubElement(item, 'title')
#         title.text = "'%s' in %s: %s" % (
#             kw, period, keyword_count[kw + ' - ' + period])

# subtitle = ET.SubElement(item, 'subtitle')
# subtitle.text = 'iCloud Device: '+device_name

#         icon = ET.SubElement(item, 'icon')
#         icon.set('type', 'fileicon')
#         icon.text = '/Applications/Day One.app'

# print ET.tostring(root)

root = ET.Element('items')

for kw in keywords:

    item = ET.SubElement(root, 'item')
    item.set('uid', kw)
    item.set('arg', '/Applications/Day One.app')

    title = ET.SubElement(item, 'title')
    title.text = "'%s'\tweek: %s, month: %s, year: %s, all: %s" % (
        kw,
        keyword_count[kw + ' - past week'],
        keyword_count[kw + ' - past month'],
        keyword_count[kw + ' - past year'],
        keyword_count[kw + ' - all time'])

    icon = ET.SubElement(item, 'icon')
    icon.set('type', 'fileicon')
    icon.text = '/Applications/Day One.app'

print ET.tostring(root)
