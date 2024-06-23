import pyautogui
import dearpygui.dearpygui as dpg
import threading
import time

scriptStatus = "OFF"
status_lock = threading.Lock()  # Lock for synchronizing access to scriptStatus

def resize_button(sender, app_data):
    window_width = dpg.get_item_width("pWindow")
    window_height = dpg.get_item_height("pWindow")
    
    dpg.set_item_width("scriptButton", window_width)
    dpg.set_item_height("scriptButton", window_height)

def changeStatus(sender, data):
    global scriptStatus  # Declare scriptStatus as global to modify it
    with status_lock:
        if scriptStatus == "OFF":
            scriptStatus = "ON"
        else:
            scriptStatus = "OFF"
    dpg.set_item_label("scriptButton", "Script: " + scriptStatus)  # Update button label
    print(f"Script status changed to: {scriptStatus}")

dpg.create_context()
dpg.create_viewport(title="League Auto Accept", width=600, height=300)
with dpg.window(tag="pWindow", label="Script Toggle", width=600, height=300):
    button_item = dpg.add_button(label="Script: " + scriptStatus, tag="scriptButton", callback=changeStatus)
    dpg.add_text("Status: Waiting...", tag="statusLabel")

def auto_accept_script():
    while True:
        with status_lock:
            if scriptStatus == "ON":
                try:
                    acceptlocation = pyautogui.locateCenterOnScreen('acceptbutton.png', confidence=0.5)
                    if acceptlocation is not None:
                        pyautogui.moveTo(acceptlocation.x, acceptlocation.y)
                        time.sleep(1)
                        pyautogui.leftClick()
                        time.sleep(1)
                        pyautogui.leftClick()
                        dpg.set_item_label("Accept button found.")
                    else:
                        dpg.set_item_label("Accept button not found.")
                except Exception as e:
                    dpg.set_item_label("statusLabel", "None Found")
        time.sleep(1)  # Add a delay to reduce CPU usage

def update_button_label():
    while True:
        with status_lock:
            dpg.set_item_label(button_item, "Script: " + scriptStatus)
        time.sleep(0.1)  # Adjust the sleep time as needed for responsiveness

# Start the auto accept script in a separate thread
auto_accept_thread = threading.Thread(target=auto_accept_script, daemon=True)
auto_accept_thread.start()

# Start a thread to continuously update the button label
update_label_thread = threading.Thread(target=update_button_label, daemon=True)
update_label_thread.start()

dpg.set_viewport_resize_callback(resize_button)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("pWindow", True)

dpg.start_dearpygui()
dpg.destroy_context()
