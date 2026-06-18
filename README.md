# MASA iOS Service Tool

A lightweight, powerful, and robust desktop utility designed for iOS device management and diagnostics. Built with a pure classic Java-style framework, this tool provides a highly responsive, streamlined interface for developers and technicians working with iOS devices on macOS.

---

## 🛠️ Features

* **Device Detection (`Detect Device`):** Instantly fetches vital hardware information including marketing device model, current iOS version, hardware Serial Number, and active jailbreak integrity status.
* **Activation Status (`Active Status`):** Queries and reports the device's exact server-side activation state directly to the standalone text console area.
* **iCloud Activation Lock Bypass (New):** Built-in automation framework to securely bypass iCloud Activation Lock screens on supported checkmearm/checkra1n-compatible devices.
* **Hardware Reboot (`Reboot Device`):** Safely transmits a raw hardware-level restart signal sequence to the connected target device.
* **Java Desktop Layout:** Robust industrial gray theme featuring high-contrast white action buttons, crisp bold monospace fonts, and double-bevel border components for absolute retro UI stability.

---

## 📋 System Requirements & Dependencies

To ensure core threads and low-level subsystem communications execute successfully, your Mac must have the following open-source dependencies installed via `Homebrew`:

```bash
# Install native iOS USB communication protocol libraries
brew install libimobiledevice
brew install usbmuxd
