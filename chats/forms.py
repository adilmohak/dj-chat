from django import forms
from django.contrib.auth.views import get_user_model
from django.db import IntegrityError

from django_select2 import forms as s2forms

from .models import DiscussionRoom, Message
from .models import Tag
# from accounts.models import User


class TagWidget(s2forms.ModelSelect2TagWidget):
	search_fields = [
		"name__icontains",
	]
	queryset = Tag.objects.all()

	def value_from_datadict(self, data, files, name):
		"""Create objects for given non-pimary-key values. Return list of all primary keys."""
		values = list(super().value_from_datadict(data, files, name))
		val_int = []
		val_str = []
		for val in values:
			try:
				val_int.append(int(val))
			except:
				val_str.append(val)
		old_tags = list(self.queryset.filter(**{'pk__in': val_int}).values_list('pk', flat=True))
		print("old_tags", old_tags)
		print("val_int", val_int)
		print("val_str", val_str)

		new_tags = []
		for val in val_str:
			new_tags.append(Tag(name=val))
		new_tags = self.queryset.bulk_create(new_tags, ignore_conflicts=True)

		new_pks = [a.pk for a in new_tags]

		return new_pks + old_tags


class DiscussionRoomForm(forms.ModelForm):
	class Meta:
		model = DiscussionRoom
		# exclude = ['room', 'owner', 'members']
		fields = ['headline', 'description', 'tags']
		widgets = {
			'headline': forms.TextInput(attrs={
				'autocomplete': 'off',
			}),
			'description': forms.Textarea(attrs={
				'rows': 4,
			}),
			'tags': TagWidget,
		}


class RecipientWidget(s2forms.ModelSelect2MultipleWidget):
	search_fields = [
		"email__icontains",
		"first_name__icontains",
		"last_name__icontains",
	]


class BulkMessageForm(forms.Form):
	# To whom do you want to send message
	recipients = forms.ModelMultipleChoiceField(
		queryset=get_user_model().objects.all(), 
		label=u"To whom",
		widget=RecipientWidget,
	)
	message = forms.CharField(widget=forms.Textarea(attrs={
		'rows': 4,
		'placeholder': 'Type your message...'
	}))


class InviteForm(forms.Form):
	users = forms.ModelMultipleChoiceField(
		queryset=get_user_model().objects.all(),
		label="Find peoples",
		help_text="Search by username, email, or full name without including @",
		widget=RecipientWidget,
	)
	room = forms.ModelChoiceField(
		queryset=DiscussionRoom.objects.all(),
		widget=forms.HiddenInput()
	)
