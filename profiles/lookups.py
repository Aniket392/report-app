from ajax_select import register, LookupChannel
from django.contrib.auth.models import User

@register('userlookup')
class UsersLookup(LookupChannel):
    model = User

    def get_query(self, q, request):
          return self.model.objects.filter(username__icontains=q).order_by('username')
    
    def get_result(self, obj):
         print(obj.username)
         return obj.username
    
    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item.username