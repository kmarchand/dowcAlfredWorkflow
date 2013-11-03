# Day One Word Search Alfred Workflow

This workflow parses entries from [Day One](https://dayone.zendesk.com) and counts instances of one or more words.  The totals for past week, month, year and all time are shown for each word selected.  If no words are specified, overall total word count is shown.

## Usage

* `dowc {word1} {word2}`
* Matching is not case sensitive
* Only full word matches are returned
* 's (apostrophe 's'), periods and commas are stripped out before matching
* Multiple occurences within the same entry are counted seperately


## Notes

* This script searches for dayone.plist in ~/Library and then parses that to find out where the journal is stored.
* After finding the entries, it will read the date and text contents of each entry.
* Nothing in the script attempts to write to the journal at all however please assure the contents are backed up prior to use.


## Changes

* November 3rd 2013; Initial upload