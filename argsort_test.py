from udmabuf     import Udmabuf
from uio         import Uio
from argsort_axi import ArgSort_AXI
import numpy as np
import time
import argparse

class ArgSort_Test:
    
    def __init__(self):
        self.uio          = Uio('uio_argsort')
        self.argsort_axi  = ArgSort_AXI(self.uio.regs())
        self.udmabuf_in   = Udmabuf('udmabuf-argsort-in' )
        self.udmabuf_out  = Udmabuf('udmabuf-argsort-out')
        self.udmabuf_tmp  = Udmabuf('udmabuf-argsort-tmp')
        self.in_dtype     = np.uint32
        self.out_dtype    = np.uint32
        self.tmp_dtype    = np.uint64
        self.in_max_size  = min((self.udmabuf_in .buf_size   ) // (np.dtype(self.in_dtype ).itemsize), self.argsort_axi.max_size)
        self.out_max_size = min((self.udmabuf_out.buf_size   ) // (np.dtype(self.out_dtype).itemsize), self.argsort_axi.max_size)
        self.tmp_max_size = min((self.udmabuf_tmp.buf_size//2) // (np.dtype(self.tmp_dtype).itemsize), self.argsort_axi.max_size)
        self.debug_mode   = 0

    def memmap_in(self, size):
        if (size > self.in_max_size):
            raise ValueError('size({0}) is over size of in-buffer({1})' .format(size,self.in_max_size ))
        return self.udmabuf_in .memmap(dtype=self.in_dtype , shape=(size))

    def memmap_out(self, size):
        if (size > self.out_max_size):
            raise ValueError('size({0}) is over size of out-buffer({1})'.format(size,self.out_max_size))
        return self.udmabuf_out.memmap(dtype=self.out_dtype, shape=(size))

    def allocate_array(self, size):
        if (size > self.tmp_max_size):
            raise ValueError('size({0}) is over size of tmp-buffer({1})'.format(size,self.tmp_max_size))
        self.in_array   = self.memmap_in(size)
        self.out_array  = self.memmap_out(size)
        
    def run(self):
        start = time.time()
        self.argsort_axi.setup(self.udmabuf_in .phys_addr ,
                               self.udmabuf_out.phys_addr,
                               self.udmabuf_tmp.phys_addr + 0x00000000,
                               self.udmabuf_tmp.phys_addr + self.udmabuf_tmp.buf_size//2,
                               self.in_array.size,
                               self.debug_mode
        )
        self.uio.irq_on()
        self.argsort_axi.start()
        self.uio.wait_irq()
        self.argsort_axi.clear_status()
        self.run_time = time.time() - start



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test Bench for ArgSort_AXI')
    parser.add_argument('-s', '--sample', help='sample file name', action='store', type=str, required=True)
    parser.add_argument('-r', '--result', help='result file name', action='store', type=str, required=True)
    parser.add_argument('-l', '--log'   , help='log file name'   , action='store', type=str, default="")
    parser.add_argument('-n', '--number', help='number of loops ', action='store', type=int, default=1)
    parser.add_argument('-d', '--debug' , help='debug mode '     , action='store', type=int, default=0)

    args   = parser.parse_args()
    test   = ArgSort_Test()

    test.argsort_axi.print_info("argsort_test   :")

    print ("argsort_test   : sample_file  : {0}".format(args.sample))
    sample = np.load(args.sample)
    print ("argsort_test   : size         : {0}".format(sample.size))

    test.allocate_array(sample.size)
    test.in_array[:] = sample
    
    total_time = 0
    total_size = 0
    count      = 0

    print ("argsort_test   : debug_mode   : {0}".format(args.debug))
    test.debug_mode = args.debug

    print ("argsort_test   : loops        : {0}".format(args.number))

    for i in range (0,args.number):
        test.run()
        total_time   = total_time  + test.run_time
        total_size   = total_size  + sample.size
        count        = count       + 1
        print ("argsort_test   : time         : {0:>8.3f} # [msec]".format(round(test.run_time*1000.0,3)))

    print ("argsort_test   : result_file  : {0}".format(args.result))
    np.save(args.result, test.out_array)
        
    average_time = round((total_time/count)*1000.0            ,3)
    throughput   = round(((total_size/total_time)/(1000*1000)),3)

    print ("argsort_test   : average_time : {0:>8.3f} # [msec]"      .format(average_time))
    print ("argsort_test   : throughput   : {0:>8.3f} # [mwords/sec]".format(throughput  ))

    test.argsort_axi.print_debug("argsort_test   :")

    if args.log != '':
        with open(args.log, mode='a') as f:
            print ("-", file=f)
            test.argsort_axi.print_info("  ", file=f)
            print ("   size         : {0}".format(sample.size), file=f)
            print ("   average_time : {0:>8.3f} # [msec]"      .format(average_time), file=f)
            print ("   throughput   : {0:>8.3f} # [mwords/sec]".format(throughput  ), file=f)
            test.argsort_axi.print_debug("  ", file=f)
            
