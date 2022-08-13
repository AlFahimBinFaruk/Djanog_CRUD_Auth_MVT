from urllib import request
from django.forms import ModelForm
from .models import Blog

# blog form


class BlogForm(ModelForm):
    #tank = forms.IntegerField(widget=forms.HiddenInput(), initial=123) 
    class Meta:
        model = Blog
        fields = '__all__'
        exclude=['blogger']

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'