from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.

#Based on MVC Model

def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)

# Model Manager for filtering posts
class PostManager(models.Manager):
	def all(self, *args, **kwargs):
		# Post.objects.all() = super(PostManager, self).all()
		return super(PostManager, self).filter(draft=False, publish_date__lte=timezone.now())


class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique=True)

	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	image = models.ImageField(
		upload_to=upload_location,
		null=True,
		blank=True,
		width_field="width_field",
		height_field="height_field")
	
	draft = models.BooleanField(default=False)
	publish_date = models.DateField(auto_now=False, auto_now_add=False)
	content = models.TextField()
	last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	posted = models.DateTimeField(auto_now=False, auto_now_add=True)

	# Need to instantiate ModelManager for it to work
	objects = PostManager()

	# if we call "objects" as "posts" like so 
	# posts = PostManager()
	# Then the call to filter becomes "Post.posts.all()" instead of "Post.objects.all()"

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"slug":self.slug})
		# return "/posts/%s/" %(self.id)

	class Meta:
		# Orders by most recently edited post
		# For this to work disable ordering in the view
		# First parameter takes precedence over the others
		ordering = ['-posted', '-last_updated']

def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	
	querySet = Post.objects.filter(slug=slug).order_by("-id")
	exists = querySet.exists()
	if exists:
		new_slug = "%s-%s" %(slug, querySet.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)