from django import forms
from inventory_manager.models import Component


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ["identifier", "description", "inventory_level"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes
        self.fields["identifier"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter identifier",
            }
        )
        self.fields["description"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter description",
            }
        )
        self.fields["inventory_level"].widget.attrs.update(
            {
                "class": "form-select",
            }
        )
