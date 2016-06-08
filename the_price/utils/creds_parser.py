import ConfigParser
import os

def get_creds(search_engine):

    config = ConfigParser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__)) + '/../../credentials.ini')
    dict1 = {}
    options = config.options(search_engine)
    for option in options:
        try:
            dict1[option] = config.get(search_engine, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

