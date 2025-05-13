from django.contrib import admin
from django.urls import path, include
from authentification.views import (
    signIn,
    postsignIn,
    logout,
    signUp,
    postsignUp,
    reset,
    postReset
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path('', signIn),
    path('postsignIn/', postsignIn),
    path('signUp/', signUp, name="signup"),
    path('logout/', logout, name="log"),
    path('postsignUp/', postsignUp),
    path("api/", include("api.urls")),
    path('reset/', reset),
    path('postReset/', postReset),
    path('resend_verification/', resend_verification, name='resend_verification'),
]
