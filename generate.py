from docxtpl import DocxTemplate
import uuid
import os
import json

TEMPLATE_PATH = "templates/contract_template.docx"
OUTPUT_DIR = "generated"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_contract(
    number: str,
    date: str,
    fio: str,
    phone: str,
    passport_series: str,
    passport_number: str,
    passport_code: str,
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

    print()

    context = {
        "number": number,
        "date": date,
        "fio": fio,
        "phone": phone,
        "passport_series": passport_series,
        "passport_number": passport_number,
        "passport_code": passport_code,
        "address": address,
        "organization": organization_name,
        "total": total,
        "nds": nds,
        "products": products_list,
        "total_without_nds": float(total) - float(nds) if total and nds else 0
    }

    doc.render(context)

    filename = f"{uuid.uuid4()}.docx"

    output_path = os.path.join(
        OUTPUT_DIR,
        filename
    )

    doc.save(output_path)

    return output_path