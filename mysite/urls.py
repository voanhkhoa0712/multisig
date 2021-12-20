"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from demo.views import *

urlpatterns = [
    path('', index),
    path('create_user', create_user),
    path('remove_user', remove_user),
    path('set_status', set_status),
    path('view_secret', view_secret),
    path('view_nonce', view_nonce),

    path('admin', admin),
    path('setup_party', setup_party),
    path('sign_message', sign_message),
    path('list_member', list_member),
    path('reset_member', reset_member),
]
