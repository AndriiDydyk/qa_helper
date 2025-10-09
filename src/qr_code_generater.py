import os
import base64
import qrcode

from faker import Faker

fake = Faker(locale="uk_UA")
class QrCodeGenerater:
    def __init__(self):
        pass

    def bin_to_hex(self, bin_str: str) -> str:
        """
        Convert 16-bit binary string (e.g. '0000100000000000') to 4-digit HEX (e.g. '0800').
        """
        if len(bin_str) != 16 or not all(c in "01" for c in bin_str):
            raise ValueError("Потрібен 16-бітний рядок, що містить лише 0 та 1")
        return format(int(bin_str, 2), "04X")

    def save_qr_as_png(self, url: str, encrypted_qr: str, filename: str) -> str:
        output_dir = "data/qr"
        os.makedirs(output_dir, exist_ok=True)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(f"{url}{encrypted_qr}")
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        file_path = os.path.join(output_dir, f"{filename}.png")
        img.save(file_path)

        return file_path

    def create_nbu_qr_code(
            self,
            service_label: str,
            qr_version: str,
            encoding_version: str,
            function: str,
            iban: str,
            recipient_name: str = "",
            recipient_inn: str = "",
            currency: str = "",
            amount: str = "",
            payments_details: str = "",
            recipient_id: str = "",
            category: str = "",
            reference: str = "",
            display_text: str = "",
            lock_code: str = "",
            expiry_datetime: str = "",
            creation_datetime: str = "",
            signature: str = ""
    ) -> str:
        data = (
            f"{service_label}\n"                  # Службова мітка (можливі варінати: BCD)
            f"{qr_version}\n"                     # Версія формату (можливі варінати: 001, 002, 003)
            f"{encoding_version}\n"               # Версія кодування (можливі варінати: 1 або 2)
            f"{function}\n"                       # Функція (можливі варінати: UCT або ICT або XCT)
            f"{recipient_id}\n"                   # Унікальний ідентифікатор отримувача
            f"{recipient_name}\n"                 # ПІБ / найменування
            f"{iban}\n"                           # IBAN
            f"{currency}{amount}\n"               # Сума + валюта
            f"{recipient_inn}\n"                  # ІПН / ЄДРПОУ
            f"{category}\n"                       # Категорія / ціль
            f"{reference}\n"                      # Reference
            f"{payments_details}\n"               # Призначення платежу
            f"{display_text}\n"                   # Додатковий текст
            f"{lock_code}\n"                      # Код заборони зміни
            f"{expiry_datetime}\n"                # Дата / час дії рахунку (у форматі РРММДДГГХХСС)
            f"{creation_datetime}\n"              # Дата / час формування (у форматі РРММДДГГХХСС)
            f"{signature}"                        # Електронний підпис
        )

        base64_bytes = base64.urlsafe_b64encode(data.encode('utf-8'))
        encrypted_qr = base64_bytes.decode('utf-8').rstrip('=')
        return encrypted_qr

    def decode_base64_url(self, base64_url: str) -> str:
        padding = '=' * (4 - len(base64_url) % 4)
        base64_url_padded = base64_url + padding
        decoded_bytes = base64.urlsafe_b64decode(base64_url_padded)

        return decoded_bytes.decode('utf-8')


qr_gen = QrCodeGenerater()
base_64_data = qr_gen.create_nbu_qr_code(
    service_label="",
    qr_version="",
    encoding_version="",
    function="",
    iban="",
    recipient_name="",
    recipient_inn="",
    amount="",
    currency="",
    payments_details="",
)
path = qr_gen.save_qr_as_png("https://bank.gov.ua/qr/", base_64_data, "test_qr")

print(f"QR збережено: {path}")
print(base_64_data)
print(qr_gen.decode_base64_url(base_64_data))