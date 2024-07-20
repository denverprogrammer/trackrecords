from core.models._ModelStubs import EventBridgeStub
from django.db import models
from django.db.models import signals
from django.dispatch import receiver


@receiver(signals.post_save, sender=models.Model)
def model_post_save(sender, instance: models.Model, created: bool, **kwargs) -> None:
    if not isinstance(instance, EventBridgeStub):
        print('This code runs if instance is not a eventbridge model in post save')
    elif created:
        print("This code runs after a new MyModel instance has been added to the database")
    else:
        print("This code runs after an existing MyModel instance has been updated")
        
@receiver(signals.post_delete, sender=models.Model)
def model_post_delete(sender, instance: models.Model, **kwargs) -> None:
    if not isinstance(instance, EventBridgeStub):
        print('This code runs if instance is not a eventbridge model in post delete')
    else:
        print("This code runs after a model has been deleted")
        
@receiver(signals.m2m_changed, sender=models.Model)
def model_m2m_changed(sender, instance: models.Model, action: str, *args, **kwargs) -> None:
    if not isinstance(instance, EventBridgeStub):
        print('This code runs if instance is not a eventbridge model in post delete')
    if action == 'post_add':
        print("This code runs after a model was added to a relation")
    elif action == 'post_remove':
        print("This code runs after a model was removed from a relation")
    else:
        print("relation changed event, ${action}")
