from rest_framework.exceptions import APIException


class CantFollowYourself(APIException):
    status_code = 403
    default_detail = "You cannot follow yourself."
    default_code = "forbidden"


class CantUnFollowYourself(APIException):
    status_code = 403
    default_detail = "You cannot unfollow yourself."
    default_code = "forbidden"
