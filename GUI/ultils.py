import json

PATH_CONFIG = './data/configs/config.json'
PATH_ICON = './data/icons/Logo.ico'
TITLE_PROGRAM = 'AOI FT672'

def load_config(): 
        """Load config from file"""
        try:
            with open(PATH_CONFIG, 'r') as f:
                return json.load(f)
        except Exception as E: 
            print(f'Error when load config: {E}')