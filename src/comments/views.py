
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect, get_object_or_404

# Create your views here.

from notifications.signals import notify

from videos.models import Video

from rest_framework import generics, mixins
from .models import Comment
from .forms import CommentForm
from .serializers import CommentCreateSerializer
from .permissions import IsOwnerOrReadOnly

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from comments.serializers import CommentSerializer,CommentCreateSerializer,CommentUpdateSerializer

from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 5

class CommentListAPIView(generics.ListAPIView):
	# authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]

	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticated]
	# paginate_by=10
	pagination_class = LargeResultsSetPagination

class CommentCreateAPIView(generics.CreateAPIView):
	# authentication_classes = [SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication]
	# queryset = Comment.objects.filter(request.user)
	serializer_class = CommentCreateSerializer
	# permission_classes = [permissions.IsAuthenticated]
class CommentDetailAPIView(mixins.DestroyModelMixin,mixins.UpdateModelMixin, generics.RetrieveAPIView):
	serializer_class = CommentUpdateSerializer
	queryset = Comment.objects.all()
	permission_classes = [IsOwnerOrReadOnly]
	
	# def get_queryset(self,*args,**kwargs):
	# 	queryset = Comment.objects.all()
		
	def put(self, request,*args,**kwargs):
		return self.update(request,*args, **kwargs)
		
	def delete(self,request, *args, **kwargs):
		return self.destroy(request,*args, **kwargs)

@login_required
def comment_thread(request, id):
	comment = get_object_or_404(Comment, id=id)
	form = CommentForm()
	context = {
	"form": form,
	"comment": comment,
	}
	return render(request, "comments/comment_thread.html", context)



def comment_create_view(request):
	if request.method == "POST" and request.user.is_authenticated():
		parent_id = request.POST.get('parent_id')
		video_id = request.POST.get("video_id")
		origin_path = request.POST.get("origin_path")
		try:
			video = Video.objects.get(id=video_id)
		except:
			video = None

		print video
		parent_comment = None
		if parent_id is not None:
			try:
				parent_comment = Comment.objects.get(id=parent_id)
			except:
				parent_comment = None

			if parent_comment is not None and parent_comment.video is not None:
				video = parent_comment.video

		form = CommentForm(request.POST)
		if form.is_valid():
			comment_text = form.cleaned_data['comment']
			if parent_comment is not None:
				# parent comments exists
				new_comment = Comment.objects.create_comment(
					user=request.user, 
					path=parent_comment.get_origin, 
					text=comment_text,
					video = video,
					parent=parent_comment
					)
				affected_users = parent_comment.get_affected_users()
				notify.send(
						request.user, 
						action=new_comment, 
						target=parent_comment, 
						recipient=parent_comment.user,
						affected_users = affected_users,
						verb='replied to')
				messages.success(request, "Thank you for your response.", extra_tags='safe')
				return HttpResponseRedirect(parent_comment.get_absolute_url())
			else:
				new_comment = Comment.objects.create_comment(
					user=request.user, 
					path=origin_path, 
					text=comment_text,
					video = video
					)
				# option to send to super user or staff users
				# notify.send(
				# 		request.user, 
				# 		recipient = request.user, 
				# 		action=new_comment, 
				# 		target = new_comment.video,
				# 		verb='commented on')
				#notify.send(request.user, recipient=request.user, action='New comment added')
				messages.success(request, "Thank you for the comment.")
				return HttpResponseRedirect(new_comment.get_absolute_url())
		else:
			print origin_path
			messages.error(request, "There was an error with your comment.")
			return HttpResponseRedirect(origin_path)

	else:
		raise Http404
