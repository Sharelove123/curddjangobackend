from rest_framework import viewsets, views, response
from django.db.models import Sum, Avg, Count
from .models import Campaign
from .serializers import CampaignSerializer
import requests

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
        platform_stats = list(Campaign.objects.values('platform').annotate(count=Count('platform')))
        
        return response.Response({
            'total_campaigns': total_campaigns,
            'active_campaigns': active_campaigns,
            'total_budget': float(total_budget),
            'avg_engagement': round(avg_engagement, 1) if avg_engagement else 0,
            'platform_stats': platform_stats
        })

class InfluencerProxyView(views.APIView):
    def get(self, request):
        # Fetch mock data from randomuser.me
        try:
            res = requests.get("https://randomuser.me/api/?results=5", timeout=10)
            res.raise_for_status()
            data = res.json()
            return response.Response(data['results'])
        except Exception as e:
            # Fallback mock data if external API fails
            mock_data = [
                {"name": {"first": "John", "last": "Doe"}, "email": "john@example.com", "location": {"country": "USA"}, "picture": {"thumbnail": "https://i.pravatar.cc/50?u=1"}},
                {"name": {"first": "Jane", "last": "Smith"}, "email": "jane@example.com", "location": {"country": "UK"}, "picture": {"thumbnail": "https://i.pravatar.cc/50?u=2"}},
                {"name": {"first": "Alex", "last": "Johnson"}, "email": "alex@example.com", "location": {"country": "Canada"}, "picture": {"thumbnail": "https://i.pravatar.cc/50?u=3"}},
                {"name": {"first": "Emily", "last": "Brown"}, "email": "emily@example.com", "location": {"country": "Australia"}, "picture": {"thumbnail": "https://i.pravatar.cc/50?u=4"}},
                {"name": {"first": "Michael", "last": "Davis"}, "email": "michael@example.com", "location": {"country": "Germany"}, "picture": {"thumbnail": "https://i.pravatar.cc/50?u=5"}},
            ]
            return response.Response(mock_data)
