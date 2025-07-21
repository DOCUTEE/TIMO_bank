from sqlalchemy.orm import sessionmaker
from model import AuthenticationMethod

def generate_auth_methods(session : sessionmaker):
    """Generate authentication methods for the banking system."""
    # Insert authentication methods if not exist
    auth_methods = {
        "password": False,
        "otp": True,
        "biometric": True,
        "pin": False
    }
    for method, is_strong in auth_methods.items():
        exists = session.query(AuthenticationMethod).filter_by(auth_method=method).first()
        if not exists:
            auth_method = AuthenticationMethod(
                auth_method=method,
                is_strong=is_strong
            )
            session.add(auth_method)
            session.commit()
