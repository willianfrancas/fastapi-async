from passlib.context import CryptContext

CRYPTO = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto'
)


def pwd_verify(pwd: str, hash_pwd: str) -> bool:
    """
    Função para verificar se a senha esta correta,
    comparando a senha em texto puro informada pelo usuario
    e o hash da senha que estará salvo no banco de dados 
    durante a criação da conta.
    """

    return CRYPTO.verify(pwd, hash_pwd)


def gen_hash_pwd(pwd: str) -> str:
    """
    FUNÇÃO QUE GERA E RETORNA O HASH DA SENHA
    """
    return CRYPTO.hash(pwd)
