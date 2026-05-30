from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from generate import generate_contract

app = FastAPI()


@app.get("/")
async def root():
    return FileResponse("index.html")


@app.post("/submit")
async def submit_form(
    number: str = Form(...),
    fio: str = Form(...),
    phone: str = Form(...),
    passport_series: str = Form(...),
    passport_number: str = Form(...),
    address: str = Form(...),
):

    output_path = generate_contract(
        number,
        fio,
        phone,
        passport_series,
        passport_number,
        address,
    )

    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="contract.docx"
    )