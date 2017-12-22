#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import click
import requests
import sys

ID = ""
Token = ""
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}

@click.command()
@click.option('-o', '--operation', help='API to excute.',
              type=click.Choice(['dmlist', 'rdlist', 'disable', 'enable', 'query']), required=True)
@click.option('-d', '--domain', help='Full domain name.')
@click.option('-r', '--recordid', help='Full record ID.')
@click.option('-l', '--line', help='Full line name.')
def excute(operation, domain, recordid, line):
    if operation == "dmlist":
        print('ID                            Domain Name')
        for id, name in get_domain_list():
            print("{:<10} {}".format(id, name))
    elif operation == "rdlist":
        domain_id = get_domain_id(domain)
        print("ID         Line    Record     Value")
        for id, name, line, value in get_record_list(domain_id):
            print("{:<10} {:<6} {:<10} {:<20}".format(id, line, name, value))
    elif operation == "disable":
        domain_id = get_domain_id(domain)
        r = disable_record(domain_id, recordid)
        print(r['status']['message'])
        if r['status']['code'] != '1':
            sys.exit(1)
    elif operation == "enable":
        domain_id = get_domain_id(domain)
        r = enable_record(domain_id, recordid)
        print(r['status']['message'])
        if r['status']['code'] != '1':
            sys.exit(1)
    elif operation == "query":
        domain_id = get_domain_id(domain)
        r = query_status(domain_id, recordid)
        print(r['status']['message'])
        if r['status']['code'] != '1':
            sys.exit(1)
        else:
            if r['record']['enabled'] == '1':
                print('{}.{}(id:{}) is enabled.'.format(r['record']['sub_domain'], domain, recordid))
            else:
                print('{}.{}(id:{}) is disabled.'.format(r['record']['sub_domain'], domain, recordid))

def api_request(url, data):
    r = requests.post(url, headers=headers, data=data)
    r = r.json()
    return r

def get_domain_list():
    r = api_request('https://dnsapi.cn/Domain.List', "login_token={},{}&format=json".format(ID, Token))
    for d in r["domains"]:
        yield d["id"], d["name"]

def get_domain_id(domain):
    domain_id = api_request('https://dnsapi.cn/Domain.List', "login_token={},{}&format=json&keyword={}".format(ID, Token, domain))["domains"][0]["id"]
    return domain_id

def get_record_list(domain_id):
    r = api_request('https://dnsapi.cn/Record.List', "login_token={},{}&format=json&domain_id={}".format(ID, Token, domain_id))
    for d in r["records"]:
        yield d["id"], d["name"], d["line"], d["value"]

def disable_record(domain_id, record_id):
    r = api_request('https://dnsapi.cn/Record.Status', "login_token={},{}&format=json&domain_id={}&record_id={}&status=disable".format(ID, Token, domain_id, record_id))
    return r

def enable_record(domain_id, recordid):
    r = api_request('https://dnsapi.cn/Record.Status', "login_token={},{}&format=json&domain_id={}&record_id={}&status=enable".format(ID, Token, domain_id, recordid))
    return r

def query_status(domain_id, recordid):
    r = api_request('https://dnsapi.cn/Record.Info', "login_token={},{}&format=json&domain_id={}&record_id={}".format(ID, Token, domain_id, recordid))
    return r


excute()
