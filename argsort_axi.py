from uio import Uio
import sys

class ArgSort_AXI:

    VERSION_REGS_ADDR   = 0x0000
    RD_ADDR_REGS_ADDR   = 0x0008
    WR_ADDR_REGS_ADDR   = 0x0010
    T0_ADDR_REGS_ADDR   = 0x0018
    T1_ADDR_REGS_ADDR   = 0x0020
    RD_MODE_REGS_ADDR   = 0x0028
    WR_MODE_REGS_ADDR   = 0x002C
    T0_MODE_REGS_ADDR   = 0x0030
    T1_MODE_REGS_ADDR   = 0x0034
    SIZE_REGS_ADDR      = 0x0038
    MODE_REGS_ADDR      = 0x003C
    STAT_REGS_ADDR      = 0x003E
    CTRL_REGS_ADDR      = 0x003F
    DEBUG_REGS_ADDR     = 0x0040

    RW_MODE_AXI_CACHE   = (0xF <<  4)
    RW_MODE_AXI_PROT    = (0x2 <<  8)
    RW_MODE_AXI_ID_0    = (0x0 << 13)
    RW_MODE_AXI_ID_1    = (0x1 << 13)
    RW_MODE_SPECULATIVE = (0x1 << 14)
    
    MODE_IRQ_ENABLE     = (0x1 <<  0)
    MODE_DEBUG_0        = (0x0 << 12)
    MODE_DEBUG_1        = (0x1 << 12)
    MODE_DEBUG_2        = (0x2 << 12)

    CTRL_RESET          = 0x80
    CTRL_PAUSE          = 0x40
    CTRL_STOP           = 0x20
    CTRL_START          = 0x10
    CTRL_IRQ_ENABLE     = 0x04
    CTRL_FIRST          = 0x02
    CTRL_LAST           = 0x01

    FCLK0_RATE_FILE     = "/sys/class/fclkcfg/amba_pl@0:fclk0/rate"
    
    def __init__(self, regs):
        self.regs    = regs
        self.rd_mode = 0x0000 | ArgSort_AXI.RW_MODE_AXI_CACHE | ArgSort_AXI.RW_MODE_AXI_PROT
        self.wr_mode = 0x0000 | ArgSort_AXI.RW_MODE_AXI_CACHE | ArgSort_AXI.RW_MODE_AXI_PROT
        self.t0_mode = 0x0000 | ArgSort_AXI.RW_MODE_AXI_ID_0
        self.t1_mode = 0x0000 | ArgSort_AXI.RW_MODE_AXI_ID_1
        self.read_info()
        self.read_frequency()

    def read_info(self):
        version_lo = self.regs.read_word(ArgSort_AXI.VERSION_REGS_ADDR+0)
        self.word_bits     = (version_lo >> 20) & 0xFFF
        self.index_bits    = (version_lo >>  8) & 0xFFF
        self.sort_order    = (version_lo >>  7) & 1
        self.comp_sign     = (version_lo >>  6) & 1
        self.debug_enable  = (version_lo >>  5) & 1
        version_hi = self.regs.read_word(ArgSort_AXI.VERSION_REGS_ADDR+4)
        self.version_major = (version_hi >> 28) & 0xF
        self.version_minor = (version_hi >> 24) & 0xF
        self.ways          = (version_hi >> 14) & 0x3FF
        self.words         = (version_hi >>  4) & 0x3FF
        self.stm_feedback  = (version_hi >>  0) & 0xF
        self.regs.write_word(ArgSort_AXI.SIZE_REGS_ADDR, 0xFFFFFFFF)
        self.max_size      = self.regs.read_word(ArgSort_AXI.SIZE_REGS_ADDR)

    def print_info(self, tag="ArgSort_AXI", file=sys.stdout):
        print ("{0} Version      : {1}.{2}".format(tag, self.version_major, self.version_minor),file=file)
        print ("{0} Ways         : {1}"    .format(tag, self.ways        ), file=file)
        print ("{0} Words        : {1}"    .format(tag, self.words       ), file=file)
        print ("{0} Feedback     : {1}"    .format(tag, self.stm_feedback), file=file)
        print ("{0} WordBits     : {1}"    .format(tag, self.word_bits   ), file=file)
        print ("{0} IndexBits    : {1}"    .format(tag, self.index_bits  ), file=file)
        print ("{0} Sort Order   : {1}"    .format(tag, self.sort_order  ), file=file)
        print ("{0} Sign Compare : {1}"    .format(tag, self.comp_sign   ) ,file=file)
        print ("{0} Max Size     : {1}"    .format(tag, self.max_size    ), file=file)
        print ("{0} Debug Enable : {1}"    .format(tag, self.debug_enable), file=file)

    def read_frequency(self):
        file = open(ArgSort_AXI.FCLK0_RATE_FILE)
        self.frequency = int(file.read())
        file.close()

    def read_debug_time(self):
        time_array = []
        if (self.debug_enable == 1):
            debug_mode = (self.regs.read_word(ArgSort_AXI.MODE_REGS_ADDR) >> 12) & 0xF
            if (debug_mode == 2):
                for i in range(0,7):
                    l = self.regs.read_word(ArgSort_AXI.DEBUG_REGS_ADDR + i*8  )
                    h = self.regs.read_word(ArgSort_AXI.DEBUG_REGS_ADDR + i*8+4)
                    v = (h << 32) | l
                    if (v > 0): 
                        time = v/self.frequency
                        time_array.append(time)
        return time_array

    def read_debug_size(self):
        size_array = []
        if (self.debug_enable == 1):
            debug_mode = (self.regs.read_word(ArgSort_AXI.MODE_REGS_ADDR) >> 12) & 0xF
            if (debug_mode == 1):
                for i in range(0,7):
                    l = self.regs.read_word(ArgSort_AXI.DEBUG_REGS_ADDR + i*8  )
                    h = self.regs.read_word(ArgSort_AXI.DEBUG_REGS_ADDR + i*8+4)
                    blk  = l
                    last = (h >> 31) & 1
                    if (blk > 0):
                        size_array.append({'block_size': blk, 'last' : last})
        return size_array
        
    def print_debug(self, tag="ArgSort_AXI", file=sys.stdout):
        time_array = self.read_debug_time()
        for i, time in enumerate(time_array):
            print ("{0} Debug_Time({1:1d}): {2:>8.3f} # [msec]".format(tag, i, round(time*1000.0,3)), file=file)
        size_array = self.read_debug_size()
        for i, dict in enumerate(size_array):
            print ("{0} Debug_Size({1:1d}): [{2},{3}]".format(tag, i, dict['block_size'], dict['last']), file=file)
        
    def setup(self, src_addr, dst_addr, tmp0_addr, tmp1_addr, size, debug_mode = 0):
        self.regs.write_word(ArgSort_AXI.RD_ADDR_REGS_ADDR+0, (src_addr  >>  0) & 0xFFFFFFFF)
        self.regs.write_word(ArgSort_AXI.RD_ADDR_REGS_ADDR+4, (src_addr  >> 32) & 0xFFFFFFFF)
        self.regs.write_word(ArgSort_AXI.WR_ADDR_REGS_ADDR+0, (dst_addr  >>  0) & 0xFFFFFFFF)
        self.regs.write_word(ArgSort_AXI.WR_ADDR_REGS_ADDR+4, (dst_addr  >> 32) & 0xFFFFFFFF)
        self.regs.write_word(ArgSort_AXI.T0_ADDR_REGS_ADDR+0, (tmp0_addr >>  0) & 0xFFFFFFFF)
        self.regs.write_word(ArgSort_AXI.T0_ADDR_REGS_ADDR+4, (tmp0_addr >> 32) & 0xFFFFFFFF)
        self.regs.write_word(ArgSort_AXI.T1_ADDR_REGS_ADDR+0, (tmp1_addr >>  0) & 0xFFFFFFFF)
        self.regs.write_word(ArgSort_AXI.T1_ADDR_REGS_ADDR+4, (tmp1_addr >> 32) & 0xFFFFFFFF)
        self.regs.write_word(ArgSort_AXI.RD_MODE_REGS_ADDR  , self.rd_mode)
        self.regs.write_word(ArgSort_AXI.WR_MODE_REGS_ADDR  , self.wr_mode)
        self.regs.write_word(ArgSort_AXI.T0_MODE_REGS_ADDR  , self.t0_mode)
        self.regs.write_word(ArgSort_AXI.T1_MODE_REGS_ADDR  , self.t1_mode)
        self.regs.write_word(ArgSort_AXI.SIZE_REGS_ADDR     , size)
        if   debug_mode == 2:
            mode = ArgSort_AXI.MODE_DEBUG_2
        elif debug_mode == 1:
            mode = ArgSort_AXI.MODE_DEBUG_1
        else:
            mode = ArgSort_AXI.MODE_DEBUG_0
        mode = mode | ArgSort_AXI.MODE_IRQ_ENABLE
        self.regs.write_word(ArgSort_AXI.MODE_REGS_ADDR     , mode)
    
    def start(self):
        ctrl = ArgSort_AXI.CTRL_START | ArgSort_AXI.CTRL_FIRST | ArgSort_AXI.CTRL_LAST | ArgSort_AXI.CTRL_IRQ_ENABLE
        self.regs.write_byte(ArgSort_AXI.CTRL_REGS_ADDR, ctrl)

    def clear_status(self):
        self.regs.write_byte(ArgSort_AXI.STAT_REGS_ADDR, 0x00)
        
    def reset(self):
        self.regs.write_byte(ArgSort_AXI.CTRL_REGS_ADDR, ArgSort_AXI.CTRL_RESET)
        self.regs.write_byte(ArgSort_AXI.CTRL_REGS_ADDR, 0)
        
