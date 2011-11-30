#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyparsing import *
from base64 import b64decode

class OTRPrivateKeys():

    @staticmethod
    def verifyLen(t):
        t = t[0]
        if t.len is not None:
            t1len = len(t[1])
            if t1len != t.len:
                raise ParseFatalException, \
                        "invalid data of length %d, expected %s" % (t1len, t.len)
        return t[1]

    @staticmethod
    def parse_sexp(data):
        '''parse sexp/S-expression format and return a python list'''
        # define punctuation literals
        LPAR, RPAR, LBRK, RBRK, LBRC, RBRC, VBAR = map(Suppress, "()[]{}|")

        decimal = Word("123456789",nums).setParseAction(lambda t: int(t[0]))
        bytes = Word(printables)
        raw = Group(decimal.setResultsName("len") + Suppress(":") + bytes).setParseAction(OTRPrivateKeys.verifyLen)
        token = Word(alphanums + "-./_:*+=")
        base64_ = Group(Optional(decimal,default=None).setResultsName("len") + VBAR 
            + OneOrMore(Word( alphanums +"+/=" )).setParseAction(lambda t: b64decode("".join(t)))
            + VBAR).setParseAction(OTRPrivateKeys.verifyLen)

        hexadecimal = ("#" + OneOrMore(Word(hexnums)) + "#")\
                        .setParseAction(lambda t: int("".join(t[1:-1]),16))
        qString = Group(Optional(decimal,default=None).setResultsName("len") + 
                                dblQuotedString.setParseAction(removeQuotes)).setParseAction(OTRPrivateKeys.verifyLen)
        simpleString = raw | token | base64_ | hexadecimal | qString

        display = LBRK + simpleString + RBRK
        string_ = Optional(display) + simpleString

        sexp = Forward()
        sexpList = Group(LPAR + ZeroOrMore(sexp) + RPAR)
        sexp << ( string_ | sexpList )

        try:
            sexpr = sexp.parseString(data)
            return sexpr.asList()[0][1:]
        except ParseFatalException, pfe:
            print "Error:", pfe.msg
            print line(pfe.loc,t)
            print pfe.markInputline()

    @staticmethod
    def parse(data):
        '''parse the otr.private_key S-Expression and return an OTR dict'''

        keys = []
        sexplist = OTRPrivateKeys.parse_sexp(data)
        for key in sexplist:
            if key[0] == "account":
                keydict = {}
                for element in key:
                    if element[0] == "name":
                        name, resource = element[1].split('/')
                        keydict['name'] = name
                        keydict['resource'] = resource
                    elif element[0] == "protocol":
                        keydict['protocol'] = element[1]
                    elif element[0] == "private-key":
                        if element[1][0] == 'dsa':
                            keydict['type'] = 'dsa';
                            for num in element[1][1:6]:
                                keydict[num[0]] = num[1]
                keys.append(keydict)
        return keys


if __name__ == "__main__":
    import sys
    import pprint

    pp = pprint.PrettyPrinter(indent=4)

    f = open(sys.argv[1], 'r')
    testotr = ""
    for line in f.readlines():
        testotr += line
    pp.pprint(OTRPrivateKeys.parse(testotr))
