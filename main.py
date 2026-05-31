from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
from generate import generate_contract
import json

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
            address=address,
            organization=organization,
            total=total,
            nds=nds,
            products=products_list
        )

        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=f"contract_{number}.docx"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))