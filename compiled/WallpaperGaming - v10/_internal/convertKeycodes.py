# Created by A_Aphid

import keyCodes

def convertToVk_key(keyName:str) -> None | str:
    """
    Takes in keyname (from keyboard library) and then changes it to vk_key code.
    """
    vk_keys = keyCodes.vk_codes
    mainRematched = keyCodes.reorganisedMainGamingKeysNameToVKKEY

    if keyName in vk_keys:
        return keyName

    if keyName in mainRematched:
        return mainRematched[keyName]

    return None # If no key found
    