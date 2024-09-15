class piPicoW:
    def __init__(self, rst_pin, cs_pin, dc_pin, busy_pin):
        self.RST_PIN = rst_pin
        self.DC_PIN = dc_pin
        self.CS_PIN = cs_pin
        self.BUSY_PIN = busy_pin