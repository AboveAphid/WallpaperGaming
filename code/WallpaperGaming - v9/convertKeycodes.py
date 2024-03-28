# Created by A_Aphid

import keyCodes

def convertToVk_key(keyName):
    vk_keys = keyCodes.vk_codes
    mainRematched = keyCodes.reorganisedMainGamingKeysNameToVKKEY

    if keyName in vk_keys:
        return keyName

    if keyName in mainRematched:
        return mainRematched[keyName]

    return None # If no key found
    