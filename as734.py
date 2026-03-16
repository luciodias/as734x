
class _as734x:
    from micropython import const
    import gc

    """
    Classe para controlar o módulo AS734x em Micropy.
    
    """
    ASTATUS = const(0x60)
    CH0_DATA = const(b'\x61\x62')
    ITIME = const(b'\x63\x64\x65')
    CH1_DATA = const(b'\x66\x67')
    CH2_DATA = const(b'\x68\x69')
    CH3_DATA = const(b'\x6A\x6B')
    CH4_DATA = const(b'\x6C\x6D')
    CH5_DATA = const(b'\x6E\x6F')
    CONFIG = const(0x70)
    STAT = const(0x71)
    EDGE = const(0x72)
    GPIO = const(0x73)
    LED = const(0x74)
    ENABLE = const(0x80)
    ATIME = const(0x81)
    WTIME = const(0x83)
    SP_TH_L = const(b'\x84\x85')
    SP_TH_H = const(b'\x86\x87')
    AUXID = const(0x90)
    REVID = const(0x91)
    ID = const(0x92)
    STATUS = const(0x93)
    ASTATUS_ = const(0x94)
    CH0_DATA_ = const(b'\x95\x96')
    CH1_DATA_ = const(b'\x97\x98')
    CH2_DATA_ = const(b'\x99\x9A')
    CH3_DATA_ = const(b'\x9B\x9C')
    CH4_DATA_ = const(b'\x9D\x9E')
    CH5_DATA_ = const(b'\x9F\xA0')
    STATUS_2 = const(0xA3)
    STATUS_3 = const(0xA4)
    STATUS_5 = const(0xA6)
    STATUS_6 = const(0xA7)
    CFG_0 = const(0xA9)
    CFG_1 = const(0xAA)
    CFG_3 = const(0xAC)
    CFG_6 = const(0xAF)
    CFG_8 = const(0xB1)
    CFG_9 = const(0xB2)
    CFG_10 = const(0xB3)
    CFG_12 = const(0xB5)
    PERS = const(0xBD)
    GPIO_2 = const(0xBE)
    ASTEP = const(b'\xCA\xCB')
    AGC_GAIN_MAX = const(0xCF)
    AZ_CONFIG = const(0xD6)
    FD_TIME_1 = const(0xD8)
    FD_TIME_2 = const(0xD4)
    FD_CFG0 = const(0xD7)
    FD_STATUS = const(0xDB)
    INTENAB = const(0xF9)
    CONTROL = const(0xFA)
    FIFO_MAP = const(0xFC)
    FIFO_LVL = const(0xFD)
    FDATA = const(b'\xFE\xFF')
    def __init__(self, i2c, address=0x39):
        self.i2c = i2c
        self.address = address
        gc.collect()

    def write_register(self, reg, data):
        if isinstance(reg, bytes):
            reg_addr = reg[0]
        else:
            reg_addr = reg
        if isinstance(data, int):
            data = bytearray([data])
        elif isinstance(data, bytes):
            data = bytearray(data)
        self.i2c.writeto_mem(self.address, reg_addr, data)
        gc.collect()

    def read_register(self, reg, length=1):
        if isinstance(reg, bytes):
            reg_addr = reg[0]
        else:
            reg_addr = reg
        data = self.i2c.readfrom_mem(self.address, reg_addr, length)
        gc.collect()
        return data

    def read_channel(self, channel_reg):
        if isinstance(channel_reg, bytes) and len(channel_reg) == 2:
            low = self.read_register(channel_reg[0])
            high = self.read_register(channel_reg[1])
            return int.from_bytes(low + high, 'little')
        else:
            return int.from_bytes(self.read_register(channel_reg, 2), 'little')

    def enable(self):
        self.write_register(self.ENABLE, 0x01)
        gc.collect()

    def disable(self):
        self.write_register(self.ENABLE, 0x00)
        gc.collect()

    def set_integration_time(self, time):
        self.write_register(self.ATIME, time)
        gc.collect()

    def set_wait_time(self, time):
        self.write_register(self.WTIME, time)
        gc.collect()

    def read_all_channels(self):
        channels = []
        for reg in [self.CH0_DATA, self.CH1_DATA, self.CH2_DATA, self.CH3_DATA, self.CH4_DATA, self.CH5_DATA]:
            channels.append(self.read_channel(reg))
        gc.collect()
        return channels