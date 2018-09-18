from django import forms
from doctor.models import ContactMessages, DoctorBlog
from PIL import Image
from geoposition.forms import GeopositionField

VALID_IMAGE_FILETYPES = (
    '.jpg','.png','.tiff'
)

class LeaveMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessages
        fields = ('name', 'phone', 'message')


class DashboardPersonalForm(forms.Form):
    base_name = forms.CharField(max_length=255)
    personal_info = forms.Textarea()

class BlogAddForm(forms.ModelForm):
    class Meta:
        model = DoctorBlog
        fields = ('author','title', 'image', 'text')

    def __init__(self, *args, **kwargs):
        super(BlogAddForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True


class PositionForm(forms.Form):
    position = GeopositionField()
class ChangePictureForm(forms.Form):

    profile_image = forms.FileField()
    # Add some custom validation to image field
    def clean_photo(self):
        photo = self.cleaned_data.get(['profile_picture'])
        if photo:
            format = Image.open(photo.file).format
            photo.file.seek(0)
            if format in VALID_IMAGE_FILETYPES:
                return photo
        raise forms.ValidationError('Yalnız jpg, png və tiff formatında şəkillər qəbul olunur')
