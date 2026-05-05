from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Media, Like, Comment, Playlist

OFFENSIVE_WORDS = ['offensive', 'spam', 'scam', 'hate', 'abuse', 'violence', 'badword', 'stupid', 'idiot']

def contains_offensive_word(*texts):
    for text in texts:
        if not text: continue
        words = text.lower().replace(',', ' ').replace('.', ' ').split()
        for w in words:
            if w in OFFENSIVE_WORDS:
                return True
    return False

def home(request):
    trending_audio = Media.objects.filter(media_type='audio', status='approved').order_by('-view_count')[:4]
    trending_video = Media.objects.filter(media_type='video', status='approved').order_by('-view_count')[:4]
    return render(request, 'home.html', {
        'trending_audio': trending_audio,
        'trending_video': trending_video
    })


# REGISTER
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm_password']
        role = request.POST['role']

        if password != confirm:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username exists'})

        User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            role=role
        )
        return redirect('login')

    return render(request, 'register.html')


# LOGIN (with ADMIN)
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # ✅ ADMIN LOGIN
        if username == "admin" and password == "admin123":
            request.session['role'] = 'admin'
            request.session['username'] = 'admin'
            return redirect('admin_panel')

        user = User.objects.filter(username=username).first()

        if user and check_password(password, user.password):
            request.session['role'] = user.role
            request.session['username'] = user.username
            return redirect('dashboard')

        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# DASHBOARD
def dashboard(request):
    if 'role' not in request.session:
        return redirect('login')

    return render(request, 'dashboard.html', {
        'role': request.session.get('role')
    })


# UPLOAD AUDIO
def upload_audio(request):
    if request.session.get('role') != 'uploader':
        return redirect('login')

    if request.method == "POST":
        file_obj = request.FILES.get('file')
        thumbnail = request.FILES.get('thumbnail')
        title = request.POST.get('title', '')
        music_director = request.POST.get('music_director', '')
        singer = request.POST.get('singer', '')
        release_year = request.POST.get('release_year', '')
        release_date = request.POST.get('release_date', '')

        status = 'approved'
        rejection_reason = None

        ext = file_obj.name.split('.')[-1].lower()
        if ext not in ['mp3', 'wav']:
            status = 'rejected'
            rejection_reason = 'Auto-rejected: Only .mp3 or .wav allowed.'
        elif file_obj.size > 20 * 1024 * 1024:
            status = 'rejected'
            rejection_reason = 'Auto-rejected: Audio file exceeds 20MB limit.'
        elif not title or not music_director or not singer:
            status = 'rejected'
            rejection_reason = 'Auto-rejected: Title, Music Director, and Singer are required.'
        elif contains_offensive_word(title, music_director, singer):
            status = 'rejected'
            rejection_reason = 'Auto-rejected: Offensive language violation.'

        Media.objects.create(
            title=title,
            media_type='audio',
            music_director=music_director,
            singer=singer,
            release_year=int(release_year) if release_year.isdigit() else None,
            release_date=release_date if release_date else None,
            file=file_obj,
            thumbnail=thumbnail,
            uploaded_by=request.session.get('username'),
            status=status,
            rejection_reason=rejection_reason
        )
        return redirect('dashboard')

    return render(request, 'uploader_audio.html')


# UPLOAD VIDEO
def upload_video(request):
    if request.session.get('role') != 'uploader':
        return redirect('login')

    if request.method == "POST":
        file_obj = request.FILES.get('file')
        thumbnail = request.FILES.get('thumbnail')
        title = request.POST.get('title', '')
        director = request.POST.get('director', '')
        actor = request.POST.get('actor', '')
        actress = request.POST.get('actress', '')
        release_year = request.POST.get('release_year', '')
        release_date = request.POST.get('release_date', '')

        status = 'approved'
        rejection_reason = None

        ext = file_obj.name.split('.')[-1].lower()
        if ext not in ['mp4', 'mkv']:
            status = 'rejected'
            rejection_reason = 'Auto-rejected: Only .mp4 or .mkv allowed.'
        elif file_obj.size > 500 * 1024 * 1024:
            status = 'rejected'
            rejection_reason = 'Auto-rejected: Video file exceeds 500MB limit.'
        elif not title or not director:
            status = 'rejected'
            rejection_reason = 'Auto-rejected: Title and Director are required.'
        elif contains_offensive_word(title, director, actor, actress):
            status = 'rejected'
            rejection_reason = 'Auto-rejected: Offensive language violation.'

        Media.objects.create(
            title=title,
            media_type='video',
            director=director,
            actor=actor,
            actress=actress,
            release_year=int(release_year) if release_year.isdigit() else None,
            release_date=release_date if release_date else None,
            file=file_obj,
            uploaded_by=request.session.get('username'),
            status=status,
            rejection_reason=rejection_reason
        )
        return redirect('dashboard')

    return render(request, 'uploader_video.html')


# 🎵 AUDIO (WITH SEARCH)
def listener_audio(request):
    query = request.GET.get('q')

    media = Media.objects.filter(status='approved', media_type='audio')

    if query:
        media = media.filter(title__icontains=query)

    return render(request, 'listener_audio.html', {
        'media': media,
        'query': query
    })


# 🎬 VIDEO (WITH SEARCH)
def listener_video(request):
    query = request.GET.get('q')

    media = Media.objects.filter(status='approved', media_type='video')

    if query:
        media = media.filter(title__icontains=query)

    return render(request, 'listener_video.html', {
        'media': media,
        'query': query
    })


# 🛡️ ADMIN PANEL (ALL MEDIA)
def admin_panel(request):
    if request.session.get('role') != 'admin':
        return redirect('login')

    media = Media.objects.all().order_by('-id')
    return render(request, 'admin.html', {'media': media})

# 🔍 GLOBAL SEARCH
def global_search(request):
    q = request.GET.get('q', '')
    if not q:
        return redirect('home')

    audio_results = Media.objects.filter(title__icontains=q, media_type='audio', status='approved').order_by('-view_count')
    video_results = Media.objects.filter(title__icontains=q, media_type='video', status='approved').order_by('-view_count')
    creators = User.objects.filter(username__icontains=q, role='uploader')

    return render(request, 'search_results.html', {
        'query': q,
        'audio': audio_results,
        'video': video_results,
        'creators': creators
    })


# LOGOUT
def logout(request):
    request.session.flush()
    return redirect('login')


# 🎧 MEDIA DETAIL PAGE & INCREMENT VIEW COUNT
def media_detail(request, media_id):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    media = get_object_or_404(Media, id=media_id)
    
    # Increment view count
    if request.method == "GET":
        media.view_count += 1
        media.save()

    comments = Comment.objects.filter(media=media).order_by('-created_at')
    
    is_liked = False
    if username:
        is_liked = Like.objects.filter(user_name=username, media=media).exists()
        
    playlists = []
    if username:
        playlists = Playlist.objects.filter(user_name=username)
        
    next_media = Media.objects.filter(media_type=media.media_type, status='approved', id__gt=media.id).order_by('id').first()
    if not next_media:
        next_media = Media.objects.filter(media_type=media.media_type, status='approved').order_by('id').first()

    return render(request, 'media_detail.html', {
        'item': media,
        'comments': comments,
        'is_liked': is_liked,
        'playlists': playlists,
        'next_media': next_media
    })


# ⭐ TOGGLE LIKE
def toggle_like(request, media_id):
    username = request.session.get('username')
    if not username:
        return redirect('login')
        
    media = get_object_or_404(Media, id=media_id)
    like_item = Like.objects.filter(user_name=username, media=media).first()
    
    if like_item:
        like_item.delete()
    else:
        Like.objects.create(user_name=username, media=media)
        
    return redirect('media_detail', media_id=media.id)


# 💬 ADD COMMENT
def add_comment(request, media_id):
    username = request.session.get('username')
    if request.method == "POST" and username:
        text = request.POST.get('text')
        if text:
            media = get_object_or_404(Media, id=media_id)
            Comment.objects.create(user_name=username, media=media, text=text)
    return redirect('media_detail', media_id=media_id)


# 👤 CREATOR PROFILE
def creator_profile(request, username):
    if not request.session.get('username'):
        return redirect('login')

    creator = User.objects.filter(username=username, role='uploader').first()
    # allow showing even if role is not strictly found just in case, but safe to fetch
    media = Media.objects.filter(uploaded_by=username, status='approved').order_by('-id')
    
    return render(request, 'creator_profile.html', {
        'creator_name': username,
        'media': media
    })


# 🌟 LIKED MEDIA
def liked_media(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    likes = Like.objects.filter(user_name=username)
    media = [like.media for like in likes]
    
    return render(request, 'liked_media.html', {'media': media})


# 🎵 PLAYLISTS
def playlists(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            Playlist.objects.create(user_name=username, title=title)
        return redirect('playlists')

    user_playlists = Playlist.objects.filter(user_name=username).order_by('-created_at')
    
    return render(request, 'playlists.html', {'playlists': user_playlists})


# ➕ ADD TO PLAYLIST
def add_to_playlist(request, media_id):
    username = request.session.get('username')
    if request.method == "POST" and username:
        playlist_id = request.POST.get('playlist_id')
        media = get_object_or_404(Media, id=media_id)
        playlist = get_object_or_404(Playlist, id=playlist_id, user_name=username)
        playlist.media_items.add(media)
    return redirect('media_detail', media_id=media_id)

# ➖ REMOVE FROM PLAYLIST
def remove_from_playlist(request, playlist_id, media_id):
    username = request.session.get('username')
    if username:
        media = get_object_or_404(Media, id=media_id)
        playlist = get_object_or_404(Playlist, id=playlist_id, user_name=username)
        playlist.media_items.remove(media)
    return redirect('playlists')

# ⚙️ SETTINGS
def settings_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')
        
    user = User.objects.filter(username=username).first()
    
    if request.method == "POST":
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        
        if email:
            user.email = email
            
        if new_password:
            user.password = make_password(new_password)
            
        user.save()
        return render(request, 'settings.html', {'user': user, 'msg': 'Settings updated successfully'})
        
    return render(request, 'settings.html', {'user': user})