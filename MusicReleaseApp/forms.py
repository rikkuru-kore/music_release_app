from django import forms
from .models import Items
from django.core.exceptions import ValidationError
from django.core import validators

class ItemCreateForm(forms.ModelForm):
    title = forms.CharField(label='タイトル',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'タイトル'}))
    artist = forms.CharField(label='アーティスト',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'アーティスト'}))
    text = forms.CharField(label='説明',widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'説明','style': 'height: 200px;'}))
    level = forms.IntegerField(label='レベル',required=False,widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'レベル'}))
    price = forms.IntegerField(label='価格',widget=forms.NumberInput(attrs={'class': 'form-control','placeholder':'価格'}))
    artwork = forms.FileField(label='アートワーク',required=False,widget=forms.FileInput(attrs={'class': 'form-control','placeholder':'アートワーク'}))
    tab = forms.FileField(label='Tab譜',required=False,widget=forms.FileInput(attrs={'class': 'form-control','placeholder':'Tab譜'}))
    music = forms.FileField(label='楽曲',required=False,widget=forms.FileInput(attrs={'class': 'form-control','placeholder':'楽曲'}))
    image = forms.FileField(label='写真',required=False,widget=forms.FileInput(attrs={'class': 'form-control','placeholder':'写真'}))
    volume = forms.CharField(label='ボリューム',required=False,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'ボリューム'}))
    url = forms.URLField(label='URL',required=False,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'URL'}))
    division = forms.ChoiceField(label='区分',choices=((0,'Tab譜'),(1,'楽曲')),widget=forms.Select(attrs={'class': 'form-control','placeholder':'区分'}))
    publish = forms.BooleanField(label='公開する',required=False,widget=forms.CheckboxInput(attrs={'class': 'form-check-input','placeholder':'公開する'}))
    class Meta:
        model = Items
        fields = ('title','artist','text','level','price','artwork','tab','music','image','division','publish','volume','url')
        
    def clean(self):
        data = super().clean()
        if not isinstance(data, dict):
            raise forms.ValidationError('入力されたデータが辞書ではありません。')
        
class EmailForm(forms.Form):
    email = forms.EmailField(label='メールアドレス',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'メールアドレス'}))
    confirm_email = forms.EmailField(label='メールアドレス（確認）',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'メールアドレス（確認）'}))
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')
        if email != confirm_email:
            raise forms.ValidationError('メールアドレスが一致しません。')