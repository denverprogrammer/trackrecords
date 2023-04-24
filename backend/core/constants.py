from django.db import models


class OrderType(models.TextChoices):
    MARKET = 'market'
    LIMIT = 'limit'
    STOP = 'stop'
    STOP_LIMIT = 'stop-limit'


class OrderAction(models.TextChoices):
    BUY = 'buy'
    SELL = 'sell'


class OrderStatus(models.TextChoices):
    PENDING = 'pending'
    PARTIAL = 'partial'
    FILLED = 'filled'
    CANCELLED = 'cancelled'


class TrendType(models.TextChoices):
    LONG = 'long'
    SHORT = 'short'


class PositionStatus(models.TextChoices):
    OPEN = 'open'
    CLOSED = 'closed'


class EntryType(models.TextChoices):
    MANUAL = 'manual'
    AUTO_SYNC = 'auto_sync'


class RecordType(models.TextChoices):
    ORDER = 'order'
    POSITION = 'position'
