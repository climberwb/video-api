from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import routers, serializers, viewsets,  permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.reverse import reverse


from comments.serializers import CommentSerializer
from .models import Video,Category


class UrlHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    lookup_field = 'slug'
    pass

class VideoUrlHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    
    def get_url(self, obj,view_name,request,format):
        kwargs = {
            "cat_slug":obj.category.slug,
            "vid_slug":obj.slug
        }
        # print(reverse(view_name,kwargs=kwargs))
        return reverse(view_name,kwargs=kwargs,request=request,format=format)

class VideoSerializer(serializers.HyperlinkedModelSerializer):
    url = VideoUrlHyperlinkedIdentityField(view_name='video_detail_api')
    # view_name='video_detail_api'
    # url = serializers.HyperlinkedIdentityField("video_detail_api")
    # category_url = serializers.CharField(source='category.get_absolute_url', read_only=True)
    # category = CategorySerializer(many=False,read_only=True )
    comment_set = CommentSerializer(many=True, read_only=True)
    category_title = serializers.CharField(source='category.title', read_only=True)
    category_image = serializers.CharField(source='category.get_image_url', read_only=True)
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = Video
        fields = [
                'id',
                'slug',
                "url",
                'title',
                'embed_code',
                'share_message',
                'timestamp',
                'order',
                # 'category',
                'category_image',
                'category_title',
                "comment_set"
                # 'category_url'
            ]
 
 
            
class VideoViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = UrlHyperlinkedIdentityField(view_name='category_detail_api')
    video_set = VideoSerializer(many=True)
    # category_url = serializers.CharField(source='category.get_absolute_url', read_only=True)
    # category_title = serializers.CharField(source='self.title', read_only=True)
    # category_image = serializers.CharField(source='self.get_image_url', read_only=True)
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = Category
        fields = [
                'id',
                'slug',
                'title',
                'active',
                'description',
                'image',
                "url",
                "video_set"
                # 'category_image',
                # 'category_title',
                # 'category_url'
            ]


class CategoryViewSet(viewsets.ModelViewSet):
    # authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated,]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

