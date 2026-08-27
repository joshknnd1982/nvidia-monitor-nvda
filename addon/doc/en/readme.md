# NVIDIA Monitor

This add-on allows you to monitor various parameters of NVIDIA graphics cards, such as name, used memory, free and total memory, power usage, temperature, and more.

## Shortcuts

Note: Some information parameters may not be compatible or supported depending on the graphics card.
All the following shortcuts can be customized in the input gestures/NVDIAMonitor category. Pressing a shortcut twice copies the information to the clipboard.

- NVDA + alt + g: Announces the GPU name/model.
- NVDA + alt + u: Announces the GPU UUID.
- NVDA + alt + v: Announces the driver version.
- NVDA + ctrl + alt + v: Announces the BIOS version.
- NVDA + alt + 1: Announces the GPU load.
- NVDA + alt + 2: Announces the memory load.
- NVDA + alt + 3: Announces the free memory.
- NVDA + alt + 4: Announces the used memory.
- NVDA + alt + 5: Announces the total memory.
- NVDA + alt + 6: Announces the GPU temperature.
- NVDA + alt + 7: Announces the power consumption.
- NVDA + alt + 8: Announces the power limit.
- NVDA + alt + 9: Announces the number of CUDA processes.
- NVDA + alt + 0: Announces the memory used by processes.
- NVDA + ctrl + alt + 1: Announces the fan speed.
- NVDA + ctrl + alt + 2: Announces the GPU clock frequency.
- NVDA + ctrl + alt + 3: Announces the maximum GPU clock frequency.
- NVDA + ctrl + alt + 4: Announces the SM clock frequency.
- NVDA + ctrl + alt + 5: Announces the maximum SM clock frequency.
- NVDA + ctrl + alt + 6: Announces the memory clock frequency.
- NVDA + ctrl + alt + 7: Announces the maximum memory clock frequency.
- NVDA + ctrl + alt + 8: Announces the TX throughput.
- NVDA + ctrl + alt + 9: Announces the RX throughput.
- NVDA + ctrl + alt + 0: Announces the power state.


## Changelog

### Version 2.1.1

- Added a Russian translation.
- Fixed an error that could stop a message being announced at all, instead of
  being spoken, when the add-on reported a problem in a language whose
  characters the system code page cannot represent.

### Version 2.0

- Compatibility with NVDA 2026.1.
- Starting with this version, the add-on makes calls directly to the pynvml library instead of using an external tool, when running on the latest version of NVDA.

### Version 1.0

- Several changes, fixes, and improvements were made to the information retrieval script.
- Errors are now logged to a file called NVIDIAMonitor.log located in the NVDA configuration folder.
- Compatibility with NVDA 2025.1.
- Some existing shortcuts were reassigned.
- New shortcuts added:
  - GPU UUID: NVDA + alt + u
  - Driver version: NVDA + alt + v
  - BIOS version: NVDA + ctrl + alt + v
  - Memory load: NVDA + alt + 2
  - Power limit: NVDA + alt + 8
  - Memory used by processes: NVDA + alt + 0
  - Maximum GPU clock frequency: NVDA + ctrl + alt + 3
  - SM clock frequency: NVDA + ctrl + alt + 4
  - Maximum SM clock frequency: NVDA + ctrl + alt + 5
  - Memory clock frequency: NVDA + ctrl + alt + 6
  - Maximum memory clock frequency: NVDA + ctrl + alt + 7
  - TX throughput: NVDA + ctrl + alt + 8
  - RX throughput: NVDA + ctrl + alt + 9
  - Power state: NVDA + ctrl + alt + 0

### Version 0.2

- Pressing a shortcut twice now copies the information to the clipboard.
- Various improvements and optimizations.

### Version 0.1

- Initial version of the add-on.
