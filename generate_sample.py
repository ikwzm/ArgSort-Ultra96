import numpy as np
import time
import argparse

def generate_sample_array(size, dtype):
    iinfo  = np.iinfo(dtype)
    return np.random.randint(iinfo.min, iinfo.max, (size)).astype(dtype)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Sample Numpy Array')
    parser.add_argument('-s', '--sample', help='sample file name', action='store', type=str, required=True)
    parser.add_argument('-n', '--size'  , help='array size'      , action='store', type=int, required=True)
    args   = parser.parse_args()

    start_time   = time.time()
    sample       = generate_sample_array(args.size, np.uint32)
    elapsed_time = time.time() - start_time

    np.save(args.sample, sample)
    
    print ("generate_sample: sample_file : {0}".format(args.sample))
    print ("generate_sample: size        : {0}".format(sample.size))
    print ("generate_sample: time        : {0}".format(round(elapsed_time*1000.0,3)) + " [msec]")
