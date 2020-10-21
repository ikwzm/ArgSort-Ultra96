import numpy as np
import time
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Expect Numpy Array')
    parser.add_argument('-s', '--sample', help='sample file name', action='store', type=str, required=True)
    parser.add_argument('-e', '--expect', help='expect file name', action='store', type=str, required=True)
    args   = parser.parse_args()

    print ("generate_expect: sample_file : {0}".format(args.sample))
    print ("generate_expect: expect_file : {0}".format(args.expect))

    sample = np.load(args.sample)

    print ("generate_expect: size        : {0}".format(sample.size))
    
    start_time   = time.time()
    expect       = np.argsort(sample).astype(np.uint32)
    elapsed_time = time.time() - start_time

    np.save(args.expect, expect)
    
    print ("generate_expect: time        : {0}".format(round(elapsed_time*1000.0,3)) + " [msec]")
    print ("generate_expect: throughput  : {0}".format(round(((sample.size/elapsed_time)/(1000*1000)),3)) + "[Mwords/sec]")
