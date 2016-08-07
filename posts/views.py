# -*- encoding: utf-8
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from taggit.models import Tag
from django.db.models import Count

class Lista(View):
	def get(self, request,  tag_slug=None):
		template_name = "posts/lista.html"
		posts = Post.objects.all()
		tag = None
		if tag_slug:
			tag = get_object_or_404(Tag, slug=tag_slug)
			posts = posts.filter(tags__in=[tag])
		context = {'posts':posts, 'tag':tag,}
		return render(request, template_name, context)

class DetailView(View):
	def get(self,request,slug):
		template_name = 'posts/detalle.html'
		#post = Post.objects.get(slug=slug)
		post = get_object_or_404(Post,slug=slug)
		comment_form = CommentForm()
		post_tags_id = post.tags.values_list('id', flat=True)
		posts_similares = Post.objects.filter(tags__in=post_tags_id).exclude(id=post.id)
		posts_similares = posts_similares.annotate(same_tags=Count('tags'))
		context = {'post':post, 'comment_form':comment_form,'posts_similares':posts_similares}
		return render(request,template_name,context)

	def post(self,request,slug):
		comment_form = CommentForm(request.POST)
		template_name = 'posts/detalle.html'
		if comment_form.is_valid():
			comentario = comment_form.save(commit=False)
			comentario.autor = request.user
			comentario.post = Post.objects.get(slug=slug)
			comment_form.save()
			post = get_object_or_404(Post,slug=slug)
			comment_form = CommentForm()
			context = {'post':post, 'comment_form':comment_form,}
			return render(request,template_name,context)
		else:
			context = {}
			return render(request,template_name,context)



class FormView(View):
	@method_decorator(login_required)
	def get(self,request):
		template_name = 'posts/formulario.html'
		form = PostForm()
		context = {'form': form}
		return render(request, template_name, context)

	def post(self,request):
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			nuevo_post = form.save(commit=False)
			nuevo_post.slug = slugify(nuevo_post.titulo)
			nuevo_post.autor = request.user
			nuevo_post.save()
			#la docu de taggit pide esto
			form.save_m2m()
			messages.success(request,'Tu post se ha guardado con exito')
			return redirect('posts:lista')
		else:
			messages.error(request,'No se guardo')
			return redirect('posts:nuevo')

