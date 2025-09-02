from django import forms
from django.core.exceptions import ValidationError
from .models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'source', 'weight']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        labels = {
            'text': 'Текст цитаты',
            'source': 'Источник',
            'weight': 'Вес',
        }
        error_messages = {
            'text': {
                'unique': 'Цитата с таким текстом уже существует!',
            }
        }
    
    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text and Quote.objects.filter(text__iexact=text).exists():
            raise ValidationError('Цитата с таким текстом уже существует!')
        return text

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get('source')

        if source:
            # Нормализуем текст: убираем кавычки, лишние пробелы, приводим к нижнему регистру
            normalized_source = source.lower().strip().replace('"', '').replace("'", "")

            # Проверяем все существующие источники на схожесть
            existing_sources = Quote.objects.values_list('source', flat=True)
            for existing_source in existing_sources:
                normalized_existing = existing_source.lower().strip().replace('"', '').replace("'", "")
                # Если нормализованные версии совпадают
                if normalized_source == normalized_existing:
                    quote_count = Quote.objects.filter(source=existing_source).count()
                    if quote_count >= 3:
                        raise ValidationError(
                            f'У источника "{existing_source}" уже есть {quote_count} цитат. '
                            'Максимально допустимое количество - 3.'
                        )
                    break

        return cleaned_data
