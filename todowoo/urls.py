from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from auth_app import views as vAuth
from todo_app import views as vTodo

urlpatterns = [
    path('admin/', admin.site.urls),
    # Authentification
    path('signup/', vAuth.signupuser, name='signupuser'),
    path('login/', vAuth.loginuser, name='loginuser'),
    path('logout/', vAuth.logoutuser, name='logoutuser'),
    # Todos
    path('', vTodo.home, name='home'),
    path('current/', vTodo.currenttodos,  name='currenttodos'),
    path('completed/', vTodo.completedtodos,  name='completedtodos'),
    path('create/', vTodo.createtodo,  name='createtodo'),
    path('todo/<int:todo_pk>', vTodo.viewtodo,  name='viewtodo'),
    path('todo/<int:todo_pk>/complete', vTodo.completetodo,  name='completetodo'),
    path('todo/<int:todo_pk>/delete', vTodo.deletetodo,  name='deletetodo'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
