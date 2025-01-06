from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



# Function ya view


# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),  # URL ya admin
    path('', include('base.urls')),
    path('api/', include('base.api.url')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)