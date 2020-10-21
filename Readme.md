ArgSorter for Ultra96
====================================================================================

Overvier
------------------------------------------------------------------------------------

### Requirement

* Board: any of the following
  - Ultra96
  - Ultra96-V2
* OS: any of the following
  - https://github.com/ikwzm/ZynqMP-FPGA-Linux
  - https://github.com/ikwzm/ZynqMP-FPGA-Ubuntu18.04-Ultra96

### Licensing

Distributed under the BSD 2-Clause License.

Quick Start
------------------------------------------------------------------------------------

### Install

#### Install ZynqMP-FPGA-Linux or ZynqMP-FPGA-Ubuntu18.04-Ultra96

See https://github.com/ikwzm/ZynqMP-FPGA-Linux or https://github.com/ikwzm/ZynqMP-FPGA-Ubuntu18.04-Ultra96

#### Boot Ultra96 or Ultra96-V2

#### Login fpga user

#### Download ArgSort-Ultra96 to Ultra96

```console
fpga@debian-fpga:~/$ git clone --branch 0.6.0 git://github.com/ikwzm/ArgSort-Ultra96.git
fpga@debian-fpga:~/$ cd ArgSort-Ultra96
```
#### Install FPGA Bitstream file and Device Tree

```console
fpga@debian-fpga:~/ArgSort-Ultra96$ sudo rake install
./dtbocfg.rb --install argsort --dts argsort_16_1_2_5.4.dts
/tmp/dtovly20201021-1043-r9dc1n: Warning (unit_address_vs_reg): /fragment@2/__overlay__/uio_argsort: node /tmp/dtovly20201021-1043-r9dc1n: Warning (avoid_unnecessary_addr_size): /fragment@2: unnecessary #address-cells/#size-cells without "ranges" or child "reg" property has a reg or ranges property, but no unit name
[ 4382.922884] fpga_manager fpga0: writing argsort_16_1_2.bin to Xilinx ZynqMP FPGA Manager
[ 4383.084520] OF: overlay: WARNING: memory leak will occur if overlay removed, property: /fpga-full/firmware-name
[ 4383.097432] fclkcfg amba_pl@0:fclk0: driver version : 1.7.1
[ 4383.103056] fclkcfg amba_pl@0:fclk0: device name    : amba_pl@0:fclk0
[ 4383.109501] fclkcfg amba_pl@0:fclk0: clock  name    : pl0_ref
[ 4383.115243] fclkcfg amba_pl@0:fclk0: clock  rate    : 249999998
[ 4383.121184] fclkcfg amba_pl@0:fclk0: clock  enabled : 1
[ 4383.126404] fclkcfg amba_pl@0:fclk0: remove rate    : 1000000
[ 4383.132148] fclkcfg amba_pl@0:fclk0: remove enable  : 0
[ 4383.137367] fclkcfg amba_pl@0:fclk0: driver installed.
[ 4383.159102] u-dma-buf udmabuf-argsort-in: driver version = 3.2.0
[ 4383.165117] u-dma-buf udmabuf-argsort-in: major number   = 241
[ 4383.170960] u-dma-buf udmabuf-argsort-in: minor number   = 0
[ 4383.176617] u-dma-buf udmabuf-argsort-in: phys address   = 0x0000000070400000
[ 4383.183755] u-dma-buf udmabuf-argsort-in: buffer size    = 33554432
[ 4383.190020] u-dma-buf amba_pl@0:udmabuf_argsort_in: driver installed.
[ 4383.212900] u-dma-buf udmabuf-argsort-out: driver version = 3.2.0
[ 4383.219002] u-dma-buf udmabuf-argsort-out: major number   = 241
[ 4383.224928] u-dma-buf udmabuf-argsort-out: minor number   = 1
[ 4383.230673] u-dma-buf udmabuf-argsort-out: phys address   = 0x0000000072400000
[ 4383.237892] u-dma-buf udmabuf-argsort-out: buffer size    = 33554432
[ 4383.244244] u-dma-buf amba_pl@0:udmabuf_argsort_out: driver installed.
[ 4383.309921] u-dma-buf udmabuf-argsort-tmp: driver version = 3.2.0
[ 4383.316030] u-dma-buf udmabuf-argsort-tmp: major number   = 241
[ 4383.321958] u-dma-buf udmabuf-argsort-tmp: minor number   = 2
[ 4383.327706] u-dma-buf udmabuf-argsort-tmp: phys address   = 0x0000000074400000
[ 4383.334939] u-dma-buf udmabuf-argsort-tmp: buffer size    = 134217728
[ 4383.341374] u-dma-buf amba_pl@0:udmabuf_argsort_tmp: driver installed.
```

### Run 

#### Generate sample.npy

```console
fpga@debian-fpga:~/ArgSort-Ultra96$ rake sample.npy
python3 generate_sample.py --size 8388608 --sample sample.npy
generate_sample: sample_file : sample.npy
generate_sample: size        : 8388608
generate_sample: time        : 342.474 [msec]
```

#### Generate expect.npy

```console
fpga@debian-fpga:~/ArgSort-Ultra96$ rake expect.npy
python3 generate_expect.py --sample sample.npy --expect expect.npy
generate_expect: sample_file : sample.npy
generate_expect: expect_file : expect.npy
generate_expect: size        : 8388608
generate_expect: time        : 19556.543 [msec]
generate_expect: throughput  : 0.429[Mwords/sec]
```

#### Run argsort_test

```console
fpga@debian-fpga:~/ArgSort-Ultra96$ rake test
python3 argsort_test.py --sample sample.npy --result result.npy -n 10
argsort_test   : sample_file : sample.npy
argsort_test   : size        : 8388608
argsort_test   : loops       : 10
argsort_test   : time        : 267.967 [msec]
argsort_test   : time        : 268.095 [msec]
argsort_test   : time        : 267.919 [msec]
argsort_test   : time        : 268.094 [msec]
argsort_test   : time        : 267.987 [msec]
argsort_test   : time        : 268.254 [msec]
argsort_test   : time        : 268.641 [msec]
argsort_test   : time        : 268.11 [msec]
argsort_test   : time        : 267.956 [msec]
argsort_test   : time        : 267.923 [msec]
argsort_test   : result_file : result.npy
argsort_test   : average_time: 268.095 [msec]
argsort_test   : throughput  : 31.29[Mwords/sec]
python3 check_result.py --sample sample.npy --result result.npy --expect expect.npy
check_result: sample file : sample.npy
check_result: expect file : expect.npy
check_result: result file : result.npy
check_result: OK
```

### Uninstall

#### Uninstall Device Tree

```console
fpga@debian-fpga:~/ArgSort-Ultra96$ sudo rake uninstall
./dtbocfg.rb --remove argsort
[ 5027.711421] u-dma-buf amba_pl@0:udmabuf_argsort_tmp: driver removed.
[ 5027.723439] u-dma-buf amba_pl@0:udmabuf_argsort_out: driver removed.
[ 5027.735371] u-dma-buf amba_pl@0:udmabuf_argsort_in: driver removed.
[ 5027.742727] fclkcfg amba_pl@0:fclk0: driver removed.
```

Build Bitstream file
------------------------------------------------------------------------------------

### Requirement

* Xilinx Vivado 2020.1

### Download ArgSort-Ultra96

```console
shell$ git clone --branch 0.6.0 git://github.com/ikwzm/ArgSort-Ultra96.git
shell$ cd ArgSort-Ultra96
shell$ git submodule update --init --recursive
```

### Build argsort_16_1_2.bin

#### Create Project

```
Vivado > Tools > Run Tcl Script... > argsort_16_1_2/create_project.tcl
```

#### Implementation

```
Vivado > Tools > Run Tcl Script... > argsort_16_1_2/implementation.tcl
```

#### Convert from Bitstream File to Binary File

```console
vivado% bootgen -image argsort_16_1_2.bif -arch zynqmp -w -o argsort_16_1_2.bin
```

Behavioral Simulation with GHDL
------------------------------------------------------------------------------------

### Requirement

* GHDL 0.35 or later

### Download ArgSort-Ultra96

```console
shell$ git clone git://github.com/ikwzm/ArgSort-Ultra96.git
shell$ cd ArgSort-Ultra96
shell$ git submodule update --init --recursive
```

### Compile Dummy_Plug

```console
shell$ cd Merge_Sorter/Dummy_Plug/sim/ghdl-0.35/dummy_plug/
shell$ make
```

### Compile PipeWork and Merge_Sorter

```console
shell$ cd sim/ghdl
shell$ make dut
../../Merge_Sorter/PipeWork/tools/vhdl-archiver.rb \
            --library MERGE_SORTER \
            --archive merge_sorter.vhd \
            ../../ip/argsort_axi_0.6//src/MERGE_SORTER/
/mnt/d/ichiro/work/ArgSort-Ultra96/Merge_Sorter/PipeWork/tools/lib/pipework/vhdl-reader.rb:149: warning: constant ::FALSE is deprecated
/mnt/d/ichiro/work/ArgSort-Ultra96/Merge_Sorter/PipeWork/tools/lib/pipework/vhdl-reader.rb:159: warning: constant ::TRUE is deprecated
/mnt/d/ichiro/work/ArgSort-Ultra96/Merge_Sorter/PipeWork/tools/lib/pipework/vhdl-reader.rb:155: warning: constant ::TRUE is deprecated
../../Merge_Sorter/PipeWork/tools/vhdl-archiver.rb \
            --library PIPEWORK \
            --use_entity 'QUEUE_ARBITER(INTEGER_ARCH)' \
            --use_entity 'SDPRAM(MODEL)' \
            --archive    pipework.vhd \
            ../../ip/argsort_axi_0.6//src/PIPEWORK/
/mnt/d/ichiro/work/ArgSort-Ultra96/Merge_Sorter/PipeWork/tools/lib/pipework/vhdl-reader.rb:149: warning: constant ::FALSE is deprecated
/mnt/d/ichiro/work/ArgSort-Ultra96/Merge_Sorter/PipeWork/tools/lib/pipework/vhdl-reader.rb:159: warning: constant ::TRUE is deprecated
/mnt/d/ichiro/work/ArgSort-Ultra96/Merge_Sorter/PipeWork/tools/lib/pipework/vhdl-reader.rb:155: warning: constant ::TRUE is deprecated
ghdl -a --mb-comments -P../../Merge_Sorter/Dummy_Plug/sim/ghdl-0.35/dummy_plug -P./ --work=PIPEWORK pipework.vhd
pipework.vhd:11155:23:warning: declaration of "data_width" hides constant "data_width" [-Whide]
pipework.vhd:13223:18:warning: declaration of "req_queue_empty" hides signal "req_queue_empty" [-Whide]
pipework.vhd:17553:18:warning: declaration of "size" hides process labeled "size" [-Whide]
pipework.vhd:17597:16:warning: declaration of "xfer_last" hides port "xfer_last" [-Whide]
pipework.vhd:26909:15:warning: declaration of "queue_tree_arbiter" hides entity "queue_tree_arbiter" [-Whide]
pipework.vhd:26992:13:warning: declaration of "arb" hides component instance "arb" [-Whide]
pipework.vhd:27509:18:warning: declaration of "i_val" hides port "i_val" [-Whide]
pipework.vhd:27591:18:warning: declaration of "i_val" hides port "i_val" [-Whide]
ghdl -a --mb-comments -P../../Merge_Sorter/Dummy_Plug/sim/ghdl-0.35/dummy_plug -P./ --work=MERGE_SORTER merge_sorter.vhd
merge_sorter.vhd:6356:23:warning: declaration of "outlet_last" hides port "outlet_last" [-Whide]
merge_sorter.vhd:10042:9:warning: declaration of "req" hides block statement labeled "req" [-Whide]
merge_sorter.vhd:10047:23:warning: declaration of "req_last" hides port "req_last" [-Whide]
merge_sorter.vhd:11211:16:warning: declaration of "merge_sorter_tree" hides entity "merge_sorter_tree" [-Whide]
merge_sorter.vhd:11953:32:warning: declaration of "a_word" hides port "a_word" [-Whide]
merge_sorter.vhd:11953:40:warning: declaration of "b_word" hides port "b_word" [-Whide]
merge_sorter.vhd:11968:30:warning: declaration of "a_word" hides port "a_word" [-Whide]
merge_sorter.vhd:11968:38:warning: declaration of "b_word" hides port "b_word" [-Whide]
```

### Run Test Bench

```console
shell$ cd sim/ghdl
shell$ make
ghdl -a --mb-comments -P../../Merge_Sorter/Dummy_Plug/sim/ghdl-0.35/dummy_plug -P./ --work=MERGE_SORTER ../../Merge_Sorter/src/test/vhdl/argsort_axi_test_bench.vhd
ghdl -e --mb-comments -P../../Merge_Sorter/Dummy_Plug/sim/ghdl-0.35/dummy_plug -P./ --work=MERGE_SORTER ArgSort_AXI_Test_Bench_X16_F2
ghdl -r --mb-comments -P../../Merge_Sorter/Dummy_Plug/sim/ghdl-0.35/dummy_plug -P./ --work=MERGE_SORTER ArgSort_AXI_Test_Bench_X16_F2
        35 ns| MARCHAL < ArgSort_AXI_Test TEST 1 Start.
        55 ns| MARCHAL < ArgSort_AXI_Test TEST 1.1 Start.
      1705 ns| MARCHAL < ArgSort_AXI_Test TEST 1.1 Done.
           :
	   :
	   :
   2391315 ns| MARCHAL < ArgSort_AXI_Test TEST 3.20 SIZE=502 Start.
   2517085 ns| MARCHAL < ArgSort_AXI_Test TEST 3.20 SIZE=502 Done.
   2517105 ns| MARCHAL < ArgSort_AXI_Test TEST 3 Done.
  ***  
  ***  ERROR REPORT TEST_X16_F2
  ***  
  ***  [ CSR ]
  ***    Error    : 0
  ***    Mismatch : 0
  ***    Warning  : 0
  ***  
  ***  [ STM AXI]
  ***    Error    : 0
  ***    Mismatch : 0
  ***    Warning  : 0
  ***  
  ***  [ MRG AXI]
  ***    Error    : 0
  ***    Mismatch : 0
  ***    Warning  : 0
  ***  
../../Merge_Sorter/src/test/vhdl/argsort_axi_test_bench.vhd:874:13:@2517126ns:(assertion note): Simulation complete(success).
```

Behavioral Simulation with Vivado
------------------------------------------------------------------------------------

### Requirement

* Xilinx Vivado 2019.2

### Download ArgSort-Ultra96

```console
shell$ git clone git://github.com/ikwzm/ArgSort-Ultra96.git
shell$ cd ArgSort-Ultra96
shell$ git submodule update --init --recursive
```

### Create Project

```
Vivado > Tools > Run Tcl Script... > sim/vivado/create_project.tcl
```

### Run Behavioral Simulation

```
Vivado > File > Project > Open... > sim/vivado/argsort_axi.xpr
Vivado > Flow Navigator > Run Simulation > Run Behavioral Simulation
```

