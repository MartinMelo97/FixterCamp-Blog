from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


class Dashboard(View):
	@method_decorator(login_required)
	def get(self, request):
		template_name="accounts/perfil.html"
		userform = UserEditForm(instance=request.user)
		profileform = ProfileEditForm(instance=request.user.profile)
		context = {'userform':userform, 'profileform': profileform}
		return render(request, template_name, context)
	def post(self, request):
		template_name="accounts/perfil.html"
		updateUser_form = UserEditForm(data=request.POST, instance=request.user)
		updateProfile_form = ProfileEditForm(data=request.POST, instance=request.user.profile, files=request.FILES)
		if updateUser_form.is_valid():
			updateUser = updateUser_form.save(commit=False)
			updateUser.save()
		else:
			context = {
			'userform': updateUser,
			'profileform': updateProfile
			}
		if updateProfile_form.is_valid():
			updateProfile = updateProfile_form.save(commit=False)
			updateProfile.save()
		else:
			context = {
			'userform': updateUser,
			'profileform': updateProfile
			}
		#perfil = Profile()
		#perfil.user = updateProfile
		#perfil.save()
		return redirect('profile')





class Registration(View):
	def get(self, request):
		form = UserRegistrationForm()
		template_name = "accounts/registration.html"
		context = {'form': form,}
		return render(request, template_name, context)

	def post(self, request):
		template_name = "accounts/registration.html"
		new_user_form = UserRegistrationForm(request.POST)
		if new_user_form.is_valid():
			new_user = new_user_form.save(commit=False)
			new_user.set_password(new_user_form.cleaned_data['password'])
			new_user.save()
			perfil = Profile()
			perfil.user = new_user
			perfil.save()
			#perfil = Profile.object.create_or_update or only .create(user=new_user)
			return redirect('profile')
		else:
			context = {'form':new_user_form}
			return render(request, template_name, context)