import numpy as np
import time
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Expect Numpy Array')
    parser.add_argument('-s', '--sample', help='sample file name', action='store', type=str, required=True)
    parser.add_argument('-e', '--expect', help='expect file name', action='store', type=str, required=True)
    parser.add_argument('-l', '--log'   , help='log file name'   , action='store', type=str, default="")

    args   = parser.parse_args()

    print ("generate_expect: sample_file  : {0}".format(args.sample))
    print ("generate_expect: expect_file  : {0}".format(args.expect))

    sample = np.load(args.sample)

    print ("generate_expect: size         : {0}".format(sample.size))
    
    start_time   = time.time()
    expect       = np.argsort(sample).astype(np.uint32)
    elapsed_time = time.time() - start_time

    np.save(args.expect, expect)
    
    average_time = round(elapsed_time*1000.0,3)
    throughput   = round(((sample.size/elapsed_time)/(1000*1000)),3)

    print ("generate_expect: average_time : {0:>8.3f} # [msec]"      .format(average_time))
    print ("generate_expect: throughput   : {0:>8.3f} # [mwords/sec]".format(throughput  ))

    if args.log != '':
        with open(args.log, mode='a') as f:
            print ("-", file=f)
            print ("   sample_file  : {0}".format(args.sample), file=f)
            print ("   expect_file  : {0}".format(args.expect), file=f)
            print ("   size         : {0}".format(sample.size), file=f)
            print ("   average_time : {0:>8.3f} # [msec]"      .format(average_time), file=f)
            print ("   throughput   : {0:>8.3f} # [mwords/sec]".format(throughput  ), file=f)
            
