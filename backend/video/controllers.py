from django.contrib.auth import get_user_model, authenticate
from ninja import Router, File
# from .schemas import ChatMessage, PartyCreate
# from .models import Party, Message
from ..schemas import MessageOut
from ninja.files import UploadedFile
User = get_user_model()

video_controller = Router(tags=['video'])
from .models import VideoUpload

@video_controller.post('upload_video', response={
    200: MessageOut,
})
def upload(request, file: UploadedFile = File(...), thumbnail: UploadedFile = File(...),
            title: str = None, description: str = None
           ):
    data = file.read()
    upload = VideoUpload(video=file, title=title, thumbnail=thumbnail, description=description)
    upload.save()
    url = upload.video.url
    return 200, {'detail': url}


