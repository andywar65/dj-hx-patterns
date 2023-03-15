from django.forms import ModelForm

from .models import Row


class RowCreateForm(ModelForm):
    class Meta:
        model = Row
        fields = "__all__"


class RowUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RowUpdateForm, self).__init__(*args, **kwargs)
        self.fields["title"].required = False
        self.fields["color"].required = False

    class Meta:
        model = Row
        fields = "__all__"
