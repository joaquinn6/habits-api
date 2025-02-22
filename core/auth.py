from typing import Optional
import datetime
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from jose import JWTError, jwt
from passlib.context import CryptContext

from repositories.user_repository import UserRepository
from core.var_env import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from core.helpers_api import raise_no_authorized
from models.user_model import User
from models.token_model import Token
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/")


class AuthService():
  def __init__(self) -> None:
    self._user_repo = UserRepository()

  def verify_password(self, plain_password: str, password: str) -> bool:
    return pwd_context.verify(plain_password, password)

  def get_password_hash(self, password: str) -> str:
    return pwd_context.hash(password)

  def authenticate_user(self, email: str, password: str) -> User | None:
    user = self._user_repo.get_by_email(email)
    if not user:
      return None
    if not self.verify_password(password, user.password):
      return None
    return user

  def create_access_token(self, data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(
        datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode['expire'] = expire.strftime("%Y-%m-%dT%H:%M:%S.%f")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

  def generate_token(self, email: str, password: str) -> Token:
    user = self.authenticate_user(email, password)
    if not user:
      raise_no_authorized()
    token_str = self.create_access_token(
        data={'extra_data': {
            'email': user.email,
            'id': user.id
        }
        }
    )
    return Token(token=f"Bearer {token_str}", email=user.email, id=str(user.id))

  def get_content_token(self, token: str) -> dict:
    try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      email: str = payload['extra_data']['email']
      if email is None:
        self._raise_fail_credentials()
      if self._is_expired(payload['expire']):
        self._raise_token_expired()
    except JWTError:
      self._raise_fail_credentials()
    return payload['extra_data']

  def _is_expired(self, date_str: str) -> bool:
    date = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    date = date.replace(tzinfo=datetime.timezone.utc)
    now = datetime.datetime.now(datetime.timezone.utc)
    return date <= now

  def _raise_fail_credentials(self):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    raise credentials_exception

  def _raise_token_expired(self):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    raise credentials_exception

  def is_logged(self, authorization: str) -> bool:
    content = self.get_content_token(authorization)
    return content is not None


class OptionalHTTPBearer(HTTPBearer):
  async def __call__(self, request: Request) -> Optional[str]:
    try:
      r = await super().__call__(request)
      token = r.credentials
    except HTTPException as ex:
      assert ex.status_code == status.HTTP_403_FORBIDDEN, ex
      token = None
    return token
