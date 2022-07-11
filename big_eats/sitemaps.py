from django.contrib.sitemaps import Sitemap
from checkout.models import Invoice, OrderLineItem
from product.models import Category, Product
from profiles.models import UserProfile

 
class Big_eatsSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    protocol = 'http'
    
    def items(self):
        return Invoice.objects.all(), OrderLineItem.objects.all(), Category.objects.all(), Product.objects.all(), UserProfile.objects.all()

    def lastmod(self, obj):
        return obj.article_published
        
    def location(self,obj):
        return '/blog/%s' % (obj.article_slug)