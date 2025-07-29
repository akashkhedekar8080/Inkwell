from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import BlogPostForm, CommentForm
from .models import BlogPost

# Create your views here.


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = "blogs/blog_create_edit.html"
    form_class = BlogPostForm
    context_object_name = "blog"

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        response = super().form_valid(form)
        email = getattr(form.instance.author.user, "email", None)
        if email:
            subject = "New Blog Post Created"
            message = (
                f"Hello {self.request.user.username},\n\n"
                f"Your new blog post titled '{form.instance.title}' has been successfully created.\n\n"
                f"View or edit your post anytime on the blog platform.\n\n"
                f"Thank you,\nThe Blog Team"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=True,
            )

        messages.success(self.request, "Blog post created successfully")
        return response

    def get_success_url(self):
        return reverse_lazy("blogs:blog_detail", kwargs={"slug": self.object.slug})


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    template_name = "blogs/blog_create_edit.html"
    form_class = BlogPostForm
    context_object_name = "blog"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        return reverse_lazy("blogs:blog_detail", kwargs={"slug": self.object.slug})

    def test_func(self):
        user = self.request.user
        blog = self.get_object()
        return user.is_superuser or blog.author == user.author

    def form_valid(self, form):
        response = super().form_valid(form)
        email = getattr(form.instance.author.user, "email", None)
        if email:
            subject = "Blog Post Updated"
            message = (
                f"Hello,\n\n"
                f"The blog post titled '{form.instance.title}' was updated by {self.request.user.username}.\n\n"
                f"Check it out on the platform.\n\n"
                f"Regards,\nYour Blog Platform"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=True,
            )
        messages.success(self.request, "Blog post updated successfully!")
        return response


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = "blogs/blog_delete_confirm.html"
    context_object_name = "blog"
    success_url = reverse_lazy("blogs:blog_list")
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def test_func(self):
        user = self.request.user
        blog = self.get_object()
        return user.is_superuser or blog.author == user.author

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Retrieve the blog post before deletion
        blog_title = self.object.title
        author_email = self.object.author.user.email
        deleted_by = self.request.user.username

        print("Author email:", author_email)

        if author_email:
            subject = "Blog Post Deleted"
            message = (
                f"Hello,\n\n"
                f"The blog post titled '{blog_title}' was deleted by {deleted_by}.\n\n"
                f"If this was not expected, please contact the admin.\n\n"
                f"Regards,\nYour Blog Platform"
            )
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [author_email],
                    fail_silently=False,  # <-- Temporarily set to False to catch errors
                )
                print(f"Email sent to {author_email}")
            except Exception as e:
                print("Email sending failed:", e)

        messages.success(request, "Blog post deleted successfully!")
        return super().post(request, *args, **kwargs)


@method_decorator(login_required, name="get")
class BlogListView(ListView):
    model = BlogPost
    template_name = "blogs/blog_post_list.html"
    context_object_name = "blogs"
    ordering = ["-created_at"]
    paginate_by = 2


@method_decorator(login_required, name="dispatch")
class BlogDetailView(DetailView):
    model = BlogPost
    template_name = "blogs/blog_detail.html"
    context_object_name = "blog"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.filter(
            parent__isnull=True
        ).prefetch_related("replies")
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user.author
            comment.post = self.object
            parent_id = request.POST.get("parent_id")
            if parent_id:
                comment.parent_id = parent_id
            comment.save()
            messages.success(request, "Comment Added Successfully")
        return redirect("blogs:blog_detail", slug=self.object.slug)
