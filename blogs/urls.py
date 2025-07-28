from django.urls import path

from . import views

app_name = "blogs"
urlpatterns = [
    path("", views.BlogListView.as_view(), name="blog_list"),
    path("detail/<slug:slug>", views.BlogDetailView.as_view(), name="blog_detail"),
    path("create/", views.BlogCreateView.as_view(), name="blog_create"),
    path("edit/<slug:slug>", views.BlogUpdateView.as_view(), name="blog_edit"),
    path("delete/<slug:slug>", views.BlogDeleteView.as_view(), name="blog_delete"),
]
