from uio import Uio

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

    RW_MODE_AXI_CACHE   = (0xF <<  4)
    RW_MODE_AXI_PROT    = (0x2 <<  8)
    RW_MODE_AXI_ID_0    = (0x0 << 13)
    RW_MODE_AXI_ID_1    = (0x1 << 13)
    RW_MODE_SPECULATIVE = (0x1 << 14)
    
    MODE_IRQ_ENABLE     = 0x01

    CTRL_RESET          = 0x80
    CTRL_PAUSE          = 0x40
    CTRL_STOP           = 0x20
    CTRL_START          = 0x10
    CTRL_IRQ_ENABLE     = 0x04
    CTRL_FIRST          = 0x02
    CTRL_LAST           = 0x01

    def __init__(self, regs):
        self.regs    = regs
        self.rd_mode = 0x0000 | ArgSort_AXI.RW_MODE_AXI_CACHE | ArgSort_AXI.RW_MODE_AXI_PROT
        self.wr_mode = 0x0000 | ArgSort_AXI.RW_MODE_AXI_CACHE | ArgSort_AXI.RW_MODE_AXI_PROT
        self.t0_mode = 0x0000 | ArgSort_AXI.RW_MODE_AXI_ID_0
        self.t1_mode = 0x0000 | ArgSort_AXI.RW_MODE_AXI_ID_1
        self.read_info()

    def read_info(self):
        version_lo = self.regs.read_word(ArgSort_AXI.VERSION_REGS_ADDR+0)
        self.word_bits     = (version_lo >> 20) & 0xFFF
        self.index_bits    = (version_lo >>  8) & 0xFFF
        self.sort_order    = (version_lo >>  7) & 1
        self.comp_sign     = (version_lo >>  6) & 1
        version_hi = self.regs.read_word(ArgSort_AXI.VERSION_REGS_ADDR+4)
        self.version_major = (version_hi >> 28) & 0xF
        self.version_minor = (version_hi >> 24) & 0xF
        self.ways          = (version_hi >> 14) & 0x3FF
        self.words         = (version_hi >>  4) & 0x3FF
        self.stm_feedback  = (version_hi >>  0) & 0xF

    def print_info(self):
        print ("ArgSort_AXI Version     : {0}.{1}".format(self.version_major, self.version_minor))
        print ("ArgSort_AXI Ways        : {0}"    .format(self.ways))
        print ("ArgSort_AXI Words       : {0}"    .format(self.words))
        print ("ArgSort_AXI Feedback    : {0}"    .format(self.stm_feedback))
        print ("ArgSort_AXI WordBits    : {0}"    .format(self.word_bits ))
        print ("ArgSort_AXI IndexBits   : {0}"    .format(self.index_bits))
        print ("ArgSort_AXI Sort Order  : {0}"    .format(self.sort_order))
        print ("ArgSort_AXI Sign Compare: {0}"    .format(self.comp_sign ))
        
        
    def setup(self, src_addr, dst_addr, tmp0_addr, tmp1_addr, size):
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
        self.regs.write_word(ArgSort_AXI.MODE_REGS_ADDR     , ArgSort_AXI.MODE_IRQ_ENABLE)
    
    def start(self):
        ctrl = ArgSort_AXI.CTRL_START | ArgSort_AXI.CTRL_FIRST | ArgSort_AXI.CTRL_LAST | ArgSort_AXI.CTRL_IRQ_ENABLE
        self.regs.write_byte(ArgSort_AXI.CTRL_REGS_ADDR, ctrl)

    def clear_status(self):
        self.regs.write_byte(ArgSort_AXI.STAT_REGS_ADDR, 0x00)
        
    def reset(self):
        self.regs.write_byte(ArgSort_AXI.CTRL_REGS_ADDR, ArgSort_AXI.CTRL_RESET)
        self.regs.write_byte(ArgSort_AXI.CTRL_REGS_ADDR, 0)
        
