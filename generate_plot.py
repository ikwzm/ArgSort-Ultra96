import yaml
import math
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot Log Data')
    parser.add_argument('-l', '--log_files'  , help='log files', nargs='+', required=True )
    parser.add_argument('-s', '--size_list'  , help='size list', nargs='+', required=False)
    parser.add_argument('-d', '--data_file'  , help='gnu plot data file name'  , action='store', type=str, default="gnuplot.dat")
    parser.add_argument('-p', '--plot_script', help='gnu plot script file name', action='store', type=str, default="gnuplot.gp")
    parser.add_argument('-y', '--yscale'     , help='y scale factor' , action='store', type=float, default=1.0)

    args = parser.parse_args()

    log_files  = args.log_files
    data_file  = args.data_file
    size_list  = args.size_list

    data_list  = {}
    title_list = {}
    name_list  = []
    max_time   = 0

    for log_file_name in log_files:
        with open(log_file_name) as log_file:
            log_data_list = yaml.safe_load(log_file)
            for log_data in log_data_list:
                if 'Ways' in log_data:
                    ways     = log_data['Ways']
                    words    = log_data['Words']
                    feedback = log_data['Feedback']
                    name     = "{0}_{1}_{2}".format(ways, words, feedback)
                    title    = "Ways={0},Words={1},Feedback={2}".format(ways, words, feedback)
                elif 'expect_file' in log_data:
                    name     = "expect"
                    title    = "numpy on ZynqMP(arm64)"
                else:
                    break
                if not name in name_list :
                    name_list.append(name)
                if not name in title_list:
                    title_list[name] = title
                size = str(log_data['size'])
                time = log_data['average_time']
                if not size_list or size in size_list:
                    if size  in data_list:
                        data_list[size][name] = time
                    else:
                        data_list[size] = {name: time}
                    if max_time < time:
                        max_time = time

    with open(data_file, mode='w') as f:
        print("{0} {1}".format("#size", " ".join(name_list)), file=f)

        for size,data in sorted(data_list.items(), key=lambda x:int(x[0])):
            time_list = []
            for name in name_list:
                if name in data :
                    time_list.append(str(data[name]))
                else:
                    time_list.append('-')
            print("{0} {1}".format(size, " ".join(time_list)), file=f)

    with open(args.plot_script, mode='w') as f:
        color_table = {'16_1_0' : 'light-blue',
                       '16_1_1' : 'blue',
                       '16_1_2' : 'dark-blue',
                       '16_2_0' : 'light-red',
                       '16_2_1' : 'red',
                       '16_2_2' : 'dark-red',
                       '32_1_0' : 'light-green',
                       '32_1_1' : 'green',
                       '32_1_2' : 'dark-green',
                       'expect' : 'pink'}
        key_font_size = 8
        max_yrange    = (math.ceil(float(max_time)/10.0)*10.0)*args.yscale
        print('set xlabel "{}"'.format('entry size'), file=f)
        print('set ylabel "{}"'.format('average time [msec]'), file=f)
        print('set yrange [{}:{}]'.format(0, max_yrange), file=f)
        print('set style fill solid border lc rgb "black"', file=f)
        print('set key left top', file=f)
        print('set key font ",{}"'.format(key_font_size), file=f)
        print('set boxwidth 1', file=f)
        n_item = len(name_list)
        plot_list = []
        index  = 0
        for name in name_list:
            title = title_list[name]
            color = color_table[name]
            plot_list.append('"{}" using ($0*{}+{}):{:<3d} {:<7s} with boxes lw 2 lc rgb "{}" title "{}"'. format(data_file, n_item+3, index, index+2, ':xtic(1)' if (index == n_item//2) else '', color, title))
            index = index + 1
        print('plot {0}'.format(",\\\n     ".join(plot_list)), file=f)

