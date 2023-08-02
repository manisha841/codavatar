from fastapi import HTTPException,status

def custom_message(message,status):
    raise HTTPException(detail= message, status_code= status)

