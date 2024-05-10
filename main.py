import requests
from bs4 import BeautifulSoup
import csv
import datetime
import time
import smtplib
import pandas as pd

product_url = 'https://www.amazon.com.tr/Kahve-D%C3%BCnyas%C4%B1-Bitter-Gofrik-24l%C3%BC/dp/B074PT2HZ8/ref=sr_1_5?__mk_tr_TR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&sr=8-5'
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
response = requests.get(product_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

product_name = soup.find("span", attrs={"id": 'productTitle'}).text.strip()
product_price = soup.find("span", attrs={"class": 'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'}).text.strip()
product_star = soup.find("a", attrs={"class": 'a-popover-trigger a-declarative'}).find("span", attrs={"class": 'a-size-base a-color-base'}).text.strip()
product_review = soup.find("span", attrs={"id": 'acrCustomerReviewText'}).text.strip()

def get_info(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(f"{product_name}")
    return "Ürün adı:", product_name,"Ürün fiyatı:", product_price,"Ürün 5 Üzerinden Puanı:", product_star,"Ürünün değerlendirme sayısı:", product_review

    
def check_price(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    header = ['Title','Price','Date']
    today = datetime.date.today()
    data = [product_name,product_price,today]

    with open ('AmazonWebScraperDataset.csv','a+',newline="", encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    
    df = pd.read_csv(r'D:\School\fourth year second semester\Web Mining\Web Mining Project\AmazonWebScraperDataset.csv')
    print(df)
    

def discount_alert(product_url, threshold):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    current_price_str = product_price.replace('₺', '').replace(',', '').replace('TL', '').strip()  # '₺' sembolünü, virgülü ve 'TL' metnini kaldırın
    current_price = float(current_price_str)

    # İndirim kontrolü
    discount_threshold = threshold  # Belirlenen eşik değeri
    original_price = 100.0  # Orjinal fiyat (örneğin)
    discount_amount = original_price - current_price
    discount_percent = (discount_amount / original_price) * 100

    if discount_percent >= discount_threshold:
        send_mail()
        print("İndirim algılandı! İndirim Oranı: {}%".format(discount_percent))
    else:
        print("Henüz indirim yok.")

    return discount_percent

def send_mail():
    # E-posta gönderen ve alıcının e-posta adreslerini belirtin
    sender_email = "byzylmzr1@gmail.com"
    receiver_email = "gulsenbeyzayilmazer@posta.mu.edu.tr"

    # E-posta başlığını ve içeriğini belirtin
    subject = "Amazon Ürün İndirim Uyarısı"
    body = "İndirim algılandı! İlgili üründe %10'dan fazla bir indirim bulunmaktadır."

    # Gmail SMTP sunucusuna bağlanın
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()

    # E-posta göndermek için Gmail hesabınızın kimlik bilgilerini kullanarak oturum açın
    server.login("byzylmzr1@gmail.com", "xxxxx")

    # E-posta başlığını ve içeriğini birleştirin
    message = f"Subject: {subject}\n\n{body}"

    # E-postayı gönderin
    server.sendmail(sender_email, receiver_email, message)

    # SMTP oturumunu kapatın
    server.quit()

    print("E-posta gönderildi!")
    
def compare_product(product_url):
    compare_product_url = 'https://www.trendyol.com/kahve-dunyasi/gofrik-sutlu-24-lu-p-3674870'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    response = requests.get(compare_product_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    compare_product_name = soup.find("a", attrs={"class": 'product-brand-name-with-link'}).text.strip()
    compare_product_price = soup.find("div", attrs={"class": 'pr-bx-nm with-org-prc'}).text.strip()
   
    if product_price == compare_product_price:
        print("İki ürün aynı fiyata sahip.")
    elif product_price < compare_product_price:
        print(f"{product_name} daha UCUZ. Fiyatı: {product_price} TL")
        print(f"{compare_product_name} daha PAHALI. Fiyatı: {compare_product_price} TL")
    else:
        print(f"{compare_product_name} daha UCUZ. Fiyatı: {compare_product_price} TL")
        print(f"{product_name} daha PAHALI. Fiyatı: {product_price} TL")

    
def menu():
    while True:
        print("\nAna Menü:")
        print("1. Ürün Bilgisi Al")
        print("2. Fiyatı Kontrol Et")
        print("3. İndirim Uyarısı Ayarla")
        print("4. Benzer Ürün Fiyatı Karşılaştır")
        print("5. Çıkış")

        choice = input("Lütfen bir seçenek seçin: ")

        if choice == "1":
            get_info(product_url)
        elif choice == "2":
            check_price(product_url)
        elif choice == "3":
            threshold_str = input("İndirim eşiği değerini girin (%): ")
            threshold = float(threshold_str.rstrip('%'))  # Yüzde işaretini kaldırın ve ardından dönüştürün
            discount_alert(product_url, threshold)
        elif choice == "4":
            compare_product(product_url)
        elif choice == "5":
            print("Programdan çıkılıyor...")
            break
        else:
            print("Geçersiz bir seçenek. Lütfen tekrar deneyin.")

menu()

