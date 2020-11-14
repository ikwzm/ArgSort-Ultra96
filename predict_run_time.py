from uio         import Uio
from argsort_axi import ArgSort_AXI
import numpy as np
import argparse

def calc_transaction(size,ways,words,feedback):
    transactions = [{'block_size': 1, 'block_number': size}]
    block_size   = words*(ways**(feedback+1))
    block_number = (size + block_size - 1) // block_size
    transactions.append({'block_size': block_size, 'block_number': block_number})
    while (transactions[-1]['block_number'] > 1):
        next_block_size   = transactions[-1]['block_size'] * ways
        next_block_number = (size + next_block_size - 1) // next_block_size
        next_transaction  = {'block_size': next_block_size, 'block_number': next_block_number}
        transactions.append(next_transaction)
    for i in range(len(transactions)):
        if   (transactions[i]['block_size'  ] == 1) :
            transactions[i]['bytes'] = size * 4
        elif (transactions[i]['block_number'] == 1) :
            transactions[i]['bytes'] = size * 4
        else:
            transactions[i]['bytes'] = size * 8
    return transactions
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Predict Run Time')
    parser.add_argument('-s', '--sample'  , help='sample file name', action='store', type=str )
    parser.add_argument('-n', '--size'    , help='array size'      , action='store', type=int )
    parser.add_argument('-x', '--ways'    , help='argsort ways'    , action='store', type=int )
    parser.add_argument('-w', '--words'   , help='argsort words'   , action='store', type=int )
    parser.add_argument('-f', '--feedback', help='argsort feedback', action='store', type=int )
    parser.add_argument('--argsort_axi'   , help='use argsort_axi ', action='store', type=bool, default=False)

    args   = parser.parse_args()

    if (args.argsort_axi == True):
        uio         = Uio('uio_argsort')
        argsort_axi = ArgSort_AXI(uio.regs())
        ways        = argsort_axi.ways
        words       = argsort_axi.words
        feedback    = argsort_axi.stm_feedback
    else:
        ways        = args.ways
        words       = args.words
        feedback    = args.feedback

    if (args.sample != None):
        sample = np.load(args.sample)
        size   = sample.size
    else:
        size   = args.size

    band_width       = (2.0*1000.0*1000.0*1000.0) # 2.0GByte/sec
    transaction_list = calc_transaction(size,ways,words,feedback)

    read_transaction   = transaction_list.pop(0)
    transaction_index  = 1
    predicted_run_time = 0
    while (len(transaction_list) > 0):
        write_transaction  = transaction_list.pop(0)
        read_block_size    = read_transaction ['block_size'  ]
        read_block_number  = read_transaction ['block_number']
        read_bytes         = read_transaction ['bytes'       ]
        write_block_size   = write_transaction['block_size'  ]
        write_block_number = write_transaction['block_number']
        write_bytes        = write_transaction['bytes'       ]
        transaction_time   = ((write_bytes + read_bytes) / band_width)*1000.0
        print("{0}: Read: {1} x {2} , Write {3} x {4}, time {5} [msec]".format(
            transaction_index,
            read_block_size,
            read_block_number,
            write_block_size,
            write_block_number,
            transaction_time))
        transaction_index  = transaction_index + 1
        predicted_run_time = predicted_run_time + transaction_time
        read_transaction   = write_transaction

    print("expected run time {0} [msec]".format(predicted_run_time))
    
