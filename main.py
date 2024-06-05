import requests
from bs4 import BeautifulSoup
import csv
import datetime
import time
import smtplib
import pandas as pd

product_url = 'https://www.amazon.com.tr/%C3%9Clker-%C3%87ikolatal%C4%B1-Gofret-36Gr-Adet/dp/B08X6WYHP3/ref=sr_1_5?__mk_tr_TR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&sr=8-5'
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
response = requests.get(product_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

product_name = soup.find("span", attrs={"id": 'productTitle'}).text.strip()
product_price_elem = soup.find("span", attrs={"class": 'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})
product_star = soup.find("a", attrs={"class": 'a-popover-trigger a-declarative'}).find("span", attrs={"class": 'a-size-base a-color-base'}).text.strip()
product_review = soup.find("span", attrs={"id": 'acrCustomerReviewText'}).text.strip()

if product_price_elem:
    product_price = product_price_elem.text.strip()
else:
    product_price = "Fiyat bilgisi bulunamadı."

def get_product_info(product_url):
    return product_name, product_price, product_star, product_review

def check_price(product_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_price_elem = soup.find("span", attrs={"class": 'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})
    
    if product_price_elem:
        product_price = product_price_elem.text.strip()
    else:
        product_price = "Fiyat bilgisi bulunamadı."

    header = ['Title','Price','Date']
    today = datetime.date.today()
    data = [product_name,product_price,today]

    with open (r'D:\School\fourth year second semester\Web Mining\Amazon Web Scraping\AmazonWebScraperDataset.csv', 'a+', newline="", encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    
    df = pd.read_csv(r'D:\School\fourth year second semester\Web Mining\Amazon Web Scraping\AmazonWebScraperDataset.csv')
    print(df)

    return product_price, None  # product_price döndürülüyor, ancak product_price_tag döndürülmüyor

def discount_alert(product_url, product_price_elem, threshold):
    current_price_str = product_price.replace('₺', '').replace(',', '').replace('TL', '').strip()
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

def compare_product(product_url,product_price):
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
    product_price = None  # Başlangıçta product_price değerini None
    product_price_tag = None  # product_price_tag'i None olarak tanımlayın
    while True:
        print("\nAna Menü:")
        print("1. Ürün Bilgisi Al")
        print("2. Fiyatı Kontrol Et")
        print("3. İndirim Uyarısı Ayarla")
        print("4. Benzer Ürün Fiyatı Karşılaştır")
        print("5. Çıkış")

        choice = input("Lütfen bir seçenek seçin: ")

        if choice == "1":
            product_name, product_price, product_star, product_review = get_product_info(product_url)
            print(f"Ürün adı: {product_name}")
            print(f"Ürün fiyatı: {product_price}")
            print(f"Ürün 5 Üzerinden Puanı: {product_star}")
            print(f"Ürünün değerlendirme sayısı: {product_review}")
        elif choice == "2":
            product_price, product_price_tag = check_price(product_url)
        elif choice == "3":
            if product_price_tag is not None:  # product_price_tag değeri None değilse discount_alert fonksiyonunu çağırın
                threshold_str = input("İndirim eşiği değerini girin (%): ")
                threshold = float(threshold_str.rstrip('%'))  # Yüzde işaretini kaldırın ve ardından dönüştürün
                discount_alert(product_url, product_price_tag, threshold)
            else:
                print("Önce ürün fiyatını kontrol etmelisiniz!")
        elif choice == "4":
            if product_price is not None:  # product_price değeri None değilse compare_product fonksiyonunu çağırın
                compare_product(product_url, product_price)
            else:
                print("Önce ürün fiyatını kontrol etmelisiniz!")
        elif choice == "5":
            print("Programdan çıkılıyor...")
            break
        else:
            print("Geçersiz bir seçenek. Lütfen tekrar deneyin.")
menu()