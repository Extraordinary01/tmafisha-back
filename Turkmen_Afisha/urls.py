from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'afisha.views.error_404'
handler403 = 'afisha.views.error_403'
handler500 = 'afisha.views.error_500'

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
] + i18n_patterns(path('', include('afisha.urls')), path('users/', include('users.urls')), path('administrationsettings/', admin.site.urls), path('ckeditor/', include('ckeditor_uploader.urls')))

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns