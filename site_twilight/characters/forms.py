from django import forms
from django.core.exceptions import ValidationError
from .models import Character


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        exclude = ("owner",)
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "lore": forms.Textarea(attrs={"rows": 4}),
            "rtag": forms.Textarea(attrs={"rows": 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Agregar validación de longitud máxima en el frontend
        self.fields['first_name'].widget.attrs.update({
            'maxlength': '64',
            'placeholder': 'Máximo 64 caracteres'
        })
        self.fields['last_name'].widget.attrs.update({
            'maxlength': '64',
            'placeholder': 'Máximo 64 caracteres'
        })
        self.fields['country'].widget.attrs.update({
            'maxlength': '64',
            'placeholder': 'Máximo 64 caracteres'
        })
        self.fields['codename'].widget.attrs.update({
            'maxlength': '32',
            'placeholder': 'Máximo 32 caracteres'
        })
        self.fields['faction'].widget.attrs.update({
            'maxlength': '32',
            'placeholder': 'Máximo 32 caracteres'
        })
        self.fields['lore'].widget.attrs.update({
            'maxlength': '5000',
            'placeholder': 'Máximo 5000 caracteres'
        })
        self.fields['morph'].widget.attrs.update({
            'maxlength': '100',
            'placeholder': 'Máximo 100 caracteres'
        })
        self.fields['hat'].widget.attrs.update({
            'maxlength': '100',
            'placeholder': 'Máximo 100 caracteres'
        })
        self.fields['nvg_color'].widget.attrs.update({
            'maxlength': '16',
            'placeholder': 'Máximo 16 caracteres'
        })
        self.fields['shirt'].widget.attrs.update({
            'maxlength': '64',
            'placeholder': 'Máximo 64 caracteres'
        })
        self.fields['pants'].widget.attrs.update({
            'maxlength': '64',
            'placeholder': 'Máximo 64 caracteres'
        })
        self.fields['ntag'].widget.attrs.update({
            'maxlength': '64',
            'placeholder': 'Máximo 64 caracteres'
        })
        
        # Campos numéricos
        for field in ['skin_r', 'skin_g', 'skin_b', 
                     'cntag_r', 'cntag_g', 'cntag_b',
                     'crtag_r', 'crtag_g', 'crtag_b']:
            self.fields[field].widget.attrs.update({
                'min': '0',
                'max': '255',
                'type': 'number',
                'step': '1',
                'placeholder': '0-255'
            })
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validar que al menos un campo de morph esté completado
        morph_fields = [
            cleaned_data.get('morph'),
            cleaned_data.get('hat'),
            cleaned_data.get('nvg_color'),
            cleaned_data.get('shirt'),
            cleaned_data.get('pants'),
            cleaned_data.get('skin_r'),
            cleaned_data.get('skin_g'),
            cleaned_data.get('skin_b'),
            cleaned_data.get('ntag'),
            cleaned_data.get('cntag_r'),
            cleaned_data.get('cntag_g'),
            cleaned_data.get('cntag_b'),
            cleaned_data.get('rtag'),
            cleaned_data.get('crtag_r'),
            cleaned_data.get('crtag_g'),
            cleaned_data.get('crtag_b'),
        ]
        
        has_morph_data = any(
            field is not None and field != '' 
            for field in morph_fields
            if field is not None
        )
        
        if not has_morph_data:
            raise ValidationError("Al menos un campo de morph debe estar definido.")
        
        return cleaned_data
    
    def clean_codename(self):
        codename = self.cleaned_data.get('codename', '')
        if len(codename) > 32:
            raise ValidationError(
                f"El codename no puede exceder los 32 caracteres. "
                f"Actual: {len(codename)} caracteres."
            )
        return codename
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '')
        if len(first_name) > 64:
            raise ValidationError(
                f"El nombre no puede exceder los 64 caracteres. "
                f"Actual: {len(first_name)} caracteres."
            )
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '')
        if len(last_name) > 64:
            raise ValidationError(
                f"El apellido no puede exceder los 64 caracteres. "
                f"Actual: {len(last_name)} caracteres."
            )
        return last_name
    
    def clean_country(self):
        country = self.cleaned_data.get('country', '')
        if len(country) > 64:
            raise ValidationError(
                f"El país no puede exceder los 64 caracteres. "
                f"Actual: {len(country)} caracteres."
            )
        return country
    
    def clean_faction(self):
        faction = self.cleaned_data.get('faction', '')
        if len(faction) > 32:
            raise ValidationError(
                f"La facción no puede exceder los 32 caracteres. "
                f"Actual: {len(faction)} caracteres."
            )
        return faction
    
    def clean_lore(self):
        lore = self.cleaned_data.get('lore', '')
        if len(lore) > 5000:
            raise ValidationError(
                f"El lore no puede exceder los 10000 caracteres. "
                f"Actual: {len(lore)} caracteres."
            )
        return lore
    
    def clean_morph(self):
        morph = self.cleaned_data.get('morph', '')
        if len(morph) > 100:
            raise ValidationError(
                f"El morph no puede exceder los 100 caracteres. "
                f"Actual: {len(morph)} caracteres."
            )
        return morph
    
    def clean_hat(self):
        hat = self.cleaned_data.get('hat', '')
        if len(hat) > 100:
            raise ValidationError(
                f"El hat no puede exceder los 100 caracteres. "
                f"Actual: {len(hat)} caracteres."
            )
        return hat
    
    def clean_nvg_color(self):
        nvg_color = self.cleaned_data.get('nvg_color', '')
        if len(nvg_color) > 16:
            raise ValidationError(
                f"El color NVG no puede exceder los 16 caracteres. "
                f"Actual: {len(nvg_color)} caracteres."
            )
        return nvg_color
    
    def clean_shirt(self):
        shirt = self.cleaned_data.get('shirt', '')
        if len(shirt) > 64:
            raise ValidationError(
                f"La camisa no puede exceder los 64 caracteres. "
                f"Actual: {len(shirt)} caracteres."
            )
        return shirt
    
    def clean_pants(self):
        pants = self.cleaned_data.get('pants', '')
        if len(pants) > 64:
            raise ValidationError(
                f"Los pantalones no pueden exceder los 64 caracteres. "
                f"Actual: {len(pants)} caracteres."
            )
        return pants
    
    def clean_ntag(self):
        ntag = self.cleaned_data.get('ntag', '')
        if len(ntag) > 64:
            raise ValidationError(
                f"El ntag no puede exceder los 64 caracteres. "
                f"Actual: {len(ntag)} caracteres."
            )
        return ntag
    
    def clean_rtag(self):
        rtag = self.cleaned_data.get('rtag', '')
        if len(rtag) > 500:
            raise ValidationError(
                f"El rtag no puede exceder los 500 caracteres. "
                f"Actual: {len(rtag)} caracteres."
            )
        return rtag
    
    def clean_skin_r(self):
        skin_r = self.cleaned_data.get('skin_r')
        if skin_r is not None and (skin_r < 0 or skin_r > 255):
            raise ValidationError("El valor de skin_r debe estar entre 0 y 255")
        return skin_r
    
    def clean_skin_g(self):
        skin_g = self.cleaned_data.get('skin_g')
        if skin_g is not None and (skin_g < 0 or skin_g > 255):
            raise ValidationError("El valor de skin_g debe estar entre 0 y 255")
        return skin_g
    
    def clean_skin_b(self):
        skin_b = self.cleaned_data.get('skin_b')
        if skin_b is not None and (skin_b < 0 or skin_b > 255):
            raise ValidationError("El valor de skin_b debe estar entre 0 y 255")
        return skin_b
    
    def clean_cntag_r(self):
        cntag_r = self.cleaned_data.get('cntag_r')
        if cntag_r is not None and (cntag_r < 0 or cntag_r > 255):
            raise ValidationError("El valor de cntag_r debe estar entre 0 y 255")
        return cntag_r
    
    def clean_cntag_g(self):
        cntag_g = self.cleaned_data.get('cntag_g')
        if cntag_g is not None and (cntag_g < 0 or cntag_g > 255):
            raise ValidationError("El valor de cntag_g debe estar entre 0 y 255")
        return cntag_g
    
    def clean_cntag_b(self):
        cntag_b = self.cleaned_data.get('cntag_b')
        if cntag_b is not None and (cntag_b < 0 or cntag_b > 255):
            raise ValidationError("El valor de cntag_b debe estar entre 0 y 255")
        return cntag_b
    
    def clean_crtag_r(self):
        crtag_r = self.cleaned_data.get('crtag_r')
        if crtag_r is not None and (crtag_r < 0 or crtag_r > 255):
            raise ValidationError("El valor de crtag_r debe estar entre 0 y 255")
        return crtag_r
    
    def clean_crtag_g(self):
        crtag_g = self.cleaned_data.get('crtag_g')
        if crtag_g is not None and (crtag_g < 0 or crtag_g > 255):
            raise ValidationError("El valor de crtag_g debe estar entre 0 y 255")
        return crtag_g
    
    def clean_crtag_b(self):
        crtag_b = self.cleaned_data.get('crtag_b')
        if crtag_b is not None and (crtag_b < 0 or crtag_b > 255):
            raise ValidationError("El valor de crtag_b debe estar entre 0 y 255")
        return crtag_b