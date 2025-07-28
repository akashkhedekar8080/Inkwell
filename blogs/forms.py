from django import forms

from .models import BlogPost, Comment


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "title",
            "content",
            "image",
            "is_published",
            "published_at",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter post title"}
            ),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "published_at": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Add a comment..."}
            )
        }
