from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account.controller.views import AccountView

router = DefaultRouter()
router.register(r'', AccountView, basename='account')

urlpatterns = [
    path('', include(router.urls)),
    path('email-duplication-check',
         AccountView.as_view({'post': 'checkEmailDuplication'}),
         name='account-email-duplication-check'),
    path('register', AccountView.as_view({'post': 'registerAccount'}), name='register-account'),
    path('register-social', AccountView.as_view({'post': 'registerSocialAccount'}), name='register-social-account'),
    path('login', AccountView.as_view({'post': 'loginAccount'}), name='login-account'),
    path('login-type', AccountView.as_view({'post': 'checkLoginType'}), name='login-type'),
]
