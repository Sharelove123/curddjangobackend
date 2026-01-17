from rest_framework import viewsets, views, response
from django.db.models import Sum, Avg, Count
from .models import Campaign
from .serializers import CampaignSerializer
import urllib.request
import json

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all().order_by('-created_at')
    serializer_class = CampaignSerializer

class DashboardStatsView(views.APIView):
    def get(self, request):
        total_campaigns = Campaign.objects.count()
        active_campaigns = Campaign.objects.filter(status='active').count()
        total_budget = Campaign.objects.aggregate(Sum('budget'))['budget__sum'] or 0
        avg_engagement = Campaign.objects.aggregate(Avg('engagement_score'))['engagement_score__avg'] or 0
        
        # Platform breakdown
        platform_stats = Campaign.objects.values('platform').annotate(count=Count('platform'))
        
        return response.Response({
            'total_campaigns': total_campaigns,
            'active_campaigns': active_campaigns,
            'total_budget': total_budget,
            'avg_engagement': round(avg_engagement, 1),
            'platform_stats': platform_stats
        })

class InfluencerProxyView(views.APIView):
    def get(self, request):
        # Fetch mock data from randomuser.me
        try:
            with urllib.request.urlopen("https://randomuser.me/api/?results=5") as url:
                data = json.loads(url.read().decode())
                return response.Response(data['results'])
        except Exception as e:
            return response.Response({'error': str(e)}, status=500)
