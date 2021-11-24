from django.urls import path
from .views import ContactView, PopularAds, Search, AdView, StocksView, AdsByCity, AdsByCategory, GetAd, index, CounterRedirectView

urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact'),
    path('ads/popular/', PopularAds.as_view(), name='popular-ads'),
    path('ads/search/', Search.as_view(), name='search'),
    path('ads/', AdView.as_view(), name='ad-list'),
    path('stocks/', StocksView.as_view(), name='stocks'),
    path('category/<slug:slug>/', AdsByCategory.as_view(), name='category'),
    path('city/<slug:slug>/', AdsByCity.as_view(), name='city'),
    path('ad/<slug:slug>/', GetAd.as_view(), name='ad-details'),
    path('ad/<slug:slug>/counter', CounterRedirectView.as_view(), name='ad-counter'),
    path('', index, name='home'),
]