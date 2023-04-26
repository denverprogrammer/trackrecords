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


class CollectionName(models.TextChoices):
    PORTFOLIO = 'portfolio'
    PERMISSION = 'permission'
    SUBSCRIPTION = 'subscription'

    FILLED_ORDER = 'filled_order'
    PARTIAL_ORDER = 'partial_order'
    PENDING_ORDER = 'pending_order'
    CANCELLED_ORDER = 'cancelled_order'

    OPEN_POSITION = 'open_position'
    CLOSED_POSITION = 'closed_position'


class CollectionGroup(models.TextChoices):
    PORTFOLIO = 'portfolio'
    PERMISSION = 'permission'
    SUBSCRIPTION = 'subscription'
    ORDER = 'order'
    POSITION = 'position'


class RoleType(models.TextChoices):
    OWNER = 'owner'
    ADMIN = 'admin'
    SUBSCRIBER = 'subscriber'
    GUEST = 'guest'


class ActionType(models.TextChoices):
    CREATE = 'create'
    VIEW = 'view'
    LIST = 'list'
    UPDATE = 'update'
    DELETE = 'delete'
