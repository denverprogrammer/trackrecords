from django.shortcuts import render

## views.py
from django.views.generic import ListView
from membership.models import Membership, Subscription, UserMembership


class MembershipView(ListView):
    model = Membership
    template_name = 'memberships/list.html'

    def get_user_membership(self):
        user_membership_qs = UserMembership.objects.filter(user=self.request.user)
        if user_membership_qs.exists():
            return user_membership_qs.first()
        return None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = self.get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership)
        return context
    
### import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from membership.models import Membership, Subscription, UserMembership


class SignUpForm(UserCreationForm):
    free_membership = Membership.objects.get(membership_type='Free')

    class Meta(UserCreationForm.Meta):
       model = settings.AUTH_USER_MODEL

    def save(self):
      user = super().save(commit=False)
      user.save()

      # Creating a new UserMembership
      user_membership = UserMembership.objects.create(user=user, membership=self.free_membership)
      user_membership.save()

      # Creating a new UserSubscription
      user_subscription = Subscription()
      user_subscription.user_membership = user_membership
      user_subscription.save()

      return user
