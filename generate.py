from docxtpl import DocxTemplate
import uuid
import os

TEMPLATE_PATH = "templates/contract_template.docx"
OUTPUT_DIR = "generated"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_contract(
    number,
    fio,
    phone,
    passport_series,
    passport_number,
    address
):
    doc = DocxTemplate(TEMPLATE_PATH)

    context = {
        "number": number,
        "fio": fio,
        "phone": phone,
        "passport_series": passport_series,
        "passport_number": passport_number,
        "address": address,
    }

    doc.render(context)

    filename = f"{uuid.uuid4()}.docx"

    output_path = os.path.join(
        OUTPUT_DIR,
        filename
    )

    doc.save(output_path)

    return output_path