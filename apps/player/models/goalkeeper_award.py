# import uuid
# from django.db import models
# from ..models.player import Player


# class GoalkeeperAwardEvent(models.Model):
#     class Status(models.TextChoices):
#         DRAFT = "Draft", "Draft"
#         OPEN = "Open", "Open"
#         CLOSED = "Closed", "Closed"

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)

#     event_date = models.DateField()
#     venue = models.CharField(max_length=255, blank=True)

#     status = models.CharField(
#         max_length=10,
#         choices=Status.choices,
#         default=Status.DRAFT
#     )

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ["-event_date"]

#     def __str__(self):
#         return self.title



# class GoalkeeperAwardCategory(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

#     event = models.ForeignKey(
#         GoalkeeperAwardEvent,
#         on_delete=models.CASCADE,
#         related_name="categories"
#     )

#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True)

#     criteria = models.TextField(
#         help_text="Award criteria / parameters"
#     )

#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ["event", "name"]
#         ordering = ["name"]

#     def __str__(self):
#         return f"{self.name} ({self.event.title})"



# class GoalkeeperAwardNomination(models.Model):
#     class Status(models.TextChoices):
#         PENDING = "Pending", "Pending"
#         APPROVED = "Approved", "Approved"
#         REJECTED = "Rejected", "Rejected"

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

#     category = models.ForeignKey(
#         GoalkeeperAwardCategory,
#         on_delete=models.CASCADE,
#         related_name="nominations"
#     )

#     player = models.ForeignKey(
#         Player,
#         on_delete=models.CASCADE,
#         related_name="award_nominations"
#     )

#     justification = models.TextField(blank=True)

#     status = models.CharField(
#         max_length=10,
#         choices=Status.choices,
#         default=Status.PENDING
#     )

#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ["category", "player"]

#     def __str__(self):
#         return f"{self.player} - {self.category.name}"



# class GoalkeeperAwardWinner(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

#     nomination = models.OneToOneField(
#         GoalkeeperAwardNomination,
#         on_delete=models.CASCADE,
#         related_name="winner"
#     )

#     awarded_at = models.DateTimeField(auto_now_add=True)

#     approved_by = models.ForeignKey(
#         "auth.User",
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )

#     class Meta:
#         ordering = ["-awarded_at"]

#     def __str__(self):
#         return f"Winner: {self.nomination.player}"

