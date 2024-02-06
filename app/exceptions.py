from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect login or password"


class NotAllowedException(BookingException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Not allowed"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token Expired"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token Absent"


class TokenEncodeException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token Encode Error"


class CantGetUserFromTokenException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Can't get user from token"


class CantGetUserFromDBException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Can't get user from db"


class RoomCanNotBeBookedException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Room can not be booked"


class NothingToDeleteException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Nothing to delete"


class DateFromIsGreaterThenDateToException(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "date_from is greater then date_to"


class TotalDaysIsGreaterThen30Exception(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Total days is greater then 30"


class CannotAddDataToDatabase(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Can't import to db"


class CannotProcessCSV(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Can't process CSV file"
