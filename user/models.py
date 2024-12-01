from django.contrib.auth.models import AbstractUser


# Create your models here.
class BlogUser(AbstractUser):
    """추후 django.contrib.auth에서 필요한 필드들을 추가할때 확장성을 위해 만들어놓음."""

    class Meta:
        db_table = "blog_user"  # 테이블 이름을 명시적으로 설정
