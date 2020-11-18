from uio         import Uio
from argsort_axi import ArgSort_AXI

if __name__ == '__main__':
    uio         = Uio('uio_argsort')
    argsort_axi = ArgSort_AXI(uio.regs())
    argsort_axi.print_info()
    argsort_axi.print_debug()
    
