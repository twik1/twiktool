from pypykatz.dpapi.dpapi import DPAPI
from pypykatz.dpapi.structures.blob import DPAPI_BLOB

import sqlite3
import hashlib, os
import sys
import argparse
import binascii

class HTMLout:
    def __init__(self):
        self.outstring_top = "<!doctype html>\n" \
                        "<html lang=\"en\">\n" \
                        "\t<head>\n" \
                        "\t\t<meta charset=\"utf-8\">\n" \
                        "\t\t<title>Unchrome</title>\n" \
                        "\t\t<meta name=\"twik\" version=\"1.0\">\n" \
                        "\t</head>\n" \
                        "\t<body>\n" \
                        "\t\t<table>\n" \
                        "\t\t\t<tr><th>origin_url</th><th>action_url</th><th>username_element</th>" \
                        "<th>username_value</th><th>password_element</th><th>password_value</th>" \
                        "<th>date_created</th><tr>\n"
        self.outstring_bot = "\t\t</table>\n" \
                        "\t</body>\n" \
                        "</html>\n"
        self.rows = []

    def add_row(self, ourl, aurl, uelem, uvalue, pelem, pvalue, dcreate, color):
        self.rows.append("\t\t\t<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td>"
                         "<td>{}</td><td><font color={}>{}</font></td><td>{}></td></tr>".format(ourl, aurl,
                                                                                                uelem, uvalue,pelem,
                                                                                                color, pvalue, dcreate))
    def output(self):
        return self.outstring_top + "".join(self.rows) + self.outstring_bot


def run_unchrome(sid, password, masterkeydir, chromedb, out):
    status = {'result': 0, 'mkfile': 0, 'decoded': 0, 'notdecoded': 0}
    phash = hashlib.sha1(password.encode("UTF-16LE")).hexdigest()
    phash = phash.encode("utf-8").hex()
    dpapi = DPAPI()
    dpapi.get_prekeys_from_password(sid, password, phash)
    #todo dpapi.get_prekeys_form_registry_files()
    htmlout = HTMLout()

    dirlist = os.listdir(masterkeydir)
    for file in dirlist:
        try:
            result = dpapi.decrypt_masterkey_file(os.path.join(masterkeydir, file))
            if not len(result[0]) and not len(result[1]):
                continue
            else:
                status['mkfile'] += 1
        except:
            continue

    if not len(dpapi.masterkeys):
        status = {'result': 1}
        return status

    #if options.credhist != None:
    #    mkp.addCredhistFile(options.sid, options.credhist)

    fields = [ 'origin_url', 'action_url', 'username_element',
               'username_value', 'password_element', 'password_value',
               'date_created' ]

    db = chromedb
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT %s FROM logins" % ",".join(fields))
    for row in c:
        w = {}
        for f in fields:
            w[f] = row[f]
        blob = DPAPI_BLOB.from_bytes(w["password_value"])
        w['color'] = 'red'
        status['notdecode'] += 1
        for key in dpapi.masterkeys.keys():
            if blob.masterkey_guid == key:
                w['password_value'] = dpapi.decrypt_blob(blob, dpapi.masterkeys[key]).decode('UTF-8')
                w['color'] = 'green'
                status['decode'] += 1
                status['notdecode'] -= 1
        htmlout.add_row(w['origin_url'], w['action_url'], w['username_element'], w['username_value'],
                        w['password_element'], w['password_value'], w['date_created'], w['color'])
    c.close()
    conn.close()

    try:
        f = open(out, 'w')
        f.write(htmlout.output())
        f.close()
    except OSError:
        status['result'] = 2  # Unable to save
    return status


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='unchrome v1.0')
    parser.add_argument('-s', '--sid', help='SID', required=True)
    parser.add_argument('-m', '--masterkey', help='Masterkey dir', required=True)
    parser.add_argument('-p', '--password', help='User password', required=True)
    parser.add_argument('-c', '--chromedb', help='Crhome password file', required=True)
    parser.add_argument('-o', '--output', help='Decoded Chrome file', required=True)
    args = parser.parse_args()

    run_unchrome(args.sid, args.password, args.masterkeydir, args.chromedb, args.output)

