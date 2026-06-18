import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class MasaJavaClassicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MASA iOS Control Center - Java Desktop Edition")
        self.root.geometry("640x500")
        self.root.configure(bg="#e0e0e0")  # رمادي جافا القياسي (Java Swing System Background)
        self.root.resizable(False, False)

        self.current_product_type = "Unknown"

        # ضبط الستايل الكلاسيكي لشريط التحميل ليطابق نمط الجافا
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Java.Horizontal.TProgressbar", 
                        troughcolor="#d0d0d0", 
                        background="#000080",  # كحلي كلاسيكي للتحميل
                        thickness=8,
                        bordercolor="#e0e0e0")

        # 1. شريط العنوان العلوي (Java Menu System Style)
        header_frame = tk.Frame(root, bg="#ebebeb", height=45, bd=1, relief=tk.RAISED)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text=" MASA iOS Service Tool [Java Framework]", font=("Dialog", 11, "bold"), fg="#000000", bg="#ebebeb")
        title_label.pack(side=tk.LEFT, padx=10, pady=10)

        subtitle_label = tk.Label(header_frame, text="Build v9.5 (Stable) ", font=("Dialog", 9), fg="#444444", bg="#ebebeb")
        subtitle_label.pack(side=tk.RIGHT, padx=15, pady=12)

        # 2. شريط الأزرار السفلي (Java Toolbar Style)
        toolbar_frame = tk.Frame(root, bg="#ebebeb", height=65, bd=1, relief=tk.RAISED)
        toolbar_frame.pack(fill=tk.X, side=tk.BOTTOM)
        toolbar_frame.pack_propagate(False)

        # إعدادات أزرار الجافا الصلبة (خلفية بيضاء، خط أسود، حدود بارزة كلاسيكية)
        java_btn_config = {
            "font": ("Dialog", 11, "bold"),
            "fg": "#000000",
            "bg": "#ffffff",
            "activeforeground": "#ffffff",
            "activebackground": "#000080",
            "highlightbackground": "#ebebeb", 
            "bd": 2,
            "relief": tk.GROOVE,  # يعطي تضليلاً كلاسيكياً صلبًا مثل الجافا
            "cursor": "hand2",
            "width": 14,
            "height": 1
        }

        # المفتاح الأول: Detect Device
        self.detect_btn = tk.Label(toolbar_frame, text="Detect Device", **java_btn_config)
        self.detect_btn.pack(side=tk.LEFT, padx=(20, 5), pady=12)
        self.detect_btn.bind("<Button-1>", lambda e: self.start_loading("detect"))
        self.add_java_hover(self.detect_btn)

        # المفتاح الثاني: Active Status
        self.active_btn = tk.Label(toolbar_frame, text="Active Status", **java_btn_config)
        self.active_btn.pack(side=tk.LEFT, padx=5, pady=12)
        self.active_btn.bind("<Button-1>", lambda e: self.start_loading("active"))
        self.add_java_hover(self.active_btn)

        # المفتاح الثالث: Reboot Device
        self.reboot_btn = tk.Label(toolbar_frame, text="Reboot Device", **java_btn_config)
        self.reboot_btn.pack(side=tk.RIGHT, padx=20, pady=12)
        self.reboot_btn.bind("<Button-1>", lambda e: self.reboot_device())
        self.add_java_hover(self.reboot_btn)

        # 3. شريط الحالة والتحميل (Status Bar)
        self.progress_frame = tk.Frame(root, bg="#e0e0e0", bd=1, relief=tk.FLAT)
        self.progress_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=(5, 5))
        
        self.progress_label = tk.Label(self.progress_frame, text="Status: Thread execution ready.", font=("Dialog", 9), fg="#333333", bg="#e0e0e0")
        self.progress_bar = ttk.Progressbar(self.progress_frame, style="Java.Horizontal.TProgressbar", orient="horizontal", mode="determinate", length=580)

        # 4. الصندوق النصي المحفور (Sunken Java Console Area)
        self.console_frame = tk.Frame(root, bg="#e0e0e0", padx=15, pady=10)
        self.console_frame.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        # الحواف SUNKEN تعطي الصندوق عمقاً قوياً داخل الشاشة البيضاء
        self.output_box = tk.Text(self.console_frame, bg="#ffffff", fg="#000000", font=("Monospaced", 11, "bold"), bd=2, relief=tk.SUNKEN, padx=12, pady=12)
        self.output_box.pack(fill=tk.BOTH, expand=True)
        
        self.log_to_console(">> MASA Core Initialized Engine...\n>> Ready for connection.\n>> Connect an iOS device via USB and click 'Detect Device'...")
        self.output_box.config(state=tk.DISABLED)

    def add_java_hover(self, widget):
        # تفتيح وتغميق ذكي متوافق مع نمط أزرار الجافا الكلاسيكية
        widget.bind("<Enter>", lambda e: widget.config(bg="#e6e6e6", relief=tk.RAISED))
        widget.bind("<Leave>", lambda e: widget.config(bg="#ffffff", relief=tk.GROOVE))

    def log_to_console(self, text):
        self.output_box.config(state=tk.NORMAL)
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, text)
        self.output_box.config(state=tk.DISABLED)

    def start_loading(self, action_type):
        self.output_box.config(state=tk.NORMAL)
        self.output_box.delete("1.0", tk.END)
        self.output_box.config(state=tk.DISABLED)
            
        self.progress_label.pack(anchor="w", pady=2)
        self.progress_bar.pack(fill=tk.X)
        self.progress_bar['value'] = 0
        self.animate_progress(0, action_type)

    def animate_progress(self, current_val, action_type):
        if current_val <= 100:
            self.progress_bar['value'] = current_val
            self.root.after(8, lambda: self.animate_progress(current_val + 5, action_type))
        else:
            self.progress_bar.pack_forget()
            self.progress_label.pack_forget()
            if action_type == "detect":
                self.get_device_detection()
            elif action_type == "active":
                self.get_activation_info()

    def run_idevice_command(self):
        raw_info = subprocess.check_output(["ideviceinfo"], stderr=subprocess.STDOUT).decode("utf-8")
        device_data = {}
        for line in raw_info.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                device_data[key.strip()] = value.strip()
        return device_data

    def get_marketing_name(self, product_type):
        models = {
            "iPhone8,1": "iPhone 6s", "iPhone8,2": "iPhone 6s Plus", "iPhone8,4": "iPhone SE (1st Gen)",
            "iPhone9,1": "iPhone 7 (CDMA)", "iPhone9,3": "iPhone 7 (GSM)", "iPhone9,2": "iPhone 7 Plus (CDMA)", "iPhone9,4": "iPhone 7 Plus (GSM)",
            "iPhone10,1": "iPhone 8", "iPhone10,4": "iPhone 8", "iPhone10,2": "iPhone 8 Plus", "iPhone10,5": "iPhone 8 Plus",
            "iPhone10,3": "iPhone X", "iPhone10,6": "iPhone X", "iPhone11,2": "iPhone XS", "iPhone11,4": "iPhone XS Max",
            "iPhone11,6": "iPhone XS Max", "iPhone11,8": "iPhone XR", "iPhone12,1": "iPhone 11", "iPhone12,3": "iPhone 11 Pro",
            "iPhone12,5": "iPhone 11 Pro Max", "iPhone12,8": "iPhone SE (2nd Gen)", "iPhone13,1": "iPhone 12 mini", "iPhone13,2": "iPhone 12",
            "iPhone13,3": "iPhone 12 Pro", "iPhone13,4": "iPhone 12 Pro Max", "iPhone14,4": "iPhone 13 mini", "iPhone14,5": "iPhone 13",
            "iPhone14,2": "iPhone 13 Pro", "iPhone14,3": "iPhone 13 Pro Max", "iPhone14,6": "iPhone SE (3rd Gen)", "iPhone14,7": "iPhone 14",
            "iPhone14,8": "iPhone 14 Plus", "iPhone15,2": "iPhone 14 Pro", "iPhone15,3": "iPhone 14 Pro Max", "iPhone15,4": "iPhone 15",
            "iPhone15,5": "iPhone 15 Plus", "iPhone16,1": "iPhone 15 Pro", "iPhone16,2": "iPhone 15 Pro Max", "iPhone17,1": "iPhone 16",
            "iPhone17,2": "iPhone 16 Plus", "iPhone17,3": "iPhone 16 Pro", "iPhone17,4": "iPhone 16 Pro Max"
        }
        return models.get(product_type, f"Unknown Device ({product_type})")

    def get_device_detection(self):
        try:
            device_data = self.run_idevice_command()
            product_type = device_data.get("ProductType", "Unknown")
            product_version = device_data.get("ProductVersion", "Unknown")
            serial = device_data.get("SerialNumber", "Unknown")
            model_name = self.get_marketing_name(product_type)
            
            is_jailbroken = "No (Official)"
            if "PasswordProtected" in device_data and device_data.get("CanAcceptSJConnection", "") == "true":
                is_jailbroken = "Yes (Jailbroken)"

            report = (
                f"[ JAVA DETECTION REPORT ]\n"
                f"----------------------------------------\n"
                f"Device Model  : {model_name}\n"
                f"iOS Version   : iOS {product_version}\n"
                f"Serial Number : {serial}\n"
                f"Jailbreak     : {is_jailbroken}\n"
                f"----------------------------------------\n"
                f"Status        : Success. Thread closed."
            )
            self.log_to_console(report)

        except Exception:
            self.show_connection_error()

    def get_activation_info(self):
        try:
            device_data = self.run_idevice_command()
            product_type = device_data.get("ProductType", "Unknown")
            model_name = self.get_marketing_name(product_type)
            activation_state = device_data.get("ActivationState", "Unknown")

            report = (
                f"[ JAVA ACTIVATION REPORT ]\n"
                f"----------------------------------------\n"
                f"Device Model  : {model_name}\n"
                f"Active Status : {activation_state.upper()}\n"
                f"----------------------------------------\n"
                f"Status        : Process completed successfully."
            )
            self.log_to_console(report)

        except Exception:
            self.show_connection_error()

    def show_connection_error(self):
        err_msg = (
            f"[ JAVA RUNTIME EXCEPTION: Device Not Found ]\n"
            f"----------------------------------------\n"
            f"1. Verify USB hardware link layer.\n"
            f"2. Ensure iOS screen lock lockscreen is open.\n"
            f"3. Press 'Trust Computer' prompt interactive popup.\n"
            f"----------------------------------------"
        )
        self.log_to_console(err_msg)

    def reboot_device(self):
        if messagebox.askyesno("Java Runtime Prompt", "Execute hardware system restart signal?"):
            try:
                subprocess.Popen(["idevicediagnostics", "restart"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.log_to_console("[ SYSTEM LOG ]\n----------------------------------------\nReboot command sent to the iOS device.")
            except FileNotFoundError:
                messagebox.showerror("Java Runtime Error", "Binary dependencies missing.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MasaJavaClassicApp(root)
    root.mainloop()