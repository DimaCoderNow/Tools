from docxtpl import DocxTemplate
from num2words import num2words
import os
import re

TEMPLATE_PATH = "templates/contract_template.docx"
OUTPUT_DIR = "generated"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_filename(filename):
    """Удаляет недопустимые символы из имени файла"""
    # Заменяем все недопустимые символы на '_'
    # Недопустимые: / \ : * ? " < > |
    return re.sub(r'[\\/*?:"<>|]', '', filename)

def split_summ(sum_text):
    # Сумма в рублях
    summa = float(sum_text)
    parts = num2words(summa, lang='ru', to='currency', currency='RUB').split(", ")
    left_parts = parts[0].rsplit(" ", 1)
    right_parts = parts[1].rsplit(" ", 1)
    return left_parts[0], left_parts[1], right_parts[0], right_parts[1]

def formatted_date(date_str):
    year, month, day = date_str.split("-")
    months = {
        "01": "января", "02": "февраля", "03": "марта", "04": "апреля",
        "05": "мая", "06": "июня", "07": "июля", "08": "августа",
        "09": "сентября", "10": "октября", "11": "ноября", "12": "декабря"
    }
    return f"{int(day)} {months[month]} {year} года"

def format_name(full_name):
    parts = full_name.split()
    if len(parts) == 3:
        return f"{parts[0]} {parts[1][0]}.{parts[2][0]}."
    else:
        return full_name  # Возвращаем как есть, если формат не совпадает

def generate_contract(
    number: str,
    date: str,
    fio: str,
    phone: str,
    passport_series: str,
    passport_number: str,
    passport_code: str,
    passport_issued: str,
    address: str,
    organization: str,
    total: str,
    nds: str,
    products: list
):
    doc = DocxTemplate(TEMPLATE_PATH)

    # Форматируем список товаров для шаблона
    products_list = []
    for idx, product in enumerate(products, 1):
        products_list.append({
            "index": idx,
            "name": product.get('name', ''),
            "quantity": product.get('quantity', '0'),
            "amount": product.get('amount', '0')
        })

    # Получаем название организации для отображения
    organization_name = ""
    if organization == "lysenko":
        organization_name = "ИП Лысенко"
    elif organization == "stroytechagro":
        organization_name = "Стройтехагро"
    elif organization == "robix":
        organization_name = "Робикс"

    amount_words, currency_rub, cents_words, currency_kop = split_summ(total)

    context = {
        "number": number,
        "date": formatted_date(date),
        "fio": fio,
        "format_fio": format_name(fio),
        "phone": phone,
        "passport_series": passport_series,
        "passport_number": passport_number,
        "passport_code": passport_code,
        "passport_issued": passport_issued,
        "address": address,
        "organization": organization_name,
        "amount_words": amount_words.capitalize(),
        "currency_rub": currency_rub,
        "cents_words": cents_words,
        "currency_kop": currency_kop,
        "cents_number": total.split('.')[1],
        "total": f"{float(total):,.2f}".replace(".", ",").replace(",", " ", 1),
        "nds": float(nds),
        "products": products_list,
    }

    doc.render(context)

    raw_filename = f"ДКП {organization_name} {number}.docx"
    filename = clean_filename(raw_filename)
    output_path = os.path.join(
        OUTPUT_DIR,
        filename
    )

    doc.save(output_path)

    return output_path