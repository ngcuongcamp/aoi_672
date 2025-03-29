import json



# path dirs
PATH_CONFIG = './data/configs/config.json'
PATH_ICON = './data/icons/Logo.ico'
TITLE_PROGRAM = 'AOI FT672'
PATH_TEMPLATE = './data/temp/2temp_black.png'

# colors & rectangle properties 
GREEN_COLOR = (0, 255, 0)
RED_COLOR = (0,0,255)
WHITE_COLOR = (255,255,255)
BLACK_COLOR = (0,0,0)
PINK_COLOR = (255, 0, 255)
ORANGE_COLOR = (0, 165, 255)
YELLOW_COLOR = (0, 255, 255)
PURPLE_COLOR = (255, 0, 128)

def load_config(): 
        """Load config from file"""
        try:
            with open(PATH_CONFIG, 'r') as f:
                return json.load(f)
        except Exception as E: 
            print(f'Error when load config: {E}')