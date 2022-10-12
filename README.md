## Django Ninja Example

An example [Django Ninja](https://django-ninja.rest-framework.com/) REST framework project.

### API Endpoints

* **/api/v1/docs** (API documentation [provided by the OpenAPI / Swagger UI](https://github.com/swagger-api/swagger-ui)
* **/api/v1/blog/blog_posts/** (Blog posts list endpoint)
* **/api/v1/blog/new_blog_post/** (Blog post create (POST) endpoint)
* **/api/v1/blog/blog_post/{blog_post_id}** (Blog post retrieve (GET), update (PUT) and destroy (DELETE) endpoint)

### Test Case Scenarios
* Get blog post list.
* Get a single blog post.
* Create a blog post with API.
* Update a blog post with API.
* Delete a blog post with API.


### Install & Usage
1. Clone the repo:
    ```
    git clone https://github.com/ju-c/django-ninja-example.git
    ```

2. Move to the base directory:
    ```
    cd django-ninja-example
    ```
    
3. Create a new python environment:
    ```
    python -m venv env
    ```

4. Activate environment:  

On Windows:
    ```
    env\Scripts\activate
    ```

On Linux and Mac:
    ```
    source env/bin/activate
    ```

5. Install the requirements:
    ```bash
    pip install -r requirements.txt
    ``` 

6. Run the migrations:
    ```
    python manage.py makemigrations && python manage.py migrate
    ```

7. Create a super user:
    ```
    python manage.py createsuperuser
    ```
8. Run the server:
    ```
    python manage.py runserver
    ```

### To Do
- Adding a proper authentication management.
- Defining our own exceptions and overriding the defaults provided by Django Ninja.