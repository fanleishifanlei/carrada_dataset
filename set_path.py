"""Script to set the path to CARRADA in the config.ini file"""
import sys
from utils.configurable import Configurable

if __name__ == '__main__':
    path_to_carrada = sys.argv[1]
    configurable = Configurable('config.ini')
    configurable.set('data', 'warehouse', path_to_carrada)
    with open('config.ini', 'w') as fp:
        configurable.config.write(fp)
