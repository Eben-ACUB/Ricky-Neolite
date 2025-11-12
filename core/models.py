

from django.db import models
from datetime import datetime
from cloudinary.models import CloudinaryField


from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone

from django.utils.safestring import mark_safe

class Courier(models.Model):
    """A full-featured shipment model with DHL-style tracking."""

    TRACKING_SERVICES = [
        ("NeoLite-Logistics", "NeoLite Logistics"),
        ("Comone Express", "Comone Express"),
        ("Direct Freight Express", "Direct Freight Express"),
        ("Dex-i Express", "Dex-i Express"),
        ("UPS Express", "UPS Express"),
        ("ZeptoExpress", "ZeptoExpress"),
        ("Pgeon Delivery", "Pgeon Delivery"),
        ("Roadbull", "Roadbull"),
        ("LWE", "LWE"),
        ("SPC", "SPC"),
        ("DHL Ecommerce", "DHL Ecommerce"),
    ]

    STATUS_CHOICES = [
        ("processing", "Processing"),
        ("in_transit", "In Transit"),
        ("arrived_at_hub", "Arrived at Hub"),
        ("out_for_delivery", "Out for Delivery"),
        ("delivered", "Delivered"),
        ("delayed", "Delayed"),
        ("on_hold", "On Hold"),
        ("returned", "Returned to Sender"),
    ]

    # Core Identifiers
    tracking_id = models.CharField(max_length=255, unique=True, db_index=True)
    service = models.CharField(max_length=50, choices=TRACKING_SERVICES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="processing")

    # Sender Details
    sender_name = models.CharField(max_length=255)
    sender_contact = models.CharField(max_length=100, blank=True)
    sender_address = models.TextField(blank=True)

    # Receiver Details
    receiver_name = models.CharField(max_length=255)
    receiver_contact = models.CharField(max_length=100, blank=True)
    receiver_address = models.TextField(blank=True)

    # Package Details
    quantity = models.PositiveIntegerField(default=1)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    remarks = models.TextField(blank=True, null=True, help_text="Special instructions or notes")

    # Logistics
    current_location = models.CharField(max_length=255, blank=True)
    date_sent = models.DateTimeField(default=timezone.now)
    expected_arrival = models.DateTimeField(blank=True, null=True)
    map_location = models.TextField(blank=True, null=True, help_text="Paste Google Maps iframe URL here")

    # Images
    package_image = CloudinaryField("Package Image", default="https://res.cloudinary.com/demo/image/upload/sample.jpg")
    id_document = CloudinaryField("Receiver ID", default="https://res.cloudinary.com/demo/image/upload/sample.jpg")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"

    def __str__(self):
        return f"{self.tracking_id} - {self.get_status_display()}"

    # Helpers
    def get_tracking_url(self):
        return f"/track/?tracking_id={self.tracking_id}"

    def is_delivered(self):
        return self.status == "delivered"

    def formatted_price(self):
        return f"${self.price_usd:,.2f}"
    @property
    def map_location_iframe(self):
        """Returns the map_location field as safe HTML for templates."""
        if self.map_location:
            return mark_safe(self.map_location)
        return ""