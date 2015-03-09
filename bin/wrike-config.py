#!/usr/bin/env python
import argparse
from wrike.client import WrikeAPI
from wrike.storage import FileStorage


parser = argparse.ArgumentParser(description='Prepare a configuration file for python-wrike.')
parser.add_argument('--client-id',
                    dest='client_id',
                    action='store',
                    help='Wrike API client id',
                    required=True)
parser.add_argument('--client-secret',
                    dest='client_secret',
                    action='store',
                    help='Wrike API client secret',
                    required=True)
parser.add_argument('--code',
                    dest='code',
                    action='store',
                    help='Wrike API code')
parser.add_argument('--output',
                    dest='output',
                    action='store',
                    help='A configuration file path')

args = parser.parse_args()
args_api = {
    "client_id": args.client_id,
    "client_secret": args.client_secret,
}

if args.code:
    args_api["code"] = args.code

if args.output:
    args_api["storage"] = FileStorage(args.output)

api = WrikeAPI(**args_api)

if args.code is None:
    print "Go to the following link in your browser:"
    print api.authorize_url
    print
else:
    print args.output
    print "Done."
