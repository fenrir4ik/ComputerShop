from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.store.urls')),
    path('user/', include('apps.user.urls')),
    path('admin-panel/', include('apps.admin_panel.urls')),
]

# urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
