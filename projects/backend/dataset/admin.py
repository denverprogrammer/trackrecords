from django.contrib import admin
from django.urls import reverse
from django.utils import safestring
from django.utils.html import format_html
from more_admin_filters import RelatedDropdownFilter
from vega.models import Exchange, Market, NaicsCode, Security, SicCode, Symbol


class NamedAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ['code', 'description']

    def admin_link(self, obj) -> safestring.SafeText | None:
        return format_html(
            '<a href="{}" title="{}">{}</a>',
            reverse('admin:%s_%s_change' % (obj._meta.app_label,
                    obj._meta.model_name),  args=[obj.id]),
            obj.description,
            obj.code,
        )


@admin.register(NaicsCode)
class NaicsAdmin(NamedAdmin):
    pass


@admin.register(SicCode)
class SicAdmin(NamedAdmin):
    pass


@admin.register(Exchange)
class ExchangeAdmin(NamedAdmin):
    pass


@admin.register(Market)
class MarketAdmin(NamedAdmin):
    pass


@admin.register(Security)
class SecurityAdmin(NamedAdmin):
    pass


@admin.register(Symbol)
class SymbolAdmin(NamedAdmin, admin.ModelAdmin):
    list_per_page = 25
    autocomplete_fields = ['exchange', 'market', 'security', 'naics', 'sic']
    list_display = (
        'code',
        'description',
        'exchange_link',
        'market_link',
        'security_link',
        'sic_link',
        'frontmonth',
        'naics_link'
    )

    list_filter = (
        ('exchange', RelatedDropdownFilter),
        ('market', RelatedDropdownFilter),
        ('security', RelatedDropdownFilter),
    )

    list_select_related = [
        'exchange',
        'market',
        'security',
        'naics',
        'sic'
    ]

    @admin.display(ordering='naics__code', description='NAICS')
    def naics_link(self, obj) -> safestring.SafeText | None:
        return self.admin_link(obj.naics) if obj and obj.naics else None

    @admin.display(ordering='sic__code', description='SIC')
    def sic_link(self, obj) -> safestring.SafeText | None:
        return self.admin_link(obj.sic) if obj and obj.sic else None

    @admin.display(ordering='exchange__code', description='exchange')
    def exchange_link(self, obj) -> safestring.SafeText | None:
        return self.admin_link(obj.exchange) if obj.exchange else None

    @admin.display(ordering='market__code', description='market')
    def market_link(self, obj) -> safestring.SafeText | None:
        return self.admin_link(obj.market) if obj.market else None

    @admin.display(ordering='security__code', description='security')
    def security_link(self, obj) -> safestring.SafeText | None:
        return self.admin_link(obj.security) if obj.security else None
