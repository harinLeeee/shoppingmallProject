from django.contrib import admin
from django.urls import path, include
from shoppingApp import views
from accounts import views as account_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('boards/', views.boards, name='boards'),
    path('search/', views.search, name='search'),
    path('products/', views.products, name='products'),

    # django modelform을 이용해 블로그 객체 만들기
    path('create/', views.create, name='create'),
    path('detail/<int:post_id>', views.detail, name='detail'), # <int:post_id> detail 함수에 넘길 값
    path('new_comment/<int:post_id>', views.new_comment, name='new_comment'),

    path('login/', account_views.login, name='login'),
    path('logout/', account_views.logout, name='logout'),
    path('signup/', account_views.signup, name='signup'),

    path('detail/<int:post_id>/delete', views.delete, name='delete'),
    path('detail/<int:post_id>/edit', views.edit, name='edit'),

    path('detail/<int:post_id>/delete_comment/<int:com_id>', views.delete_comment, name='delete_comment'),
    path('detail/<int:post_id>/edit_comment/<int:com_id>', views.edit_comment, name='edit_comment'),

    path('accounts/', include('allauth.urls')),
]

# media 파일에 접근할 수 있는 url도 추가해주어야 함
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)