import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    os.path.pardir))
DATA_DIR = os.path.join(BASE_DIR, 'data')
XML_PATH = os.path.join(BASE_DIR, 'data/SceneTrialTrain/locations.xml')
TEXT_PATH = os.path.join(BASE_DIR, 'data/word/')
SCENERY_PATH = os.path.join(BASE_DIR, 'data/SceneTrialTrain/')
PATCH_PATH = os.path.join(BASE_DIR, 'data/patches/')
WINDOW_PATH = os.path.join(BASE_DIR, 'data/windows/')
DICT_PATH = os.path.join(BASE_DIR, 'data/dict.npy')
CHARACTER_MODEL_PATH = os.path.join(BASE_DIR, 'data/character_model.pkl')
NUM_PATCHES_PER_TEXT = 30  # TODO this should be >100, for classification training purposes 30 atm
TEXT_MODEL_PATH = os.path.join(BASE_DIR, 'data/text_model.pkl')
TEST_IMAGE_PATH = os.path.join(BASE_DIR, 'data/test_images/')
TOTAL_WINDOWS_FOR_TRAINING = 10000
ALPHA = .5 #hyperparam from feature extraction #TODO tune this in crossval

NUM_D = 20  # number of dictionary entries
