#!/usr/bin/python3

import argparse
import os
import sqlite3
import sys

CL_LINE1='\033[32m'
CL_LINE2='\033[33m'
CL_USERNAME='\033[93m'
CL_DATE='\033[33m'
CL_PAT='\033[91m'
CL_DEF='\033[0m'

localdir = [d for d in os.listdir(os.path.expanduser('~') +'/.ViberPC') if set(d) < set(['1','2','3','4','5','6','7','8','9','0'])][0]
filename = f"{os.path.expanduser('~')}/.ViberPC/{localdir}/viber.db"

def composite_name(a,b):
    if a and b:
        if a == b:
            return f"{a}"
        else:
            return f"{b} [{a}]"
    elif a:
        return f"{a}"
    else:
        return f"{b}"
    


def get_phone_numbers(names=['']):
    if type(names)==type(''):
        names = [names]
    def _craft_name(p):
        return f'{composite_name(*p[0:2])}: {p[2]}'
        if p[0] and p[1]:
            if p[0] == p[1]:
                return f"{p[1]}: {p[2]}"
            else:
                return f"{p[1]} [{p[0]}]: {p[2]}"
        elif p[0]:
            return f"{p[0]}: {p[2]}"
        else:
            return f"{p[1]}: {p[2]}"
    dump_phone="""
    SELECT Contact.Name AS Name,
     Contact.ClientName AS AltName,
     Contact.Number As Cellphone
    FROM Events 
     INNER JOIN Contact ON Events.ContactID = Contact.ContactID
     INNER JOIN Messages ON Events.EventID = Messages.EventID
    """
    con = sqlite3.connect(filename)
    cur = con.cursor()
    cur.execute(dump_phone)
    phones = [_craft_name(p)  for p in list(set(cur.fetchall())) if p[2]]

    clrs = [CL_LINE1, CL_LINE2]
    for i in sorted(phones):
        for n in names:
            if n.lower() in i.lower():
                print(clrs[0]+i+"\033[0m")
                clrs = clrs[::-1]
                break

def dump_names(names=['']):
    if type(names)==type(''):
        names = [names]
    dump_phone="""
    SELECT Contact.Name AS Name,
     Contact.ClientName AS AltName
    FROM Events 
     INNER JOIN Contact ON Events.ContactID = Contact.ContactID
     INNER JOIN Messages ON Events.EventID = Messages.EventID
    """
    con = sqlite3.connect(filename)
    cur = con.cursor()
    cur.execute(dump_phone)
    names_lst = [composite_name(*p)  for p in list(set(cur.fetchall()))]

    clrs = [CL_LINE1, CL_LINE2]
    for i in sorted(names_lst):
        for n in names:
            if n.lower() in i.lower():
                print(clrs[0]+i+"\033[0m")
                clrs = clrs[::-1]
                break


def dump_messages(names=[''], pattern=''):
    if type(names)==type(''):
        names = [names]
    dump_msges="""
    SELECT strftime('%Y-%m-%d %H:%M:%S',(Events.TimeStamp/1000),'unixepoch') AS Time, 
     Contact.Name AS Name,
     Contact.ClientName AS AltName,
     CASE Direction WHEN 0 THEN '<-' ELSE '->' END AS Direction,
     Messages.Body AS Message
    FROM Events 
     INNER JOIN Contact ON Events.ContactID = Contact.ContactID
     INNER JOIN Messages ON Events.EventID = Messages.EventID
    ORDER BY Time;
    """

    con = sqlite3.connect(filename)
    cur = con.cursor()
    cur.execute(dump_msges)
    for p in cur.fetchall():
        compos_name = composite_name(*p[1:3])
        for n in names:
            if n.lower() in compos_name.lower():
                if p[4]!=None and pattern in p[4]:
                    msg = p[4] if pattern=='' else p[4].replace(pattern, f"{CL_PAT}{pattern}{CL_DEF}")
                    print(f"{CL_DATE}{p[0]}>{CL_DEF} {CL_USERNAME}{compos_name}:{CL_DEF} {msg}")
                break


def dump_conversation(names=[''], pattern=''):
    if type(names)==type(''):
        names = [names]
    dump_msges="""
    SELECT strftime('%Y-%m-%d %H:%M:%S',(Events.TimeStamp/1000),'unixepoch') AS Time, 
     Contact.Name AS Name,
     Contact.ClientName AS AltName,
     CASE Direction WHEN 0 THEN '<-' ELSE '->' END AS Direction,
     Messages.Body AS Message,
     ChatID
    FROM Events 
     INNER JOIN Contact ON Events.ContactID = Contact.ContactID
     INNER JOIN Messages ON Events.EventID = Messages.EventID
    ORDER BY Time;
    """

    con = sqlite3.connect(filename)
    cur = con.cursor()
    cur.execute(dump_msges)
    response = cur.fetchall()
    ids = []
    for n in names:
        chat_ids = [p[5] for p in response if n.lower() in composite_name(*p[1:3]).lower()]
        ids += [chat_ids]
    common_ids = set(ids[0])
    for i in ids[1:]: common_ids = common_ids & set(i)

    for p in response:
        compos_name = composite_name(*p[1:3])
        if p[5] in common_ids:
            for n in names:
                if n.lower() in compos_name.lower():
                    if p[4]!= None and pattern in p[4]:
                        msg = p[4] if pattern=='' else p[4].replace(pattern, f"{CL_PAT}{pattern}{CL_DEF}")
                        print(f"{CL_DATE}{p[0]}>{CL_DEF} {CL_USERNAME}{compos_name}:{CL_DEF} {msg}")
                    break



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Tool for Viber logs forensic',
    )
    parser.add_argument('namelist', metavar='namelist', type=str, nargs='*', help='user names, space separated', default=[''])
    parser.add_argument('--names',   '-n', help='search for names', dest='name', action='store_true', required=False)
    parser.add_argument('--phones',   '-p', help='search for phones', dest='phone', action='store_true', required=False)
    parser.add_argument('--messages', '-m', help='search for messages', dest='msg', action='store_true', required=False, default=None)
    parser.add_argument('--conv', '-c', help='search for conversation', dest='convers', action='store_true', required=False, default=None)
    parser.add_argument('--pattern', '-x', help='filter messages by text pattern (case sensitive)', dest='pattern', type=str, metavar='PATTERN', required=False, default='')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    if args.name:
        dump_names(args.namelist)

    if args.phone:
        get_phone_numbers(args.namelist)

    if args.msg:
        dump_messages(args.namelist, args.pattern)

    if args.convers:
        dump_conversation(args.namelist, args.pattern)
