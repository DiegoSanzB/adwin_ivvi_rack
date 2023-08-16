import logging

import ADwin

def boot(device_number, raise_exceptions, adwin_processor_type):
    adw = ADwin.ADwin(device_number, raise_exceptions)

    adw.Boot(adw.ADwindir + "ADwin" + str(adwin_processor_type) + ".btl")

    # Test Version
    if adw.Test_Version() == 0:
        print("ok")
    else:
        print("Boot failed")

    return adw
    


if __name__ == '__main__':
    boot()
