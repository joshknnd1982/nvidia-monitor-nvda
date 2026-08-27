import os
import subprocess
import threading
import time
import datetime
import versionInfo
from logHandler import log
import globalVars
import addonHandler

#For translators
try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	log.warning("Unable to initialise translations. This may be because the addon is running from NVDA scratchpad.")

build_year=getattr(versionInfo,'version_year', 2026)

class GPUMonitor:
	def __init__(self):
		self.path = os.path.join(os.path.dirname(__file__), "data", "NVIDIAScript.exe")
		self.running=False
		self.cached_results={}
		self.cache_expiry=1
		self.use_legacy_script=True
		if build_year >= 2026:
			from . import pynvml as _pynvml
			self.pynvml = _pynvml
			log.info(_("NVIDIAMonitor: NVDA 64-bit, using pynvml"))
			self.use_legacy_script=False
		else:
			self.pynvml = None
			log.info(_("NVIDIAMonitor: NVDA version older than 2026.1, using external script"))

	def _format_memory(self, bytes, type):
		type_labels = {
			"free": _("Free memory"),
			"used": _("Used memory"),
			"total": _("Total memory"),
			"used by processes": _("Memory used by processes"),
		}
		label = type_labels.get(type, type)
		if bytes < 2**10:
			return _("{label}: {bytes} B").format(label=label, bytes=bytes)
		elif bytes < 2**20:
			return _("{label}: {bytes:.2f} KB").format(label=label, bytes=bytes / (2**10))
		elif bytes < 2**30:
			return _("{label}: {bytes:.2f} MB").format(label=label, bytes=bytes / (2**20))
		else:
			return _("{label}: {bytes:.2f} GB").format(label=label, bytes=bytes / (2**30))

	def _format_throughput(self, bytes, direction):
		if bytes < 2**20:
			return _("{direction} Throughput: {bytes:.2f} KB/s").format(direction=direction, bytes=bytes / (2**10))
		else:
			return _("{direction} Throughput: {bytes:.2f} MB/s").format(direction=direction, bytes=bytes / (2**20))

	def _get_power_state_description(self, power_state):
		descriptions = {
			0: _("P0 - Maximum performance"),
			1: _("P1 - Very high performance"),
			2: _("P2 - High performance"),
			3: _("P3 - Moderate-high performance"),
			4: _("P4 - Moderate performance"),
			5: _("P5 - Low performance"),
			6: _("P6 - Power saving mode"),
			7: _("P7 - Power saving (intermediate)"),
			8: _("P8 - Idle / very low performance"),
			9: _("P9 - (Undocumented)"),
			10: _("P10 - (Undocumented)"),
			11: _("P11 - (Undocumented)"),
			12: _("P12 - (Undocumented)"),
			13: _("P13 - (Undocumented)"),
			14: _("P14 - (Undocumented)"),
			15: _("P15 - Minimum performance / maximum power saving"),
		}
		return descriptions.get(power_state, 'Unknown')

	def format_script_result(self, command, result):
		result=result.strip()
		if result.startswith("ERROR:"):
			error_msg=_("Failed to get info: {error}").format(error=result[6:])
			self.write_log(error_msg)
			return error_msg
		elif result=="ERROR":
			return _("Error obtaining GPU information")
		if command=="name":
			return _("Name: {res}").format(res=result)
		elif command=="uuid":
			return _("UUID: {res}").format(res=result)
		elif command=="driver_version":
			return _("Driver version: {res}").format(res=result)
		elif command=="load":
			return _("GPU load: {res}%").format(res=result)
		elif command=="memory_load":
			return _("Memory load: {res}%").format(res=result)
		elif command=="memory_free":
			return self._format_memory(int(result), "free")
		elif command=="memory_used":
			return self._format_memory(int(result), "used")
		elif command=="memory_total":
			return self._format_memory(int(result), "total")
		elif command=="temperature":
			return _("Temperature: {res} °C").format(res=result)
		elif command=="power_usage":
			return _("Power consumption: {res} W").format(res=result)
		elif command=="power_limit":
			return _("Power limit: {res} W").format(res=result)
		elif command=="fan_speed":
			return _("Fan speed: {res}%").format(res=result)
		elif command=="cuda_processes":
			return _("CUDA processes: {res}").format(res=result)
		elif command=="process_memory":
			return self._format_memory(int(result), "used by processes")
		elif command=="clock_frequency":
			return _("GPU clock frequency: {res} MHz").format(res=result)
		elif command=="sm_clock_frequency":
			return _("SM clock frequency: {res} MHz").format(res=result)
		elif command=="memory_clock_frequency":
			return _("Memory clock frequency: {res} MHz").format(res=result)
		elif command=="max_clock_frequency":
			return _("Maximum GPU clock frequency: {res} MHz").format(res=result)
		elif command=="max_sm_clock_frequency":
			return _("Maximum SM clock frequency: {res} MHz").format(res=result)
		elif command=="max_memory_clock_frequency":
			return _("Maximum memory clock frequency: {res} MHz").format(res=result)
		elif command=="tx_throughput":
			return self._format_throughput(int(result), "TX")
		elif command=="rx_throughput":
			return self._format_throughput(int(result), "RX")
		elif command=="bios_version":
			return _("BIOS version: {res}").format(res=result)
		elif command=="power_state":
			power_state=int(result)
			return _("Power state: {desc}").format(desc=self._get_power_state_description(power_state))
		else:
			return _("Invalid information type")

	def write_log(self,message):
		log_path=os.path.join(globalVars.appArgs.configPath, "NVIDIAMonitor.log")
		# Must be UTF-8: log messages are translated, and on a system whose
		# code page cannot represent them the write raises UnicodeEncodeError,
		# which aborts execute_command before it ever calls its callback --
		# leaving the user with silence instead of an error announcement.
		with open(log_path, "a", encoding="utf-8") as f:
			current_time=datetime.datetime.now()
			time_format=current_time.strftime("%Y-%m-%d %H:%M")
			f.write(f"{time_format} - {message}\n")

	def run_script(self):
		try:
			self.process = subprocess.Popen(
				[self.path],
				stdin=subprocess.PIPE,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				text=True,
				creationflags=subprocess.CREATE_NO_WINDOW
			)
			self.running=True
			return self.process
		except FileNotFoundError as e:
			self.running=False
			error_path=_("Error: File not found at the specified path: {path}").format(path=self.path)
			self.write_log(error_path)
			log.error(error_path)
			self.process=None
			return self.process
		except subprocess.CalledProcessError as e:
			self.running=False
			error_message=_("Error starting process: {code} {cmd}").format(code=e.returncode, cmd=e.cmd)
			self.write_log(error_message)
			log.error(error_message)
			self.process=None
			return self.process

	def execute_command(self,command,cb):
		if self.use_legacy_script:
			def command_thread():
				current_time=time.monotonic()
				if command in self.cached_results:
					result, timestamp=self.cached_results[command]
					if current_time - timestamp < self.cache_expiry:
						return cb(result)
				if not self.running or self.process.poll() is not None:
					self.run_script()
				try:
					self.process.stdin.write(f"{command}\n")
					self.process.stdin.flush()
					result = self.process.stdout.readline()
					if not result:
						error_result=f"No output received for command: {command}"
						self.write_log(error_result)
						log.error(error_result)
						return cb("Error receiving response from process.")
					#Format raw result from script
					formatted_result=self.format_script_result(command, result)
					#Save result to cache
					self.cached_results[command] = formatted_result, current_time
					return cb(formatted_result)
				except OSError as e:
					error_process=_("Error writing to subprocess: {error}").format(error=e)
					self.write_log(error_process)
					log.error(error_process)
					return cb("Error writing to process.")
			thread=threading.Thread(target=command_thread)
			thread.start()
		else:
			def pynvml_thread():
				try:
					result=self.execute_pynvml(command)
					cb(result)
				except Exception as e:
					error_msg = _("Error executing command with pynvml: {error}").format(error=e)
					log.error(error_msg)
					self.write_log(error_msg)
					cb(_("Error obtaining GPU information"))
			thread=threading.Thread(target=pynvml_thread)
			thread.start()

	def execute_pynvml(self, info_type):
		try:
			self.pynvml.nvmlInit()
			handle = self.pynvml.nvmlDeviceGetHandleByIndex(0)
		except Exception as e:
			log.error(_("Failed to initialize pynvml: {error}").format(error=e))
			return _("Failed to initialize pynvml")
		try:
			if info_type == "name":
				gpu_name = self.pynvml.nvmlDeviceGetName(handle)
				full_name = gpu_name.strip()
				return _("Name: {name}").format(name=full_name)
			elif info_type=="uuid":
				return _("UUID: {uuid}").format(uuid=self.pynvml.nvmlDeviceGetUUID(handle))
			elif info_type=="driver_version":
				return _("Driver version: {ver}").format(ver=self.pynvml.nvmlSystemGetDriverVersion())
			elif info_type == "load":
				utilization = self.pynvml.nvmlDeviceGetUtilizationRates(handle)
				return _("GPU load: {load}%").format(load=utilization.gpu)
			elif info_type=="memory_load":
				memory_utilization=self.pynvml.nvmlDeviceGetUtilizationRates(handle)
				return _("Memory load: {load}%").format(load=memory_utilization.memory)
			elif info_type == "memory_free":
				memory_info = self.pynvml.nvmlDeviceGetMemoryInfo(handle)
				return self._format_memory(memory_info.free, "free")
			elif info_type == "memory_used":
				memory_info = self.pynvml.nvmlDeviceGetMemoryInfo(handle)
				return self._format_memory(memory_info.used, "used")
			elif info_type == "memory_total":
				memory_info = self.pynvml.nvmlDeviceGetMemoryInfo(handle)
				return self._format_memory(memory_info.total, "total")
			elif info_type == "temperature":
				temperature = self.pynvml.nvmlDeviceGetTemperature(
					handle, self.pynvml.NVML_TEMPERATURE_GPU
				)
				return _("Temperature: {temp} °C").format(temp=temperature)
			elif info_type == "power_usage":
				power_usage = self.pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
				return _("Power consumption: {power:.2f} W").format(power=power_usage)
			elif info_type=="power_limit":
				power_limit=self.pynvml.nvmlDeviceGetPowerManagementLimit(handle) / 1000.0
				return _("Power limit: {limit:.2f} W").format(limit=power_limit)
			elif info_type == "fan_speed":
				fan_speed = self.pynvml.nvmlDeviceGetFanSpeed(handle)
				return _("Fan speed: {speed}%").format(speed=fan_speed)
			elif info_type == "cuda_processes":
				cuda_processes = self.pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
				return _("CUDA processes: {count}").format(count=len(cuda_processes))
			elif info_type=="process_memory":
				processes=self.pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
				total_process_memory = 0
				for proc in processes:
					if proc.usedGpuMemory is not None:
						total_process_memory += proc.usedGpuMemory
				return self._format_memory(total_process_memory, "used by processes")
			elif info_type == "clock_frequency":
				clock_graphics_current = self.pynvml.nvmlDeviceGetClockInfo(handle, self.pynvml.NVML_CLOCK_GRAPHICS)
				return _("GPU clock frequency: {clock} MHz").format(clock=clock_graphics_current)
			elif info_type=="sm_clock_frequency":
				clock_sm=self.pynvml.nvmlDeviceGetClockInfo(handle, self.pynvml.NVML_CLOCK_SM)
				return _("SM clock frequency: {clock} MHz").format(clock=clock_sm)
			elif info_type=="memory_clock_frequency":
				clock_memory=self.pynvml.nvmlDeviceGetClockInfo(handle, self.pynvml.NVML_CLOCK_MEM)
				return _("Memory clock frequency: {clock} MHz").format(clock=clock_memory)
			elif info_type=="max_clock_frequency":
				clock_max=self.pynvml.nvmlDeviceGetMaxClockInfo(handle, self.pynvml.NVML_CLOCK_GRAPHICS)
				return _("Maximum GPU clock frequency: {clock} MHz").format(clock=clock_max)
			elif info_type=="max_sm_clock_frequency":
				clock_sm_max=self.pynvml.nvmlDeviceGetMaxClockInfo(handle, self.pynvml.NVML_CLOCK_SM)
				return _("Maximum SM clock frequency: {clock} MHz").format(clock=clock_sm_max)
			elif info_type=="max_memory_clock_frequency":
				clock_memory_max=self.pynvml.nvmlDeviceGetMaxClockInfo(handle, self.pynvml.NVML_CLOCK_MEM)
				return _("Maximum memory clock frequency: {clock} MHz").format(clock=clock_memory_max)
			elif info_type=="tx_throughput":
				tx=self.pynvml.nvmlDeviceGetPcieThroughput(handle, self.pynvml.NVML_PCIE_UTIL_TX_BYTES)
				return self._format_throughput(tx, "TX")
			elif info_type=="rx_throughput":
				rx=self.pynvml.nvmlDeviceGetPcieThroughput(handle, self.pynvml.NVML_PCIE_UTIL_RX_BYTES)
				return self._format_throughput(rx, "RX")
			elif info_type=="bios_version":
				bios_version=self.pynvml.nvmlDeviceGetVbiosVersion(handle)
				return _("BIOS version: {ver}").format(ver=bios_version)
			elif info_type=="power_state":
				power_state=self.pynvml.nvmlDeviceGetPowerState(handle)
				return _("Power state: {desc}").format(desc=self._get_power_state_description(power_state))
			else:
				return _("Invalid information type")
		finally:
			try:
				self.pynvml.nvmlShutdown()
			except Exception as e:
				log.error(_("Error closing pynvml: {error}").format(error=e))
				pass

	def terminate(self):
		if build_year < 2026:
			if self.process:
				if self.process.poll() is not None:
					self.running=False
					return
				try:
					# Send exit command
					self.process.stdin.write("exit\n")
					self.process.stdin.flush()
					#Terminate process in controlled manner
					self.process.terminate()
					# Wait for complete termination
					self.process.wait()
					# Close stdin, stdout, stderr connections
					self.process.stdin.close()
					self.process.stdout.close()
					self.process.stderr.close()
					self.running=False
				except Exception as e:
					error_terminate=_("Error attempting to terminate process: {error}").format(error=str(e))
					self.write_log(error_terminate)
					pass
