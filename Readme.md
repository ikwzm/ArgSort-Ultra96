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

Design
------------------------------------------------------------------------------------

### Design Block

![Fig.1 ArgSort-Ultra96 Design Block](./doc/ja/argsort-ultra96-bd.png "Fig.1 ArgSort-Ultra96 Design Block")

Fig.1 ArgSort-Ultra96 Design Block


### Utilization

Table.2 Utilization

<table border="2">
  <tr>
    <td align="center" colspan="4">Design</td>
    <td align="center" colspan="4">Resources</td>
    <td align="center">Freq</td>
  </tr>
  <tr>
    <td align="center">Name</td>
    <td align="center">MRG<br />WAYS</td>
    <td align="center">MRG<br />WORDS</td>
    <td align="center">STM<br />FB</td>
    <td align="center">CLB<br />LUTs</td>
    <td align="center">CLB<br />Register</td>
    <td align="center">BLOCK<br />RAM</td>
    <td align="center">DSPs</td>
    <td align="center">Freq<br />[MHz]</td>
  </tr>
  <tr>
    <td>argsort_16_1_0</td>
    <td align="center">16</td>
    <td align="center">1</td>
    <td align="center">0</td>
    <td align="center">42142</td>
    <td align="center">27011</td>
    <td align="center">38</td>
    <td align="center">0</td>
    <td align="center">250</td>
  </tr>
  <tr>
    <td>argsort_16_1_1</td>
    <td align="center">16</td>
    <td align="center">1</td>
    <td align="center">1</td>
    <td align="center">41865</td>
    <td align="center">27249</td>
    <td align="center">38</td>
    <td align="center">0</td>
    <td align="center">250</td>
  </tr>
  <tr>
    <td>argsort_16_1_2</td>
    <td align="center">16</td>
    <td align="center">1</td>
    <td align="center">2</td>
    <td align="center">41799</td>
    <td align="center">26261</td>
    <td align="center">54</td>
    <td align="center">0</td>
    <td align="center">250</td>
  </tr>
  <tr>
    <td>argsort_16_2_0</td>
    <td align="center">16</td>
    <td align="center">2</td>
    <td align="center">0</td>
    <td align="center">59246</td>
    <td align="center">55456</td>
    <td align="center">38</td>
    <td align="center">0</td>
    <td align="center">250</td>
  </tr>
  <tr>
    <td>argsort_16_2_1</td>
    <td align="center">16</td>
    <td align="center">2</td>
    <td align="center">1</td>
    <td align="center">60828</td>
    <td align="center">57063</td>
    <td align="center">38</td>
    <td align="center">0</td>
    <td align="center">250</td>
  </tr>
  <tr>
    <td>argsort_16_2_2</td>
    <td align="center">16</td>
    <td align="center">2</td>
    <td align="center">2</td>
    <td align="center">58819</td>
    <td align="center">55210</td>
    <td align="center">70</td>
    <td align="center">0</td>
    <td align="center">250</td>
  </tr>
  <tr>
    <td>argsort_32_1_0</td>
    <td align="center">32</td>
    <td align="center">1</td>
    <td align="center">0</td>
    <td align="center">64126</td>
    <td align="center">45025</td>
    <td align="center">70</td>
    <td align="center">15</td>
    <td align="center">250</td>
  </tr>
  <tr>
    <td>argsort_32_1_1</td>
    <td align="center">32</td>
    <td align="center">1</td>
    <td align="center">1</td>
    <td align="center">66621</td>
    <td align="center">46356</td>
    <td align="center">70</td>
    <td align="center">15</td>
    <td align="center">250</td>
  </tr>
  <tr>
    <td>argsort_32_1_2</td>
    <td align="center">32</td>
    <td align="center">1</td>
    <td align="center">2</td>
    <td align="center">64988</td>
    <td align="center">44866</td>
    <td align="center">198</td>
    <td align="center">15</td>
    <td align="center">250</td>
  </tr>
  <tr>
    <td>argsort_32_2_0</td>
    <td align="center">32</td>
    <td align="center">2</td>
    <td align="center">0</td>
    <td align="center" colspan="4">resource over</td>
    <td align="center"></td>
  </tr>
  <tr>
    <td colspan="4">zcu3egsbva48-1 resouce available</td>
    <td align="center">70560</td>
    <td align="center">141120</td>
    <td align="center">216</td>
    <td align="center">360</td>
    <td align="center"></td>
  </tr>
</table>

<br />

![Fig.2 Utlization(LUTs %)](./doc/ja/argsort-ultra96-resources.jpg "Fig.2 Utlization(LUTs %)")

Fig.2 Utlization(LUTs %)

<br />

### Performance


Table.3 Performance

<table border="2">
  <tr>
    <td align="center" colspan="4">Design</td>
    <td align="center" colspan="3">Sort time [msec]</td>
    <td align="center" rowspan="2">Throughput <br />Average<br />[Mwords/sec]</td>
  </tr>
  <tr>
    <td align="center">Name</td>
    <td align="center">MRG<br />WAYS</td>
    <td align="center">MRG<br />WORDS</td>
    <td align="center">STM<br />FB</td>
    <td align="center">10K<br />[words]</td>
    <td align="center">100K<br />[words]</td>
    <td align="center">1M<br />[words]</td>
  <tr>
    <td>argsort_16_1_0</td>
    <td align="center">16</td>
    <td align="center">1</td>
    <td align="center">0</td>
    <td align="right">0.569</td>
    <td align="right">4.766</td>
    <td align="right">54.456</td>
    <td align="right">18.75</td>
  </tr>
  <tr>
    <td>argsort_16_1_1</td>
    <td align="center">16</td>
    <td align="center">1</td>
    <td align="center">1</td>
    <td align="right">0.400</td>
    <td align="right">3.000</td>
    <td align="right">34.355</td>
    <td align="right">29.51</td>
  </tr>
  <tr>
    <td>argsort_16_1_2</td>
    <td align="center">16</td>
    <td align="center">1</td>
    <td align="center">2</td>
    <td align="right">0.384</td>
    <td align="right">2.674</td>
    <td align="right">27.644</td>
    <td align="right">36.04</td>
  </tr>
  <tr>
    <td>argsort_16_2_0</td>
    <td align="center">16</td>
    <td align="center">2</td>
    <td align="center">0</td>
    <td align="right">0.436</td>
    <td align="right">3.219</td>
    <td align="right">42.970</td>
    <td align="right">24.13</td>
  </tr>
  <tr>
    <td>argsort_16_2_1</td>
    <td align="center">16</td>
    <td align="center">2</td>
    <td align="center">1</td>
    <td align="right">0.325</td>
    <td align="right">2.047</td>
    <td align="right">31.311</td>
    <td align="right">33.89</td>
  </tr>
  <tr>
    <td>argsort_16_2_2</td>
    <td align="center">16</td>
    <td align="center">2</td>
    <td align="center">2</td>
    <td align="right">0.328</td>
    <td align="right">1.802</td>
    <td align="right">26.314</td>
    <td align="right">40.01</td>
  </tr>
  <tr>
    <td>argsort_32_1_0</td>
    <td align="center">32</td>
    <td align="center">1</td>
    <td align="center">0</td>
    <td align="right">0.422</td>
    <td align="right">3.384</td>
    <td align="right">39.381</td>
    <td align="right">25.69</td>
  </tr>
  <tr>
    <td>argsort_32_1_1</td>
    <td align="center">32</td>
    <td align="center">1</td>
    <td align="center">1</td>
    <td align="right">0.341</td>
    <td align="right">2.494</td>
    <td align="right">27.748</td>
    <td align="right">36.31</td>
  </tr>
  <tr>
    <td>argsort_32_1_2</td>
    <td align="center">32</td>
    <td align="center">1</td>
    <td align="center">2</td>
    <td align="right">0.595</td>
    <td align="right">2.711</td>
    <td align="right">27.433</td>
    <td align="right">36.79</td>
  </tr>
  <tr>
    <td colspan="4">ZynqMP(arm64) numpy.argsort()</td>
    <td align="right">1.790</td>
    <td align="right">32.036</td>
    <td align="right">1320.921</td>
    <td align="right">1.49</td>
  </tr>
</table>


<br />


![Fig.3 Throughput Average [Mwords/sec]](./doc/ja/argsort-ultra96-performance.jpg "Fig.3 Throughput Average [Mwords/sec]")

Fig.3 Throughput Average [Mwords/sec]

<br />




Quick Start
------------------------------------------------------------------------------------

### Install

#### Install ZynqMP-FPGA-Linux or ZynqMP-FPGA-Ubuntu18.04-Ultra96

See https://github.com/ikwzm/ZynqMP-FPGA-Linux or https://github.com/ikwzm/ZynqMP-FPGA-Ubuntu18.04-Ultra96

#### Boot Ultra96 or Ultra96-V2

#### Login fpga user

#### Download ArgSort-Ultra96 to Ultra96

```console
fpga@debian-fpga:~/$ git clone --branch 0.9.0 git://github.com/ikwzm/ArgSort-Ultra96.git
fpga@debian-fpga:~/$ cd ArgSort-Ultra96
```
#### Install FPGA Bitstream file and Device Tree

```console
fpga@debian-fpga:~/ArgSort-Ultra96$ sudo rake install
gzip -d -f -c argsort_16_2_2.bin.gz > /lib/firmware/argsort_16_2_2.bin
./dtbocfg.rb --install argsort --dts argsort_16_2_2_5.4.dts
/tmp/dtovly20201118-1281-1tf8e0q: Warning (unit_address_vs_reg): /fragment@2/__overlay__/uio_argsort: node has a reg or ranges property, but no unit name
/tmp/dtovly20201118-1281-1tf8e0q: Warning (avoid_unnecessary_addr_size): /fragment@2: unnecessary #address-cells/#size-cells without "ranges" or child "reg" property
[10952.701089] fpga_manager fpga0: writing argsort_16_2_2.bin to Xilinx ZynqMP FPGA Manager
[10952.861395] OF: overlay: WARNING: memory leak will occur if overlay removed, property: /fpga-full/firmware-name
[10952.874409] fclkcfg amba_pl@0:fclk0: driver version : 1.7.1
[10952.879998] fclkcfg amba_pl@0:fclk0: device name    : amba_pl@0:fclk0
[10952.886447] fclkcfg amba_pl@0:fclk0: clock  name    : pl0_ref
[10952.892194] fclkcfg amba_pl@0:fclk0: clock  rate    : 249999998
[10952.898138] fclkcfg amba_pl@0:fclk0: clock  enabled : 1
[10952.903363] fclkcfg amba_pl@0:fclk0: remove rate    : 1000000
[10952.909107] fclkcfg amba_pl@0:fclk0: remove enable  : 0
[10952.914327] fclkcfg amba_pl@0:fclk0: driver installed.
[10952.935858] u-dma-buf udmabuf-argsort-in: driver version = 3.2.0
[10952.941868] u-dma-buf udmabuf-argsort-in: major number   = 241
[10952.947704] u-dma-buf udmabuf-argsort-in: minor number   = 0
[10952.953360] u-dma-buf udmabuf-argsort-in: phys address   = 0x0000000070400000
[10952.960498] u-dma-buf udmabuf-argsort-in: buffer size    = 33554432
[10952.966762] u-dma-buf amba_pl@0:udmabuf_argsort_in: driver installed.
[10952.988678] u-dma-buf udmabuf-argsort-out: driver version = 3.2.0
[10952.994773] u-dma-buf udmabuf-argsort-out: major number   = 241
[10953.000697] u-dma-buf udmabuf-argsort-out: minor number   = 1
[10953.006438] u-dma-buf udmabuf-argsort-out: phys address   = 0x0000000072400000
[10953.013662] u-dma-buf udmabuf-argsort-out: buffer size    = 33554432
[10953.020014] u-dma-buf amba_pl@0:udmabuf_argsort_out: driver installed.
[10953.085033] u-dma-buf udmabuf-argsort-tmp: driver version = 3.2.0
[10953.091130] u-dma-buf udmabuf-argsort-tmp: major number   = 241
[10953.097060] u-dma-buf udmabuf-argsort-tmp: minor number   = 2
[10953.102804] u-dma-buf udmabuf-argsort-tmp: phys address   = 0x0000000074400000
[10953.110028] u-dma-buf udmabuf-argsort-tmp: buffer size    = 134217728
[10953.116466] u-dma-buf amba_pl@0:udmabuf_argsort_tmp: driver installed.
```

### Run 

#### Generate sample.npy

```console
fpga@debian-fpga:~/ArgSort-Ultra96$ rake sample.npy
python3 generate_sample.py --size 8388608 --sample sample.npy
generate_sample: sample_file : sample.npy
generate_sample: size        : 8388608
generate_sample: time        : 347.344 [msec]
```

#### Generate expect.npy

```console
fpga@debian-fpga:~/ArgSort-Ultra96$ rake expect.npy
python3 generate_expect.py --sample sample.npy --expect expect.npy
generate_expect: sample_file : sample.npy
generate_expect: expect_file : expect.npy
generate_expect: size        : 8388608
generate_expect: time        : 19599.039 [msec]
generate_expect: throughput  : 0.428[Mwords/sec]
```

#### Run argsort_test

```console
fpga@debian-fpga:~/ArgSort-Ultra96$ rake test
python3 argsort_test.py --sample sample.npy --result result.npy -n 10
argsort_test   : Version     : 0.9
argsort_test   : Ways        : 16
argsort_test   : Words       : 2
argsort_test   : Feedback    : 2
argsort_test   : WordBits    : 32
argsort_test   : IndexBits   : 32
argsort_test   : Sort Order  : 0
argsort_test   : Sign Compare: 0
argsort_test   : Debug Enable: 1
argsort_test   : sample_file : sample.npy
argsort_test   : size        : 8388608
argsort_test   : loops       : 10
argsort_test   : time        : 252.58 [msec]
argsort_test   : time        : 251.791 [msec]
argsort_test   : time        : 251.914 [msec]
argsort_test   : time        : 251.818 [msec]
argsort_test   : time        : 251.798 [msec]
argsort_test   : time        : 252.294 [msec]
argsort_test   : time        : 251.987 [msec]
argsort_test   : time        : 252.085 [msec]
argsort_test   : time        : 252.3 [msec]
argsort_test   : time        : 252.09 [msec]
argsort_test   : result_file : result.npy
argsort_test   : average_time: 252.066 [msec]
argsort_test   : throughput  : 33.279[Mwords/sec]
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
[11218.745653] u-dma-buf amba_pl@0:udmabuf_argsort_tmp: driver removed.
[11218.757907] u-dma-buf amba_pl@0:udmabuf_argsort_out: driver removed.
[11218.770021] u-dma-buf amba_pl@0:udmabuf_argsort_in: driver removed.
[11218.777459] fclkcfg amba_pl@0:fclk0: driver removed.
```

Build Bitstream file
------------------------------------------------------------------------------------

### Requirement

* Xilinx Vivado 2020.1

### Download ArgSort-Ultra96

```console
shell$ git clone --branch 0.9.0 git://github.com/ikwzm/ArgSort-Ultra96.git
shell$ cd ArgSort-Ultra96
shell$ git submodule update --init --recursive
```

### Build argsort_16_2_2.bin

#### Create Project

```
Vivado > Tools > Run Tcl Script... > argsort_16_2_2/create_project.tcl
```

#### Implementation

```
Vivado > Tools > Run Tcl Script... > argsort_16_2_2/implementation.tcl
```

#### Convert from Bitstream File to Binary File

```console
vivado% bootgen -image argsort_16_2_2.bif -arch zynqmp -w -o argsort_16_2_2.bin
```

#### Compress argsort_16_2_2.bin to argsort_16_2_2.bin.gz

```console
vivado% gzip argsort_16_2_2.bin
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
            ../../ip/argsort_axi_0.8//src/MERGE_SORTER/
/mnt/d/ichiro/work/ArgSort-Ultra96/Merge_Sorter/PipeWork/tools/lib/pipework/vhdl-reader.rb:149: warning: constant ::FALSE is deprecated
/mnt/d/ichiro/work/ArgSort-Ultra96/Merge_Sorter/PipeWork/tools/lib/pipework/vhdl-reader.rb:159: warning: constant ::TRUE is deprecated
/mnt/d/ichiro/work/ArgSort-Ultra96/Merge_Sorter/PipeWork/tools/lib/pipework/vhdl-reader.rb:155: warning: constant ::TRUE is deprecated
../../Merge_Sorter/PipeWork/tools/vhdl-archiver.rb \
            --library PIPEWORK \
            --use_entity 'SDPRAM(MODEL)' \
            --archive    pipework.vhd \
            ../../ip/argsort_axi_0.8//src/PIPEWORK/
/mnt/d/ichiro/work/ArgSort-Ultra96/Merge_Sorter/PipeWork/tools/lib/pipework/vhdl-reader.rb:149: warning: constant ::FALSE is deprecated
/mnt/d/ichiro/work/ArgSort-Ultra96/Merge_Sorter/PipeWork/tools/lib/pipework/vhdl-reader.rb:159: warning: constant ::TRUE is deprecated
/mnt/d/ichiro/work/ArgSort-Ultra96/Merge_Sorter/PipeWork/tools/lib/pipework/vhdl-reader.rb:155: warning: constant ::TRUE is deprecated
ghdl -a --mb-comments -P../../Merge_Sorter/Dummy_Plug/sim/ghdl-0.35/dummy_plug -P./ --work=PIPEWORK pipework.vhd
pipework.vhd:11179:23:warning: declaration of "data_width" hides constant "data_width" [-Whide]
pipework.vhd:13247:18:warning: declaration of "req_queue_empty" hides signal "req_queue_empty" [-Whide]
pipework.vhd:17776:18:warning: declaration of "size" hides process labeled "size" [-Whide]
pipework.vhd:17820:16:warning: declaration of "xfer_last" hides port "xfer_last" [-Whide]
pipework.vhd:27457:15:warning: declaration of "queue_tree_arbiter" hides entity "queue_tree_arbiter" [-Whide]
pipework.vhd:27540:13:warning: declaration of "arb" hides component instance "arb" [-Whide]
pipework.vhd:28081:18:warning: declaration of "i_val" hides port "i_val" [-Whide]
pipework.vhd:28163:18:warning: declaration of "i_val" hides port "i_val" [-Whide]
ghdl -a --mb-comments -P../../Merge_Sorter/Dummy_Plug/sim/ghdl-0.35/dummy_plug -P./ --work=MERGE_SORTER merge_sorter.vhd
merge_sorter.vhd:6977:23:warning: declaration of "outlet_last" hides port "outlet_last" [-Whide]
merge_sorter.vhd:7532:19:warning: declaration of "o_word" hides port "o_word" [-Whide]
merge_sorter.vhd:10846:9:warning: declaration of "req" hides block statement labeled "req" [-Whide]
merge_sorter.vhd:10851:23:warning: declaration of "req_last" hides port "req_last" [-Whide]
merge_sorter.vhd:12229:23:warning: declaration of "state_type" hides type "state_type" [-Whide]
merge_sorter.vhd:12230:23:warning: declaration of "curr_state" hides signal "curr_state" [-Whide]
merge_sorter.vhd:12480:16:warning: declaration of "merge_sorter_tree" hides entity "merge_sorter_tree" [-Whide]
merge_sorter.vhd:13452:32:warning: declaration of "a_word" hides port "a_word" [-Whide]
merge_sorter.vhd:13452:40:warning: declaration of "b_word" hides port "b_word" [-Whide]
merge_sorter.vhd:13467:30:warning: declaration of "a_word" hides port "a_word" [-Whide]
merge_sorter.vhd:13467:38:warning: declaration of "b_word" hides port "b_word" [-Whide]
```

### Run Test Bench

```console
shell$ cd sim/ghdl
shell$ make
ghdl -a --mb-comments -P../../Merge_Sorter/Dummy_Plug/sim/ghdl-0.35/dummy_plug -P./ --work=MERGE_SORTER ../../Merge_Sorter/src/test/vhdl/argsort_axi_test_bench.vhd
ghdl -e --mb-comments -P../../Merge_Sorter/Dummy_Plug/sim/ghdl-0.35/dummy_plug -P./ --work=MERGE_SORTER ArgSort_AXI_Test_Bench_X16_W1_F2
ghdl -r --mb-comments -P../../Merge_Sorter/Dummy_Plug/sim/ghdl-0.35/dummy_plug -P./ --work=MERGE_SORTER ArgSort_AXI_Test_Bench_X16_W1_F2
        35 ns| MARCHAL < ArgSort_AXI_Test TEST 1 Start.
        55 ns| MARCHAL < ArgSort_AXI_Test TEST 1.1 Start.
      1705 ns| MARCHAL < ArgSort_AXI_Test TEST 1.1 Done.
           :
	   :
	   :
   3243505 ns| MARCHAL < ArgSort_AXI_Test TEST 3.20 SIZE=479 Start.
   3370415 ns| MARCHAL < ArgSort_AXI_Test TEST 3.20 SIZE=479 Done.
   3370435 ns| MARCHAL < ArgSort_AXI_Test TEST 3 Done.
  ***  
  ***  ERROR REPORT TEST_X16_W1_F2
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
../../Merge_Sorter/src/test/vhdl/argsort_axi_test_bench.vhd:875:13:@3370456ns:(assertion note): Simulation complete(success).
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

