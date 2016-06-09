import ConfigParser
import os

def get_creds(section):

    config = ConfigParser.ConfigParser()
    config.read(os.path.dirname(os.path.realpath(__file__)) + '/../../credentials.ini')
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

