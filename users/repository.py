from .models import UserProfile


def get_user_by_id(user_id: str)-> UserProfile | None:
    return UserProfile.objects.filter(user_id=user_id).first()
    
def get_user_by_email(email: str)-> UserProfile | None:
    return UserProfile.objects.filter(email=email).first()