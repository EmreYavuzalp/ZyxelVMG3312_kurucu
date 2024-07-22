import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from tkinter import ttk
from tkinter import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By 
from tkinter import messagebox
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
chromedriver_path = os.path.join(script_dir, 'chromedriver.exe')

# Initialize WebDriver
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service)

ssidad = None
sifrewifi2 = None

girilenKullaniciAdi = None
girilenSifre = None

def submit():
    global girilenKullaniciAdi, girilenSifre
    girilenKullaniciAdi = username_entry.get()
    girilenSifre = password_entry.get()
    print(f"Username: {girilenKullaniciAdi}")
    print(f"Password: {girilenSifre}")
    driver.get("http://192.168.1.1")

    username_field = driver.find_element(By.ID, "AuthName")
    password_field = driver.find_element(By.ID, "AuthPassword")
    
    # Kullanıcı adı her zaman admin
    username = "admin"
    password_attempts = ["ttnet", "turktelekom"]

    for password in password_attempts:
        try:
            # Kullanıcı adı ve şifreyi gir
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)
            # Kısa bir süre bekle
            driver.implicitly_wait(1)

            # Başarılı giriş kontrolü
            try:
                atla_button = driver.find_element(By.XPATH, "//input[@value='Atla']")
                atla_button.click()
                print("Giriş başarılı ve 'Atla' butonuna basıldı.")
                break  # Şifre doğru, döngüden çık
            except NoSuchElementException:
                print("Şifre ttnet değil, turktelekom denenecek")
                
                # AuthName ID'li element var mı kontrol et
                try:
                    auth_name_field = driver.find_element(By.ID, "AuthName")
                    print("username fieldi var mı?")
                    if auth_name_field:
                        print("AuthName alanı bulundu, tekrar giriş yapılıyor...")
                        auth_name_field.clear()
                        auth_name_field.send_keys(username)
                        
                        auth_password_field = driver.find_element(By.ID, "AuthPassword")
                        auth_password_field.clear()
                        auth_password_field.send_keys("turktelekom")
                        auth_password_field.send_keys(Keys.RETURN)

                        # Tekrar 'Atla' butonunu kontrol et
                        driver.implicitly_wait(1)
                        atla_button = driver.find_element(By.XPATH, "//input[@value='Atla']")
                        atla_button.click()
                        print("Giriş başarılı ve 'Atla' butonuna basıldı.")
                        break  # Şifre doğru, döngüden çık
                except NoSuchElementException:
                    print("AuthName alanı bulunamadı, giriş başarısız.")
                    continue  # Diğer şifreyi dene

        except NoSuchElementException:
            print(f"Şifre '{password}' yanlış, diğer şifreyi dene.")
            continue  # Diğer şifreyi dene
    
    time.sleep(15)        
    a = ActionChains(driver)

    m = driver.find_element(By.LINK_TEXT,"Ağ Ayarı")
    a.move_to_element(m).perform()

    m2 = driver.find_element(By.LINK_TEXT,"Genişbant").click()
    time.sleep(2)
    #genişbanta tıkladıktan sonra mainFrame
    driver.switch_to.frame("mainFrame")


    print("main frame e geçildi")
        # Find the table by its ID
    table = driver.find_element(By.ID, 'boradbandTable')
    print("tablo taranıyor")

        # Find all rows in the table body
    rows = table.find_elements(By.TAG_NAME, 'tr')
    print("tr ler taranıyor")
        # Iterate over rows to find the one that contains "VDSL"
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        print("td ler taranıyor")
        for cell in cells:
            if cell.text == 'Internet_DSL':
                    # Find the edit button in the same row
                edit_button = row.find_element(By.CLASS_NAME, 'edit')
                    # Click the edit button
                edit_button.click()
                break
    driver.switch_to.default_content()

    # Wait for the element to be present using the ID
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'PPP_name_other_ISP_click'))
        )
    # Click the element
        element.click()
        print("Element clicked successfully")
    except:
        print("Timeout waiting for the element to be present or it was not found")
    #başka operatör kısmı tıklandı.


        
    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'sysPPPUsernameFull'))
        )
        time.sleep(0.5)
        username_field.clear()
        time.sleep(0.5)
        username_field.send_keys(girilenKullaniciAdi)
        print("Username entered successfully")
    except:
        print("Timeout waiting for the username field to be present or it was not found")

# Wait for the password input field to be present and enter "12345678"
    try:
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'sysPPPPwd'))
        )
        time.sleep(0.5)
        password_field.clear()
        time.sleep(0.5)
        password_field.send_keys(girilenSifre)
        print("Password entered successfully")
    except:
        print("Timeout waiting for the password field to be present or it was not found")

# Wait for the "Uygula" button to be present and click it
    try:
        apply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Uygula']"))
        )
        apply_button.click()
        print("Uygula button clicked successfully")
    except:
        print("Timeout waiting for the Uygula button to be clickable or it was not found")





warning_text2 = (
        "Buradaki kullanıcı adı ve şifre admin ve ttnet değildir!!! Bu internet kullanıcı adı ve şifresidir."
	" Eğer internet servis sağlayıcınız Türktelekom ise, 4440375 i arayıp, teknik destek almak istiyorum"
	" kısmından, internet kullanıcı adı ve şifremi almak istiyorum olan numaraya basabilirsiniz."
	" Daha sonra, kullanıcı adı ve şifreniz hat sahibine SMS olarak iletilecektir. Bunun yerine"
	" direkt olarak müşteri temsilcisiyle görüşebilirsiniz. Türknet için ise online işlem"
	" merkezinde yazmaktadır. BÜYÜK KÜÇÜK HARF ÖNEMLİDİR. LÜTFEN DİKKAT EDİNİZ!"
        " ÖNEMLİ NOT: Kur tuşuna bastıktan sonra işlem bitene kadar müdahale etmeyiniz."
        " Eğer program çalışmazsa, en son chrome sürümüne güncelleyiniz, Windows 10 ve üstü için çalışmaktadır."
    )
    



    
# Create the main window
master = tk.Tk()
master.title('Zyxel VMG3312-B10B Kurulum Programı v1.0')

# Create and place username label and entry
tk.Label(master, text="Username").grid(row=0, column=0, pady=2)
username_entry = tk.Entry(master)
username_entry.grid(row=0, column=1, padx=10, pady=10)

# Create and place password label and entry
tk.Label(master, text="Password").grid(row=1, column=0, pady=2)
password_entry = tk.Entry(master)  # show="*" hides the password text
password_entry.grid(row=1, column=1, pady=2)

# Warning text

# Create and place warning label
warning_label = tk.Label(master, text=warning_text2, padx=10, pady=10, wraplength=380, justify="left")
warning_label.grid(row=3, column=0, columnspan=2, pady=10)

# Create and place submit button
submit_button = tk.Button(master, text="Kur", command=submit)
submit_button.grid(row=4, column=0, columnspan=2, pady=2)

# Start the Tkinter event loop
master.mainloop()
