from fastapi import FastAPI
import uvicorn
from routers import sentences


app = FastAPI()
app.include_router(sentences.router_sentences)

# # uncomment for overriding the validation errors from 422 to 400

# from fastapi import status
# from fastapi.encoders import jsonable_encoder
# from fastapi.exceptions import RequestValidationError
# from fastapi.responses import JSONResponse

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     """Overrides FastAPI default status code for validation errors from 422 to 400."""
#     return JSONResponse(
#         status_code=status.HTTP_400_BAD_REQUEST,
#         content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
#     )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
