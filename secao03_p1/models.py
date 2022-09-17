from typing import Optional
from pydantic import BaseModel, validator


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int  # Validar que é mais de 12 aulas
    horas: int  # Validar que é mais de 10 aulas

    @validator('titulo')
    def validar_titulo(cls, value: str):
        palavras = value.split(' ')
        # validação 1
        if len(palavras) < 3:
            raise ValueError(f'Título deve conter ao menos 3 palavras')
        # validação 2
        if value.islower():
            raise ValueError(f'Título deve ser capitalizado')

        return value


cursos = [
    Curso(id=1, titulo="Programação para Leigos", aulas=112, horas=58),
    Curso(id=2, titulo="Algoritimos e Lógica de Programação", aulas=87, horas=67)
]
