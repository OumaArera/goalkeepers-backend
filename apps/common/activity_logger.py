from django.contrib.contenttypes.models import ContentType
from ..player.models import Activity


def log_activity(
    *,
    user,
    action,
    instance,
    description="",
    metadata=None
):
    """
    Centralized activity logger.
    Safe to call from anywhere.
    """

    # Do not log anonymous/system actions
    if not user or not user.is_authenticated:
        return

    Activity.objects.create(
        user=user,
        action=action,
        content_type=ContentType.objects.get_for_model(instance.__class__),
        object_id=instance.id,
        description=description,
        metadata=metadata or {},
    )

def log_model_activity(user, action, instance):
    log_activity(
        user=user,
        action=action,
        instance=instance,
        description=f"{instance.__class__.__name__} {action.lower()}"
    )
