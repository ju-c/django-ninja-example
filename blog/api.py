from django.shortcuts import get_object_or_404
from ninja import Router
from .schemas import PostIn, PostOut
from .models import Post

# Routers doc:
# https://django-ninja.rest-framework.com/guides/routers/
router = Router()

# Creating a blog post:
# We're using the PostOut serializer as the response.
# The url_name is equivalent to the name attribute in a path.
@router.post("/new_blog_post", response=PostOut, url_name="create_blog_post")
def create_blog_post(request, payload: PostIn):
    # The code should validate that the user is authenticated:
    if request.user.is_authenticated:
        # We using PostIn as our payload.
        # Then, we passing in all the fields in the payload.
        # The .dict() method on PostIn returns a dictionary with all the fields sent in.
        # The double stars operator (**) turns the dictionary
        # into keywords arg. on the create call.
        new_blog_post = Post.objects.create(**payload.dict(), author=request.user)

        return new_blog_post

    return {"Error": "You must be authenticated"}

# Listing the blog posts:
# The .get() decorator takes the path and declares that it will
# respond with a list of PostOut serializers.
# Because the response is set to a list of PostOut serializers,
# we returns the .all() call of the Post ORM.
@router.get("/blog_posts", response=list[PostOut], url_name="list_blog_posts")
def list_blog_posts(request):
    return Post.objects.all()

# Getting a specific blog post:
# Same as list_blog_posts, but this time the path takes an integer (blog_post_id).
@router.get("/blog_post/{int:blog_post_id}", response=PostOut, url_name="blog_post")
def get_blog_post(request, blog_post_id):
    # We using get_object_or_404() to raises a 404 error
    # instead of the DoesNotExist exception is the blog post doesn't exist.
    return get_object_or_404(Post, id=blog_post_id)

# Updating a specific blog post:
# The path need the object ID. It will responds with a PostOut serializer.
# We're updateing an existing blog post, hence the lack of a url_name arg.
@router.put("/blog_post/{int:blog_post_id}", response=PostOut)
def update_blog_post(request, blog_post_id, payload: PostIn):
    # The code should validate that the user is authenticated:
    if request.user.is_authenticated:
        # The code should validate that a user can only edit 
        # his/her own blog's posts (otherwise, return a 404 error):
        author_blog_posts = request.user.post_set
        # Like get_blog_post, we fetch the object from the database,
        # using .get_object_or_404():
        blog_post = get_object_or_404(author_blog_posts, id=blog_post_id)

        # To replace the fields we loop through all of the fields sent in
        # and call .setattr on each of them.
        # This replaces the previous content with the content sent
        # in the payload.
        for item, value in payload.dict().items():
            setattr(blog_post, item, value)

        # Then, the object need to be saved:
        blog_post.save()
        return blog_post
    return {"Error": "You must be authenticated"}


# Deleting a blog post:
# The path need the object ID.
# We don't declare a response in the decorator.
@router.delete("/blog_post/{int:blog_post_id}")
def delete_blog_post(request, blog_post_id):
    # The code should validate that the user is authenticated:
    if request.user.is_authenticated:
        # The code should validate that a user can only delete 
        # his/her own blog's posts (otherwise, return a 404 error):
        author_blog_posts = request.user.post_set
        # We fetch the object from the database, using .get_object_or_404():
        blog_post = get_object_or_404(author_blog_posts, id=blog_post_id)
        # Then we call the ORM .delete() method:
        blog_post.delete()

        return {"Blog post successfully deleted": True}

    return {"Error": "You must be authenticated"}
