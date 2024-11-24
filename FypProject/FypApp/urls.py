from django.urls import path
from . import views


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Main, name='Main'),
    path('SignUp/', views.SignUp, name='SignUp'),
    path('SignIn/', views.SignIn, name='SignIn'),
    #path('dashboard/<int:id>/', views.dasboard, name='dashboard')
    path('dashboard/', views.dasboard, name='dashboard'),
    path('dashboard/Logout', views.Logout, name='Logout'),
    #path('dashboard/addPost/<int:id>/', views.addPost, name='addPost'),
    #path('dashboard/delete_post/<int:id>/', views.deletePost, name='delete_post'),
    #path('dashboard/update_post/<int:post_id>/', views.updatePost, name='update_post')
    path('dashboard/image_upload/<int:user_id>', views.image_upload_view, name='image_upload'),
    path('dashboard/image_upload/', views.image_upload_view, name='image_upload'),
    path('dashboard/delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)