from fastapi import HTTPException, status

token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail={"description": "Token Expired", "message": "Please login again"},
    headers={"WWW-Authenticate": "Bearer"},
)

user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User does not exist",
)

incorrect_password_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect Password",
)

user_already_exists_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User already exists",
)

error_sending_confirmation_code = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="There was an error sending the confirmation code",
)

error_confirmation_code = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="The confirmation code is not valid",
)