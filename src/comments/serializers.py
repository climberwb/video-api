from django.contrib.auth import get_user_model




from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import routers, serializers, viewsets,  permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.reverse import reverse
from .models import Comment
# from accounts.models import MyUser

User = get_user_model()

class CommentVideoUrlHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj,view_name,request,format):
        kwargs = {
            "cat_slug":obj.video.category.slug,
            "vid_slug":obj.video.slug
        }
        # print(reverse(view_name,kwargs=kwargs))
        return reverse(view_name,kwargs=kwargs,request=request,format=format)
    
class CommentUpdateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username',read_only=True)
    class Meta:
        model = Comment
        fields = [
                'id',
                'user',
                'text'
            ]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
                'text',
                'user',
                'video',
                'parent'
            ]
            



class ChildCommentSerializer(serializers.HyperlinkedModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user = serializers.CharField(source='user.username',read_only=True)
    class Meta:
        model = Comment
        fields = [
                'id',
                "user",
                'text'
            ]
 


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField("comment_detail_api",lookup_field="pk")
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    video = CommentVideoUrlHyperlinkedIdentityField("video_detail_api")
    user = serializers.CharField(source='user.username',read_only=True)
    children = serializers.SerializerMethodField(read_only=True)
    
    def get_children(self,instance):
    # queryset = instance.get_children()
        queryset = Comment.objects.filter(parent__pk =instance.pk)
        serializer = ChildCommentSerializer(queryset,context={"request":instance}, many=True)
        return serializer.data 
        
    class Meta:
        model = Comment
        fields = [
                "url",
                'id',
                "children",
                # "parent",
                "user",
                'video',
                'text'
            ]
 
 
            
class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    

