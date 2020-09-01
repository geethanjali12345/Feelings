from django.urls import path
from .views import HomeView,signup,NotesView,AddNotesView,user_profile,AddProfile,edit_user_profile,NoteDetail,like_post,favNotesList,UpdateNote,DeleteNote,signout
from django.contrib.auth import views as auth_views
# from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    # path('home/', HomeView, name='home'),
    path('notes/', NotesView, name='notes'),
    path('note/<int:pk>',NoteDetail,name='note-detail'),
    path('like/',like_post,name='like_post'),
    path('profile',user_profile,name='profile'),
    path('profile/add',AddProfile.as_view(),name='add-profile'),
    path('profile/edit',edit_user_profile,name='edit-profile'),
    path('note/<slug:slug>/edit', UpdateNote.as_view(), name='note-update'),
    path('note/<slug:slug>/delete',DeleteNote.as_view(),name='delete-note'),
    path('myfavourites/', favNotesList, name='my-fav'),
    # # path('profile/',profileView,name='profile'),
    # path('profile/',SimpleProfile.as_view(),name='profile'),
    # path('note/<int:pk>',updateNoteView.as_view(),name='update-note'),
    # path('profile/<int:pk>',updateProfileView.as_view(),name='update-profile'),
    # path('note/<int:pk>/delete',deleteNoteView.as_view(),name='delete-note'),
    # # path('signup/', signup, name="signup")
    # # path('signup/', SignUpView.as_view(), name="register"),
    path('signup/',signup,name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', signout, name='logout'),
    path('add/', AddNotesView.as_view(), name='add-notes'),
    path('logout/', signout, name='logout'),
    # path('<int:pk>', NoteDetailView, name='note_detail'),
    # path('favourites/', favouritePost, name='favorite_note'),
    # path('myfavourites/', favNotesList, name='my-fav'),

]