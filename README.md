# vibsearch
Utility for viber history search

# usage
python3 vsearch.py [-h] [--names] [--phones] [--messages] [--conv]
                            [--pattern PATTERN]
                            [namelist [namelist ...]]

Tool for Viber logs forensic

positional arguments:
  namelist              user names, space separated

optional arguments:
  -h, --help            show this help message and exit
  --names, -n           search for names
  --phones, -p          search for phones
  --messages, -m        search for messages
  --conv, -c            search for conversation
  --pattern PATTERN, -x PATTERN
                        filter messages by text pattern (case sensitive)


# examples
python3 vsearch.py # print help end exit
python3 vsearch.py -n # print all saved contact names
python3 vsearch.py -n Petro # print all saved contact names that match 'Petro' substring
python3 vsearch.py -p # print all saved contact names with phone numbers
python3 vsearch.py -m petro maRicHka Iryna # show all messages from 
                                           # 'Petro' 'Marichka' 'Iryna' (case insensitive matching works)
python3 vsearch.py -m Viktoria Oleh # show all conversation (messages from common chats) between Viktoria and Oleh
python3 vsearch.py -x lindenmann -m Viktoria Oleh # the same but with filtering by string 'lindenmann' (case sensitive)
