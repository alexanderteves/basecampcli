# Basecamp CLI

Simple CLI tool to post messages to projects or add to to-do lists. Created for use in Jenkins CI jobs or other automated contexts.

## Usage
<pre>usage: basecampcli.py [-h] -a ACCOUNTID -u USERNAME -p PASSWORD -i PROJECTID
                      [-t TODOLISTID] [-s SUBJECT] [-n NOTIFY]

POST to Basecamp

POST either a message to a project or a todo to a project's todolist.

Examples:
	basecampcli.py -a 5668214 -u foo@bar.org -p 123many -i 2557963 -t 54771214           # todo
	basecampcli.py -a 5668214 -u foo@bar.org -p 123many -i 2557963 -s "My subject" -n 1  # message

optional arguments:
  -h, --help            show this help message and exit
  -a ACCOUNTID, --accountid ACCOUNTID
                        ID of the Basecamp account
  -u USERNAME, --username USERNAME
                        Username (will be an email address)
  -p PASSWORD, --password PASSWORD
                        Password for the user
  -i PROJECTID, --projectid PROJECTID
                        ID of the project to post to
  -t TODOLISTID, --todolistid TODOLISTID
                        ID of the todolist to post to
  -s SUBJECT, --subject SUBJECT
                        Message subject (omittable for todos)
  -n NOTIFY, --notify NOTIFY
                        0: nobody, 1: all subscribers (defaults to 0, omittable for todos)</pre>
