from fastapi import HTTPException, status


def raise_error_404(entity: str = 'Entity'):
  raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"{entity} no encontrado",
      headers={"WWW-Authenticate": "Bearer"},
  )


def raise_error_400(message: str = 'Entity'):
  raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"{message}",
      headers={"WWW-Authenticate": "Bearer"},
  )


def raise_error_409(entity: str = 'Entity'):
  raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail=f"{entity} ya existe",
      headers={"WWW-Authenticate": "Bearer"},
  )


def raise_error_422(entity: str = 'Contraseña'):
  raise HTTPException(
      # Usando 422 Unprocessable Entity
      status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
      detail=f"{entity} actual es incorrecta.",
      headers={"WWW-Authenticate": "Bearer"},
  )


def raise_no_authorized():
  credentials_exception = HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Usted no esta autorizado para esta acción",
      headers={"WWW-Authenticate": "Bearer"},
  )
  raise credentials_exception
