import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

print(verify_password("123", "$2b$12$L3eqOGBXLArUH/XOHOzdXuleZcSsbBTBqdwDgCnLsNdeksIRdvJbq"))