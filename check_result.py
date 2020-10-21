import numpy as np
import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Sample Numpy Array')
    parser.add_argument('-s', '--sample', help='sample file name', action='store', type=str, required=True)
    parser.add_argument('-e', '--expect', help='expect file name', action='store', type=str, required=True)
    parser.add_argument('-r', '--result', help='result file name', action='store', type=str, required=True)
    args   = parser.parse_args()

    print ("check_result: sample file : {0}".format(args.sample))
    sample = np.load(args.sample )

    print ("check_result: expect file : {0}".format(args.expect))
    expect = np.load(args.expect)

    print ("check_result: result file : {0}".format(args.result))
    result = np.load(args.result )

    mismatch_list = []
    if ((expect == result).all() == False):
        diff_index_array = np.where((expect == result) == 0)[0]
        for i in diff_index_array:
            if (sample[result[i]] != sample[expect[i]]):
                mismatch_list.append(i)

    if (len(mismatch_list) > 0):
        print('check_result: NG mismatch count = {0}'.format(len(mismatch_list)))
        sys.exit(-1)
    else:
        print('check_result: OK')
        sys.exit(0)
        
