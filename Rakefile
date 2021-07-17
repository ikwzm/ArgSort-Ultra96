require 'yaml'
ENV_YAML_FILE = "Rakefile.env"
if File.exist?(ENV_YAML_FILE)
  env = open(ENV_YAML_FILE, 'r'){ |f| YAML.load(f) }
else
  env = {}
end
if ENV.key?("TARGET")
  env["TARGET"] = ENV["TARGET"]
  YAML.dump(env, File.open(ENV_YAML_FILE, 'w'))
end
TARGET                 = env.fetch("TARGET", "argsort_16_2_2")

FPGA_BITSTREAM_FILE    = TARGET + ".bin"
FPGA_BITSTREAM_GZ_FILE = FPGA_BITSTREAM_FILE + ".gz"
LINUX_KERNEL_RELEASE   = /^(\d+\.\d+)/.match(`uname -r`)[1]
DEVICE_TREE_FILE       = TARGET + "_" + LINUX_KERNEL_RELEASE + ".dts"
DEVICE_TREE_NAME       = "argsort"
DEVICE_TREE_DIRECTORY  = "/config/device-tree/overlays/" + DEVICE_TREE_NAME
UIO_DEVICE_NAMES       = ["uio_argsort"]
UDMABUF_DEVICE_NAMES   = ["udmabuf-argsort-in", "udmabuf-argsort-out", "udmabuf-argsort-tmp"]

SAMPLE_SIZE_LIST       = Array.new(200){|i| (i+1)*5000}
SAMPLE_FILE_FORMAT     = "sample_%010d.npy"
EXPECT_FILE_FORMAT     = "expect_%010d.npy"
RESULT_FILE_FORMAT     = "result_%010d.npy"
TEST_LOG_FILE_NAME     = "#{TARGET}.log"
EXPECT_LOG_FILE_NAME   = "expect.log"
PYTHON                 = "python3"
CC                     = "g++"
CFLAGS                 = "-I ./include -Wpointer-arith"
DTBOCFG                = "./dtbocfg.rb"

require 'rake/clean'

def find_uio_device(name)
  found_device_name = nil
  Dir::entries("/sys/class/uio").map{ |device_name|
    if device_name =~ /^uio/
      File.open("/sys/class/uio/#{device_name}/name"){|file|
        if name.eql?(file.gets.chop)
          found_device_name = device_name
        end
      }
    end
  }
  return found_device_name
end

desc "Install fpga and devicetrees(#{DEVICE_TREE_NAME})"
task :install => ["/lib/firmware/#{FPGA_BITSTREAM_FILE}", DEVICE_TREE_FILE] do
  begin
    sh "#{DTBOCFG} --install #{DEVICE_TREE_NAME} --dts #{DEVICE_TREE_FILE}"
  rescue => e
    print "error raised:"
    p e
    abort
  end
  if (Dir.exist?(DEVICE_TREE_DIRECTORY) == false)
    abort "can not #{DEVICE_TREE_DIRECTORY} installed."
  end

  UIO_DEVICE_NAMES.each do |device_name|
    device_file = find_uio_device(device_name)
    if (device_file.nil?)
      abort "can not find uio device file named #{device_name}"
    end
    if (File.exist?("/dev/" + device_file) == false)
      abort "can not /dev/#{device_file} installed."
    end
    File::chmod(0666, "/dev/" + device_file)
  end    

  UDMABUF_DEVICE_NAMES.each do |device_file|
    device_file_name = File.join("/", "dev", device_file)
    if (File.exist?(device_file_name) == false)
      abort "can not found #{device_file_name}"
    end
    File::chmod(0666, device_file_name)
    ["udmabuf", "u-dma-buf"].each do |class_name|
      sys_class_path = File.join("/", "sys", "class", class_name, device_file)
      if (File.exist?(sys_class_path) == true) then
        File::chmod(0666, File.join(sys_class_path, "sync_mode"      ))
        File::chmod(0666, File.join(sys_class_path, "sync_offset"    ))
        File::chmod(0666, File.join(sys_class_path, "sync_size"      ))
        File::chmod(0666, File.join(sys_class_path, "sync_direction" ))
        File::chmod(0666, File.join(sys_class_path, "sync_owner"     ))
        File::chmod(0666, File.join(sys_class_path, "sync_for_cpu"   ))
        File::chmod(0666, File.join(sys_class_path, "sync_for_device"))
      end
    end
  end
end

desc "Uninstall fpga and devicetrees(#{DEVICE_TREE_NAME})"
task :uninstall do
  if (Dir.exist?(DEVICE_TREE_DIRECTORY) == false)
    abort "can not #{DEVICE_TREE_DIRECTORY} uninstalled: does not already exists."
  end
  sh "#{DTBOCFG} --remove #{DEVICE_TREE_NAME}"
end

file "/lib/firmware/" + FPGA_BITSTREAM_FILE => [ FPGA_BITSTREAM_GZ_FILE ] do
  sh "gzip -d -f -c #{FPGA_BITSTREAM_GZ_FILE} > /lib/firmware/#{FPGA_BITSTREAM_FILE}"
end
CLOBBER.include("/lib/firmware/" + FPGA_BITSTREAM_FILE)

directory DEVICE_TREE_DIRECTORY do
  Rake::Task["install"].invoke
end

file DEVICE_TREE_FILE => [ "argsort_axi.dts" ] do
  linux_release_number = 0
  /(\d+)\.(\d+)/.match(LINUX_KERNEL_RELEASE)[1..2].each do |n|
    linux_release_number = linux_release_number*100 + n.to_i
  end
  if linux_release_number < 419 then
    clk_name = "clkc"
  else 
    clk_name = "zynqmp_clk"
  end
  File.open(DEVICE_TREE_FILE, "w") do |o_file|
    File.open("argsort_axi.dts") do |i_file|
      i_file.each_line do |line|
        line = line.gsub(/(^\s*firmware-name\s*=\s*)(.*);/){"#{$1}\"#{FPGA_BITSTREAM_FILE}\";"}
        line = line.gsub(/&zynqmp_clk/, "&#{clk_name}")
        if linux_release_number < 500 then
          line = line.gsub(/(^\s*compatible\s*=\s*)("ikwzm,u-dma-buf");/){"#{$1}\"ikwzm,udmabuf-0.10.a\";"};
        end
        o_file.puts(line)
      end
    end
  end
end

TEST_TASK_LIST = Array.new
SAMPLE_SIZE_LIST.each do |sample_size|
  sample_file_name = SAMPLE_FILE_FORMAT % [sample_size]
  expect_file_name = EXPECT_FILE_FORMAT % [sample_size]
  result_file_name = RESULT_FILE_FORMAT % [sample_size]
  
  file sample_file_name => [ "generate_sample.py" ] do
    sh "#{PYTHON} generate_sample.py --size #{sample_size} --sample #{sample_file_name}"
  end
  CLOBBER.include(sample_file_name)

  file expect_file_name => [ "generate_expect.py", sample_file_name ] do
    sh "#{PYTHON} generate_expect.py --sample #{sample_file_name} --expect #{expect_file_name} --log #{EXPECT_LOG_FILE_NAME}"
  end
  CLOBBER.include(expect_file_name)

  file result_file_name => [ sample_file_name ] do
    sh "#{PYTHON} argsort_test.py --sample #{sample_file_name} --result #{result_file_name}"
  end
  CLEAN.include(result_file_name)

  desc "ArgSort_Krnl Test(size=#{sample_size})"
  task_name = sprintf("test_%d", sample_size).to_sym
  task task_name => [sample_file_name, expect_file_name] do
    sh "#{PYTHON} argsort_test.py --sample #{sample_file_name} --result #{result_file_name} -n 10 -d 2 --log #{TEST_LOG_FILE_NAME} "
    sh "#{PYTHON} check_result.py --sample #{sample_file_name} --result #{result_file_name} --expect #{expect_file_name}"
  end

  TEST_TASK_LIST << task_name
end

task :sample_all do
  SAMPLE_SIZE_LIST.each do |sample_size|
    sample_file_name = SAMPLE_FILE_FORMAT % [sample_size]
    Rake::Task[sample_file_name].invoke
  end
end

task :expect_all do
  sh "echo --- > #{EXPECT_LOG_FILE_NAME}"
  SAMPLE_SIZE_LIST.each do |sample_size|
    expect_file_name = EXPECT_FILE_FORMAT % [sample_size]
    Rake::Task[expect_file_name].invoke
  end
end

desc "ArgSort_Krnl Test All Size"
task :test_all do
  sh "echo --- > #{TEST_LOG_FILE_NAME}"
  TEST_TASK_LIST.each do |task_name|
    Rake::Task[task_name].invoke
  end    
end

desc "ArgSort_AXI Infomation"
task :info do
  sh "#{PYTHON} argsort_info.py"
end

task :default => [TEST_TASK_LIST[0]]

