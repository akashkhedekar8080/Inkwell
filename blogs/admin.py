from django.contrib import admin

from .models import Author, BlogPost, Comment


# Register your models here.
class StatusFilter(admin.SimpleListFilter):
    title = "Post Status"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return (
            ("draft", "Draft"),
            ("published", "Published"),
            ("archived", "Archived"),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "short_content",
        "comment_count",
        "image",
        "author_name",
        "is_published",
        "status",
        "published_at",
        "created_at",
    )
    date_hierarchy = "published_at"
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "content")
    list_filter = ("published_at", "created_at", "status", StatusFilter)
    inlines = (CommentInline,)

    def author_name(self, obj):
        return obj.author.full_name if obj.author else "Anonymous"

    author_name.short_description = "Author name"

    def short_content(self, obj):
        return obj.content[:75] + "..." if len(obj.content) > 75 else obj.content

    short_content.short_description = "Content"

    def comment_count(self, obj):
        return obj.comments.count()

    comment_count.short_description = "Comments"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "content", "parent", "created_at")
    date_hierarchy = "created_at"
    search_fields = ("content",)
    list_filter = ("author",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "full_name", "user", "email")
    date_hierarchy = "created_at"
    search_fields = ("first_name", "last_name", "full_name", "email")
    list_filter = ("email",)
