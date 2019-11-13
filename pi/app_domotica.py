from sense_hat import SenseHat
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from time import sleep

cred = credentials.Certificate("./certificate.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

config_ref = db.collection(u'smartHomeConfig').document(u'config1')
burglary_ref = db.collection(u'smartHomeConfig').document(u'burglary')
sensors_ref = db.collection(u'smartHomeConfig').document(u'sensors')


try:
    config_stream = config_ref.get().to_dict()
    burglary_stream = burglary_ref.get().to_dict()
    sensors_stream = sensors_ref.get().to_dict()
except google.cloud.exceptions.NotFound:
    print(u'No such document!')
    
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        getDataFromFireStore(doc.id)

config_watch = config_ref.on_snapshot(on_snapshot)
burglary_watch = burglary_ref.on_snapshot(on_snapshot)

def getDataFromFireStore(document):
    if document == 'config1':
        try:
            global config_stream
            config_stream = config_ref.get().to_dict()
        except google.cloud.exceptions.NotFound:
            print(u'No such document!')
    elif document == 'burglary' :
        try:
            global burglary_stream
            burglary_stream = burglary_ref.get().to_dict()
        except google.cloud.exceptions.NotFound:
            print(u'No such document!')

yellow = (255,255,0)
darkYellow = (75,75,0)
blue = (0,0,255)
darkBlue = (0,0,75)
red = (255,0,0)
green = (0,255,0)

mapColors = {
    "backdoor": {
        'active': green,
        'disabled': red
        },
    "frontdoor": {
        'active': green,
        'disabled': red
        },
    "outlet1": {
        'active': blue,
        'disabled': darkBlue
        },
    "outlet2": {
        'active': blue,
        'disabled': darkBlue
        },
    "outlet3": {
        'active': blue,
        'disabled': darkBlue
        },
    "outlet4": {
        'active': blue,
        'disabled': darkBlue
        },
    "light1": {
        'active': yellow,
        'disabled': darkYellow
        },
    "light2": {
        'active': yellow,
        'disabled': darkYellow
        },
    "light3": {
        'active': yellow,
        'disabled': darkYellow
        },
    "light4": {
        'active': yellow,
        'disabled': darkYellow
        },
    }

mapPixels = {
    "backdoor": [
        [0,7],
        [1,7],
        [2,7],
        ],
    "frontdoor": [
        [0,0],
        [1,0],
        [2,0],
        ],
    "outlet1": [
        [4,0],
        ],
    "outlet2": [
        [0,3],
        ],
    "outlet3": [
        [0,4],
        ],
    "outlet4": [
        [4,7],
        ],
    "light1": [
        [3,2],
        ],
    "light2": [
        [3,5],
        ],
    "light3": [
        [7,2],
        ],
    "light4": [
        [7,5],
        ]
    }

sense = SenseHat()
sense.clear()

def setColor(name, isActive):
    if isActive:
        return mapColors[name]['active']
    else:
        return mapColors[name]['disabled']

def setPixels(name, color):
    for key in mapPixels[name]:
        sense.set_pixel(key[0], key[1], color)


def breakIn():
    sense.clear()
    for x in range(1000):
        setPixels('backdoor', green)
        setPixels('frontdoor', green)
        setPixels('light1', yellow)
        setPixels('light2', yellow)
        setPixels('light3', yellow)
        setPixels('light4', yellow)
        sleep(0.1)
        sense.clear()
        sleep(0.1)
        if not burglary_stream['isRobbery']:
            break

def loop():
    sense.clear()
    for key in burglary_stream:
        if burglary_stream[key]:
            breakIn()
        else:
            for key in config_stream:
                isActive = config_stream[key]
                setPixels(key, setColor(key,isActive))

def getSensorData():
    temperature = int(sense.get_temperature())
    humidity = int(sense.get_humidity())
    # reduce number of calls to fireStore
    isSameData = sensors_stream['temperature'] == temperature or sensors_stream['humidity'] == humidity
    if not isSameData:
        sensors_ref.set({
            u"temperature": temperature,
            u"humidity": humidity
            })
        global sensors_stream
        sensors_stream = sensors_ref.get().to_dict()
        

# normally this will go on indefinetly but to reduce to number of calls i set this to 100 seconds
for i in range(1000):
    loop()
    sleep(0.1)
    if i % 10 == 0:
        getSensorData()
