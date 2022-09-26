from fastapi import FastAPI
from core.configs import settings
from api.v1.api import api_router

app = FastAPI(title='Curso API - Segurança')
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000,
                log_level='info', reload=True)

"""
TOKEN = "
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
    .eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjY0NzE4NDE2LCJpYXQiOjE2NjQxMTM2MTYsInN1YiI6IjEifQ
    .7fDhrPXFOuBwRP0Jeu9HBl85TygPQN-auFGqmx3gb0M"
Type = 'Bearer'
"""
