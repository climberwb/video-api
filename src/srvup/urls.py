from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
from django.views.generic import TemplateView

from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from videos.serializers import VideoViewSet,CategoryViewSet
from comments.serializers import CommentViewSet
from videos.views import CategoryListAPIView

router =  routers.DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"comments",CommentViewSet)
router.register(r"videos", VideoViewSet)


urlpatterns = patterns('',
    url(r'^api2/projects/',CategoryListAPIView.as_view(), name='category_list_api'),
    # Examples:
    #url(r'^about/$', TemplateView.as_view(template_name='base.html'), name='home'),
    #url(r'^pricing/$', TemplateView.as_view(template_name='base.html'), name='home'),
    url(r'^contact/$', TemplateView.as_view(template_name='company/contact_us.html'), name='contact_us'),
    url(r'^$', 'srvup.views.home', name='home'),
    url(r'^projects/$', 'videos.views.category_list', name='projects'),
    url(r'^projects/(?P<cat_slug>[\w-]+)/$', 'videos.views.category_detail', name='project_detail'),
    url(r'^projects/(?P<cat_slug>[\w-]+)/(?P<vid_slug>[\w-]+)/$', 'videos.views.video_detail', name='video_detail'),
    url(r'^dj/admin/', include(admin.site.urls)),
    url(r'^api/auth/token/$', obtain_jwt_token),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls))
) 

if settings.DEBUG:
    urlpatterns += patterns('',) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += patterns('',) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



#auth login/logout
urlpatterns += patterns('billing.views',
    url(r'^upgrade/$', 'upgrade', name='account_upgrade'),
    url(r'^billing/$', 'billing_history', name='billing_history'),
    url(r'^billing/cancel/$', 'cancel_subscription', name='cancel_subscription'),
)



#auth login/logout
urlpatterns += patterns('accounts.views',
    url(r'^account/$', 'account_home', name='account_home'),
	url(r'^logout/$', 'auth_logout', name='logout'),
    url(r'^login/$', 'auth_login', name='login'),
    url(r'^register/$', 'auth_register', name='register'),
)



#Comment Thread
urlpatterns += patterns('comments.views',
    url(r'^comment/(?P<id>\d+)$', 'comment_thread', name='comment_thread'),
    url(r'^comment/create/$', 'comment_create_view', name='comment_create'),
)


#Notifications
urlpatterns += patterns('notifications.views',
    url(r'^notifications/$', 'all', name='notifications_all'),
    url(r'^notifications/ajax/$', 'get_notifications_ajax', name='get_notifications_ajax'),
    url(r'^notifications/(?P<id>\d+)/$', 'read', name='notifications_read'),

)



