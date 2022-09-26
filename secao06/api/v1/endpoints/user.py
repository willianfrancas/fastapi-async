from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse


from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user_model import UserModel
from schemas.user_schema import UserSchemaBase, UserSchemaCreate, UserSchemaUpdate, UserSchemaArticles

from core.deps import get_session, get_current_user
from core.security import gen_hash_pwd
from core.auth import authenticate, create_token_access


router = APIRouter()


# GET LOGADO
@router.get('/logado', response_model=UserSchemaBase)
async def get_logged(logged_user: UserModel = Depends(get_current_user)):
    return logged_user


# POST / SIGNUP
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def post_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    new_user: UserModel = UserModel(name=user.name, lastname=user.lastname,
                                    email=user.email, pwd=gen_hash_pwd(user.pwd), is_admin=user.is_admin)

    async with db as session:
        try:
            session.add(new_user)
            await session.commit()

            return new_user
        except IntegrityError:
            raise HTTPException(detail='Já existe um usuário com este email cadastrado!',
                                status_code=status.HTTP_406_NOT_ACCEPTABLE)


# GET USUARIOS
@router.get('/', response_model=List[UserSchemaBase])
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserSchemaBase] = result.scalars().unique().all()

        return users


# GET USUARIO
@router.get('/{user_id}', response_model=UserSchemaArticles, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user:
            return user
        else:
            raise HTTPException(detail='Usuário não encontrado!',
                                status_code=status.HTTP_404_NOT_FOUND)


# PUT USUARIO
@router.put('/{user_id}', response_model=UserSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_user(user_id: int, user: UserSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_up: UserSchemaBase = result.scalars().unique().one_or_none()

        if user_up:
            if user.name:
                user_up.name = user.name
            if user.lastname:
                user_up.lastname = user.lastname
            if user.email:
                user_up.email = user.email
            if user.is_admin:
                user_up.is_admin = user.is_admin
            if user.pwd:
                user_up.pwd = gen_hash_pwd(user.pwd)

            await session.commit()
            return user_up

        else:
            raise HTTPException(detail='Usuário não encontrado!',
                                status_code=status.HTTP_404_NOT_FOUND)


# DELETE USUARIO
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_del: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user_del:
            await session.delete(user_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        else:
            raise HTTPException(detail='Usuário não encontrado!',
                                status_code=status.HTTP_404_NOT_FOUND)


# POST LOGIN
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await authenticate(email=form_data.username, pwd=form_data.password, db=db)
    if not user:
        raise HTTPException(detail='Dados de acesso incorretos!',
                            status_code=status.HTTP_400_BAD_REQUEST)

    return JSONResponse(content={"access_token": create_token_access(sub=user.id), "token_type": 'bearer'}, status_code=status.HTTP_200_OK)
