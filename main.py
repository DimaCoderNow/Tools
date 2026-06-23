from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
from generate import generate_contract
import json
import os
from urllib.parse import quote

app = FastAPI()

app.mount("/static", StaticFiles(directory="web"), name="static")


@app.get("/")
async def root():
    return FileResponse("web/index.html")


@app.post("/submit")
async def submit_form(
        organization: str = Form(...),
        number: str = Form(...),
        date: str = Form(...),
        fio: str = Form(...),
        phone: str = Form(...),
        passport_series: str = Form(...),
        passport_number: str = Form(...),
        passport_code: str = Form(...),
        passport_issued: str = Form(...),
        address: str = Form(...),
        total: str = Form(...),
        nds: str = Form(...),
        products: str = Form(...),
):
    try:
        # Парсим JSON с товарами
        products_list = json.loads(products)

        output_path = generate_contract(
            number=number,
            date=date,
            fio=fio,
            phone=phone,
            passport_series=passport_series,
            passport_number=passport_number,
            passport_code=passport_code,
            passport_issued=passport_issued,
            address=address,
            organization=organization,
            total=total,
            nds=nds,
            products=products_list
        )

        return {
            "status": "success",
            "file": output_path,

        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download")
async def download_file(file_path: str):
    """
    Эндпоинт для скачивания файла по пути
    """
    try:
        # Проверяем, существует ли файл
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Файл не найден")


        filename = os.path.basename(file_path)

        # Кодируем имя файла для заголовка
        encoded_filename = quote(filename)

        response = FileResponse(
            file_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        # Устанавливаем заголовок с правильным именем
        response.headers["Content-Disposition"] = (
            f"attachment; filename*=UTF-8''{encoded_filename}"
        )

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from num2words import num2words

# Сумма в рублях
summa = float(123)
print(num2words(summa, lang='ru', to='currency', currency='RUB'))