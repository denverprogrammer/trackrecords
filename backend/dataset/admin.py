from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Exchange, Market, Security, Symbol


class NamedAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'long_name')
    search_fields = ['short_name', 'long_name']

    def admin_link(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:%s_%s_change' % (obj._meta.app_label,
                    obj._meta.model_name),  args=[obj.id]), obj.short_name,
        )


@admin.register(Exchange)
class ExchangeAdmin(NamedAdmin):
    pass


@admin.register(Market)
class ExchangeAdmin(NamedAdmin):
    pass


@admin.register(Security)
class ExchangeAdmin(NamedAdmin):
    pass


@admin.register(Symbol)
class SymbolAdmin(NamedAdmin, admin.ModelAdmin):
    autocomplete_fields = ['exchange', 'market', 'security']
    list_display = ('short_name', 'long_name',
                    'exchange_link', 'market_link', 'security_link')

    @admin.display(ordering='exchange__short_name', description='exchange')
    def exchange_link(self, obj):
        return self.admin_link(obj.exchange)

    @admin.display(ordering='market__short_name', description='market')
    def market_link(self, obj):
        return self.admin_link(obj.market)

    @admin.display(ordering='security__short_name', description='security')
    def security_link(self, obj):
        return self.admin_link(obj.security)
