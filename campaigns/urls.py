from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CampaignViewSet, DashboardStatsView, InfluencerProxyView

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('external/influencers/', InfluencerProxyView.as_view(), name='external-influencers'),
]
