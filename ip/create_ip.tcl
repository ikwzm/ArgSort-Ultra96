#
# create_ip.tcl  Tcl script for create project and generate IP
#
set ip_name                 "ArgSort_AXI"
set ip_version              "0.8"
set ip_vendor_name          "ikwzm"
set ip_description          "ArgSort_AXI"
set ip_library_name         "Merge_Sorter"
set ip_root_directory       [file join [file dirname [info script]] "argsort_axi_0.8"]
set project_name            "argsort_axi"
set project_directory       [file join [file dirname [info script]] "work"]
set device_parts            "xc7z010clg400-1"
#
# Create project
#
cd [file dirname [info script]]
create_project -force $project_name $project_directory
#
# Set project properties
#
set_property "part"               $device_parts    [get_projects $project_name]
set_property "default_lib"        "xil_defaultlib" [get_projects $project_name]
set_property "simulator_language" "Mixed"          [get_projects $project_name]
set_property "target_language"    "VHDL"           [get_projects $project_name]
#
# Create fileset "sources_1"
#
if {[string equal [get_filesets -quiet sources_1] ""]} {
    create_fileset -srcset sources_1
}
#
# Create fileset "constrs_1"
#
if {[string equal [get_filesets -quiet constrs_1] ""]} {
    create_fileset -constrset constrs_1
}
#
# Create fileset "sim_1"
#
if {[string equal [get_filesets -quiet sim_1] ""]} {
    create_fileset -simset sim_1
}
#
# Create run "synth_1" and set property
#
if {[string equal [get_runs -quiet synth_1] ""]} {
    create_run -name synth_1 -part $device_parts -flow "Vivado Synthesis 2014" -strategy "Vivado Synthesis Defaults" -constrset constrs_1
} else {
  # set_property flow     "Vivado Synthesis 2014"     [get_runs synth_1]
    set_property strategy "Vivado Synthesis Defaults" [get_runs synth_1]
    set_property strategy "Flow_PerfOptimized_High"   [get_runs synth_1]
}
current_run -synthesis [get_runs synth_1]
#
# Create run "impl_1" and set property
#
if {[string equal [get_runs -quiet impl_1] ""]} {
    create_run -name impl_1 -part $device_parts -flow "Vivado Implementation 2014" -strategy "Vivado Implementation Defaults" -constrset constrs_1 -parent_run synth_1
} else {
  # set_property flow     "Vivado Implementation 2014"     [get_runs impl_1]
    set_property strategy "Vivado Implementation Defaults" [get_runs impl_1]
    set_property strategy "Performance_Explore"            [get_runs impl_1]
}
current_run -implementation [get_runs impl_1]
#
# Add files
#
proc add_vhdl_file {fileset library_name file_name} {
    set file     [file normalize $file_name]
    set fileset  [get_filesets   $fileset  ] 
    set file_obj [import_files -norecurse -fileset $fileset $file]
    set_property "file_type" "VHDL"        $file_obj
    set_property "library"   $library_name $file_obj
}
source add_sources.tcl
#
# Create IP-Package project
#
ipx::package_project -root_dir $ip_root_directory -vendor $ip_vendor_name -library $ip_library_name -taxonomy /UserIP -generated_files -import_files -force
#
# Infer Bus Interfaces
#
ipx::infer_bus_interfaces xilinx.com:interface:aximm_rtl:1.0 [ipx::current_core]
ipx::infer_bus_interfaces xilinx.com:interface:axis_rtl:1.0  [ipx::current_core]
#
# Set Supported Families
#
set_property supported_families {zynq Production virtex7 Production qvirtex7 Production kintex7 Production kintex7l Production qkintex7 Production qkintex7l Production artix7 Production artix7l Production aartix7 Production qartix7 Production zynq Production qzynq Production azynq Production zynquplus Production} [ipx::current_core]
#
# Set Core Version
#
set_property core_revision 0               [ipx::current_core]
set_property name          $ip_name        [ipx::current_core]
set_property display_name  $ip_name        [ipx::current_core]
set_property version       $ip_version     [ipx::current_core]
set_property description   $ip_description [ipx::current_core]
#
# Generate files
#
ipx::create_xgui_files       [ipx::current_core]
ipx::update_checksums        [ipx::current_core]
ipx::save_core               [ipx::current_core]
#
# Close and Done.
#
close_project
