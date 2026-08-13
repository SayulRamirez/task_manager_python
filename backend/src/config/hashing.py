
import bcrypt

class Hasher:
    @staticmethod
    def hash(password: str):
        hashed_password = bcrypt.hashpw(password.encode(),
                                        bcrypt.gensalt())
        return hashed_password.decode()
    
    @staticmethod
    def verify(secret: str, hash: str):
        return bcrypt.checkpw(secret.encode(),
                              hash.encode())