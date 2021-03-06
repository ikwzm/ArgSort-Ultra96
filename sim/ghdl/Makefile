
ARGSORT_IP_PATH      = ../../ip/argsort_kernel_1.0/
PIPEWORK_PATH        = ../../Merge_Sorter/PipeWork
PIPEWORK_TOOL_PATH   = $(PIPEWORK_PATH)/tools

DUMMY_PLUG_PATH      = ../../Merge_Sorter/Dummy_Plug
DUMMY_PLUG_SRC_PATH  = $(DUMMY_PLUG_PATH)/src/main/vhdl
DUMMY_PLUG_WORK_PATH = $(DUMMY_PLUG_PATH)/sim/ghdl-0.35/dummy_plug

SCENARIO_PATH        = ../../Merge_Sorter/src/test/scenarios/argsort_kernel

COPY       = cp
CAT        = cat
REMOVE     = -rm
GHDL       = ghdl
GHDLFLAGS  = --mb-comments -P$(DUMMY_PLUG_WORK_PATH) -P./

test   : test_x16_w1_f2 \
         $(END_LIST)

clean  :
	$(REMOVE) *.cf pipework.vhd merge_sorter.vhd

pipework-obj93.cf : pipework.vhd
	$(GHDL) -a $(GHDLFLAGS) --work=PIPEWORK pipework.vhd

pipework.vhd : 
	$(PIPEWORK_TOOL_PATH)/vhdl-archiver.rb \
            --library PIPEWORK \
            --use_entity 'SDPRAM(MODEL)' \
            --archive    pipework.vhd \
            $(ARGSORT_IP_PATH)/src/PIPEWORK/

merge_sorter-obj93.cf : merge_sorter.vhd pipework-obj93.cf
	$(GHDL) -a $(GHDLFLAGS) --work=MERGE_SORTER merge_sorter.vhd

merge_sorter.vhd : 
	$(PIPEWORK_TOOL_PATH)/vhdl-archiver.rb \
            --library MERGE_SORTER \
            --archive merge_sorter.vhd \
            $(ARGSORT_IP_PATH)/src/MERGE_SORTER/

dut         :  merge_sorter-obj93.cf

test_bench  :  dut
	$(GHDL) -a $(GHDLFLAGS) --work=MERGE_SORTER ../../Merge_Sorter/src/test/vhdl/argsort_kernel_test_bench.vhd

test_x16_w1_f2 : test_x16_w1_f2.snr test_bench
	$(GHDL) -e $(GHDLFLAGS) --work=MERGE_SORTER ArgSort_Kernel_Test_Bench_X16_W1_F2
	$(GHDL) -r $(GHDLFLAGS) --work=MERGE_SORTER ArgSort_Kernel_Test_Bench_X16_W1_F2

test_x16_w1_f2.snr : $(SCENARIO_PATH)/test_x16_w1_f2_1.snr $(SCENARIO_PATH)/test_x16_w1_f2_2.snr $(SCENARIO_PATH)/test_x16_w1_f2_3.snr
	$(CAT) $^ > $@

