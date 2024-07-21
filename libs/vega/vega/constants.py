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
    UNKNOWN = 'unknown'
    LONG = 'long'
    SHORT = 'short'


class ResultType(models.TextChoices):
    UNKNOWN = 'unknown'
    WIN = 'win'
    LOSS = 'loss'
    WASH = 'wash'


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
    PORTFOLIOS = 'portfolios'
    PERMISSIONS = 'permissions'
    SUBSCRIPTIONS = 'subscriptions'
    ORDERS = 'orders'
    POSITIONS = 'positions'
    SECURITIES = 'securities'
    SYMBOLS = 'symbols'


class AppNames(models.TextChoices):
    DATASET = 'dataset'
    TRACKRECORD = 'trackrecord'


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


class ModelClass(models.TextChoices):
    EXCHANGE = 'core.exchange'
    MARKET = 'core.market'
    SECURITY = 'core.security'
    SIC_CODE = 'core.siccode'
    NAICS_CODE = 'core.naicscode'
    PORTFOLIO = 'core.portfolio'
    POSITION = 'core.position'
    ORDER = 'core.order'
    SYMBOL = 'core.symbol'


NO_ACTIONS = []

ALL_ACTIONS = [
    ActionType.CREATE,
    ActionType.UPDATE,
    ActionType.VIEW,
    ActionType.LIST,
    ActionType.DELETE
]

READ_ONLY_ACTIONS = [
    ActionType.VIEW,
    ActionType.LIST
]

NO_CREATE_ACTIONS = [
    ActionType.UPDATE,
    ActionType.VIEW,
    ActionType.LIST,
    ActionType.DELETE
]

NO_DELETE_ACTIONS = [
    ActionType.CREATE,
    ActionType.UPDATE,
    ActionType.VIEW,
    ActionType.LIST
]

NO_CREATE_OR_DELETE_ACTIONS = [
    ActionType.UPDATE,
    ActionType.VIEW,
    ActionType.LIST
]
