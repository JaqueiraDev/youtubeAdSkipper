import threading
from tkinter import StringVar
import customtkinter as ctk
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
import time

running = False
list_log = []
driver = None
count = 0


def run_program():
    global driver, count
    opt = webdriver.ChromeOptions()
    opt.add_argument('--user-data-dir=/Users/ajaqueira/Library/Application Support/Google/Chrome/Default')
    driver = webdriver.Chrome(options=opt)
    driver.implicitly_wait(0.5)
    driver.maximize_window()
    web_url = 'https://www.youtube.com/'
    driver.get(web_url)
    wait = ui.WebDriverWait(driver, 3000)

    while running:
        button_xpath = (
            '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/di'
            'v/ytd-player/div/div/div[20]/div/div[3]/div/div[2]/span/button/div')
        try:
            if EC.presence_of_element_located((By.XPATH, button_xpath)):
                button = driver.find_element(By.XPATH, button_xpath)
                driver.execute_script('arguments[0].click();', button)
                list_log.append('Ad Skipped!')
                print('Ad Skipped!')
                add_to_scrollable()
                time.sleep(2)
            else:
                continue
        except NoSuchElementException:
            list_log.clear()
            list_log.append("********************  Waiting  ********************")
            print("Waiting...")
            add_to_scrollable()
            time.sleep(2)
    driver.quit()
    driver = None


window = ctk.CTk()
screen_w, screen_h = 700, 800
window.title('Youtube Ad skipper')
window.geometry(f'{screen_w}x{screen_h}')

button_label = StringVar()
button_label.set('Start')


def on_button_click():
    global running
    if not running:
        button_label.set('Stop')
        running = True
        threading.Thread(target=run_program).start()
    else:
        button_label.set('Start')
        running = False


def add_to_scrollable():
    for lb in list_log:
        label = ctk.CTkLabel(scrollable_frame, text=lb, font=ctk.CTkFont(size=20, weight='bold'))
        label.pack()


lbl = ctk.CTkLabel(window, text='Press start to open youtube and skip ads!', font=ctk.CTkFont(size=25, weight='bold'))
lbl.pack(padx=10, pady=(40, 20))

scrollable_frame = ctk.CTkScrollableFrame(window, width=screen_w - 100, height=screen_h - 300)
scrollable_frame.pack(pady=40)

start_button = ctk.CTkButton(window, textvariable=button_label, width=100, command=on_button_click)
start_button.pack(pady=20)

window.mainloop()
