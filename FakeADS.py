class fake_adc:
    def read_adc(self, channel, gain):
        return 100000

def ADS1115():
    return fake_adc()
