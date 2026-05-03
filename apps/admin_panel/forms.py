from django import forms

from apps.achievements.models import Achievement
from apps.courses.models import Course


def apply_admin_form_styles(form):
    for field in form.fields.values():
        widget = field.widget
        existing_class = widget.attrs.get('class', '')
        if isinstance(widget, forms.Select):
            widget.attrs['class'] = f'{existing_class} form-select'.strip()
        elif isinstance(widget, forms.Textarea):
            widget.attrs['class'] = f'{existing_class} form-control'.strip()
            widget.attrs.setdefault('rows', 4)
        else:
            widget.attrs['class'] = f'{existing_class} form-control'.strip()


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'category',
            'level',
            'cover_url',
            'xp_reward',
            'is_published',
        ]
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
            'category': forms.Select(),
            'level': forms.Select(),
            'cover_url': forms.URLInput(),
            'xp_reward': forms.NumberInput(attrs={'min': 10, 'max': 2000}),
            'is_published': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_admin_form_styles(self)


class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = [
            'title',
            'description',
            'icon',
            'category',
            'condition_type',
            'condition_value',
            'xp_reward',
            'is_active',
        ]
        widgets = {
            'title': forms.TextInput(),
            'description': forms.Textarea(),
            'icon': forms.TextInput(),
            'category': forms.Select(),
            'condition_type': forms.TextInput(),
            'condition_value': forms.NumberInput(attrs={'min': 1}),
            'xp_reward': forms.NumberInput(attrs={'min': 0, 'max': 5000}),
            'is_active': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_admin_form_styles(self)
