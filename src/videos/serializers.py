from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import routers, serializers, viewsets,  permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from comments.serializers import CommentSerializer
from .models import Video,Category


class CategoryUrlHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    lookup_field = 'slug'
    pass

class VideoSerializer(serializers.HyperlinkedModelSerializer):
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
    url = CategoryUrlHyperlinkedIdentityField(view_name='category_detail_api')
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

