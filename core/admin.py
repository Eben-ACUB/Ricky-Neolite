from django.contrib import admin

# Register your models here.


from .models import Courier

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    """Enhanced admin for managing courier shipments with modern UX and powerful features."""
    
    # List Display with Visual Enhancements
    list_display = (
        "tracking_id_display",
        "service_badge",
        "status_badge",
        "sender_receiver",
        "weight_quantity",
        "current_location_short",
        "timeline_display",
        "price_display",
    )
    
    # Advanced Filtering
    list_filter = (
        "service",
        "status",
        "date_sent",
        "expected_arrival",
    )
    
    # Enhanced Search
    search_fields = (
        "tracking_id",
        "sender_name",
        "sender_contact",
        "receiver_name",
        "receiver_contact",
        "current_location",
        "remarks",
    )
    
    # Date Hierarchy for easy navigation
    date_hierarchy = "date_sent"
    
    # Ordering
    ordering = ("-date_sent", "-created_at")
    
    # Read-only fields
    readonly_fields = (
        "created_at",
        "updated_at",
        "package_preview",
        "id_document_preview",
        "map_preview",
        "shipment_summary",
    )
    
    # Actions per page
    list_per_page = 25
    list_max_show_all = 100
    
    # Enable actions on top and bottom
    actions_on_top = True
    actions_on_bottom = True
    
    # Save options
    save_on_top = True
    
    # Organized Fieldsets with descriptions
    fieldsets = (
        ("📦 Shipment Information", {
            "description": "Core tracking and service details for this shipment",
            "fields": (
                "tracking_id",
                "service",
                "status",
                "shipment_summary",
            ),
        }),
        ("📤 Sender Details", {
            "description": "Information about the person or organization sending the package",
            "fields": (
                "sender_name",
                "sender_contact",
                "sender_address",
            ),
        }),
        ("📥 Receiver Details", {
            "description": "Information about the person or organization receiving the package",
            "fields": (
                "receiver_name",
                "receiver_contact",
                "receiver_address",
            ),
        }),
        ("📊 Package Specifications", {
            "description": "Physical characteristics and value of the shipment",
            "fields": (
                "quantity",
                "weight_kg",
                "price_usd",
                "remarks",
            ),
            "classes": ("collapse",),
        }),
        ("🗺️ Location & Tracking", {
            "description": "Current location and delivery timeline",
            "fields": (
                "current_location",
                "date_sent",
                "expected_arrival",
                "map_location",
                "map_preview",
            ),
        }),
        ("🖼️ Documentation", {
            "description": "Package photo and identification documents",
            "fields": (
                "package_image",
                "package_preview",
                "id_document",
                "id_document_preview",
            ),
            "classes": ("collapse",),
        }),
        ("🕒 System Timestamps", {
            "description": "Automatic record creation and modification times",
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )
    
    # Custom Actions
    actions = [
        "mark_as_in_transit",
        "mark_as_delivered",
        "mark_as_pending",
        "duplicate_shipments",
        "clear_expected_arrival",
    ]
    
    # ============= Custom Display Methods =============
    
    @admin.display(description="Tracking ID", ordering="tracking_id")
    def tracking_id_display(self, obj):
        """Display tracking ID with copy button."""
        return format_html(
            '<code style="background: #f0f0f0; padding: 4px 8px; border-radius: 4px; '
            'font-weight: bold; color: #2c3e50;">{}</code>',
            obj.tracking_id
        )
    
    @admin.display(description="Service", ordering="service")
    def service_badge(self, obj):
        """Display service type with colored badge."""
        colors = {
            "standard": "#6c757d",
            "express": "#007bff",
            "overnight": "#dc3545",
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold; '
            'text-transform: uppercase;">{}</span>',
            colors.get(obj.service, "#6c757d"),
            obj.get_service_display()
        )
    
    @admin.display(description="Status", ordering="status")
    def status_badge(self, obj):
        """Display status with colored badge and icon."""
        status_config = {
            "pending": ("#ffc107", "⏳"),
            "in_transit": ("#17a2b8", "🚚"),
            "delivered": ("#28a745", "✓"),
        }
        color, icon = status_config.get(obj.status, ("#6c757d", "●"))
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-size: 11px; font-weight: bold; '
            'text-transform: uppercase;">{} {}</span>',
            color,
            icon,
            obj.get_status_display()
        )
    
    @admin.display(description="Location")
    def current_location_short(self, obj):
        """Display current location with truncation."""
        location = obj.current_location
        if len(location) > 30:
            return format_html(
                '<span title="{}">{}</span>',
                location,
                location[:30] + "..."
            )
        return location
    
    @admin.display(description="Price")
    def price_display(self, obj):
        """Display price with currency symbol."""
        return format_html(
            '<strong style="color: #28a745;">${}</strong>',
            obj.price_usd
        )
    
    @admin.display(description="Sender → Receiver")
    def sender_receiver(self, obj):
        """Display sender and receiver in compact format."""
        return format_html(
            '<div style="line-height: 1.4;">'
            '<strong style="color: #2c3e50;">📤 {}</strong><br>'
            '<span style="color: #6c757d;">↓</span><br>'
            '<strong style="color: #2c3e50;">📥 {}</strong>'
            '</div>',
            obj.sender_name[:20] + "..." if len(obj.sender_name) > 20 else obj.sender_name,
            obj.receiver_name[:20] + "..." if len(obj.receiver_name) > 20 else obj.receiver_name
        )
    
    @admin.display(description="Weight / Qty")
    def weight_quantity(self, obj):
        """Display weight and quantity combined."""
        return format_html(
            '<div style="text-align: center;">'
            '<strong style="color: #667eea; font-size: 13px;">{} kg</strong><br>'
            '<span style="color: #6c757d; font-size: 11px;">{} item(s)</span>'
            '</div>',
            obj.weight_kg,
            obj.quantity
        )
    
    @admin.display(description="Timeline", ordering="date_sent")
    def timeline_display(self, obj):
        """Display date sent and expected arrival."""
        expected = obj.expected_arrival if obj.expected_arrival else '<em style="color: #dc3545;">TBD</em>'
        return format_html(
            '<div style="font-size: 12px; line-height: 1.5;">'
            '<strong>Sent:</strong> {}<br>'
            '<strong>ETA:</strong> {}'
            '</div>',
            obj.date_sent.strftime("%b %d, %Y"),
            expected if isinstance(expected, str) else expected.strftime("%b %d, %Y")
        )
    
    @admin.display(description="Shipment Overview")
    def shipment_summary(self, obj):
        """Display comprehensive shipment summary card."""
        if not obj.pk:
            return "Save to see summary"
        
        return format_html(
            '<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
            'padding: 20px; border-radius: 12px; color: white; margin: 10px 0;">'
            '<h3 style="margin: 0 0 15px 0; font-size: 18px;">📦 Shipment Summary</h3>'
            '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">'
            '<div><strong>From:</strong><br>{}</div>'
            '<div><strong>To:</strong><br>{}</div>'
            '<div><strong>Weight:</strong><br>{} kg</div>'
            '<div><strong>Quantity:</strong><br>{} item(s)</div>'
            '<div><strong>Value:</strong><br>${}</div>'
            '<div><strong>Status:</strong><br>{}</div>'
            '</div></div>',
            obj.sender_name,
            obj.receiver_name,
            obj.weight_kg,
            obj.quantity,
            obj.price_usd,
            obj.get_status_display()
        )
    
    @admin.display(description="Package Image")
    def package_preview(self, obj):
        """Display package image preview."""
        if obj.package_image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; '
                'border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.package_image.url
            )
        return format_html('<em style="color: #999;">No image uploaded</em>')
    
    @admin.display(description="ID Document")
    def id_document_preview(self, obj):
        """Display ID document preview."""
        if obj.id_document:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; '
                'border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.id_document.url
            )
        return format_html('<em style="color: #999;">No document uploaded</em>')
    
    @admin.display(description="Map Location")
    def map_preview(self, obj):
        """Display embedded map preview."""
        if obj.map_location:
            return format_html(
                '<div style="border-radius: 8px; overflow: hidden; '
                'box-shadow: 0 2px 8px rgba(0,0,0,0.1);">{}</div>',
                obj.map_location_iframe
            )
        return format_html('<em style="color: #999;">No map location set</em>')
    
    # ============= Custom Actions =============
    
    @admin.action(description="✓ Mark selected as In Transit")
    def mark_as_in_transit(self, request, queryset):
        """Mark selected shipments as in transit."""
        updated = queryset.update(status="in_transit")
        self.message_user(
            request,
            f"{updated} shipment(s) marked as In Transit.",
            level="success"
        )
    
    @admin.action(description="✓ Mark selected as Delivered")
    def mark_as_delivered(self, request, queryset):
        """Mark selected shipments as delivered."""
        updated = queryset.update(status="delivered")
        self.message_user(
            request,
            f"{updated} shipment(s) marked as Delivered.",
            level="success"
        )
    
    @admin.action(description="⏳ Mark selected as Pending")
    def mark_as_pending(self, request, queryset):
        """Mark selected shipments as pending."""
        updated = queryset.update(status="pending")
        self.message_user(
            request,
            f"{updated} shipment(s) marked as Pending.",
            level="warning"
        )
    
    @admin.action(description="📋 Duplicate selected shipments")
    def duplicate_shipments(self, request, queryset):
        """Duplicate selected shipments with new tracking IDs."""
        import uuid
        count = 0
        for shipment in queryset:
            shipment.pk = None
            shipment.tracking_id = str(uuid.uuid4())[:12].upper()
            shipment.status = "pending"
            shipment.save()
            count += 1
        
        self.message_user(
            request,
            f"{count} shipment(s) duplicated successfully with new tracking IDs.",
            level="success"
        )
    
    @admin.action(description="🗓️ Clear expected arrival dates")
    def clear_expected_arrival(self, request, queryset):
        """Clear expected arrival dates for selected shipments."""
        updated = queryset.update(expected_arrival=None)
        self.message_user(
            request,
            f"Expected arrival cleared for {updated} shipment(s).",
            level="warning"
        )
    
    # ============= QuerySet Optimization =============
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        qs = super().get_queryset(request)
        return qs.select_related()
    
    # ============= Custom Styling =============
    
    class Media:
        css = {
            "all": (
                "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css",
            )
        }
        js = ()
    
    # ============= Form Customization =============
    
    def get_form(self, request, obj=None, **kwargs):
        """Customize form with help text and enhanced widgets."""
        form = super().get_form(request, obj, **kwargs)
        
        # Add comprehensive help text to fields
        help_texts = {
            "tracking_id": "🔖 Unique tracking identifier. Auto-generated if left blank. Can be customized.",
            "service": "🚚 Choose the delivery speed: Standard (3-7 days), Express (1-2 days), or Overnight (next day)",
            "status": "📊 Current shipment status: Pending → In Transit → Delivered",
            "sender_name": "👤 Full name of the person or company sending the package",
            "sender_contact": "📞 Phone number or email of the sender",
            "sender_address": "📍 Complete pickup address including street, city, state, and postal code",
            "receiver_name": "👤 Full name of the person or company receiving the package",
            "receiver_contact": "📞 Phone number or email of the receiver",
            "receiver_address": "📍 Complete delivery address including street, city, state, and postal code",
            "quantity": "📦 Number of packages/items in this shipment",
            "weight_kg": "⚖️ Total weight of all packages in kilograms (e.g., 2.5 for 2.5kg)",
            "price_usd": "💰 Declared value of the shipment contents in USD",
            "remarks": "📝 Additional notes, special handling instructions, or package contents description",
            "current_location": "📍 Current location of the package (e.g., 'Chicago Distribution Center' or 'Out for delivery')",
            "date_sent": "📅 Date when the package was picked up or shipped",
            "expected_arrival": "🎯 Estimated delivery date (leave blank if unknown or to be determined)",
            "map_location": "🗺️ Paste Google Maps embed URL or iframe code to show current location",
            "package_image": "📷 Photo of the package for identification and verification",
            "id_document": "🪪 ID document of sender or receiver for security verification",
        }
        
        for field_name, help_text in help_texts.items():
            if field_name in form.base_fields:
                form.base_fields[field_name].help_text = help_text
        
        # Enhance textarea widgets
        if "remarks" in form.base_fields:
            form.base_fields["remarks"].widget.attrs.update({
                'rows': 4,
                'style': 'width: 100%; font-family: inherit;',
                'placeholder': 'Enter any special instructions, package contents, or additional notes...'
            })
        
        if "sender_address" in form.base_fields:
            form.base_fields["sender_address"].widget.attrs.update({
                'rows': 3,
                'placeholder': 'Street Address, City, State, Postal Code'
            })
        
        if "receiver_address" in form.base_fields:
            form.base_fields["receiver_address"].widget.attrs.update({
                'rows': 3,
                'placeholder': 'Street Address, City, State, Postal Code'
            })
        
        if "current_location" in form.base_fields:
            form.base_fields["current_location"].widget.attrs.update({
                'placeholder': 'e.g., New York Distribution Center, In Transit to Los Angeles'
            })
        
        if "map_location" in form.base_fields:
            form.base_fields["map_location"].widget.attrs.update({
                'rows': 4,
                'placeholder': 'Paste Google Maps embed code here (e.g., <iframe src="..." ></iframe>)'
            })
        
        return form
    
    # ============= Save Notification =============
    
    def save_model(self, request, obj, form, change):
        """Save with custom notification."""
        super().save_model(request, obj, form, change)
        
        if change:
            self.message_user(
                request,
                f"Shipment {obj.tracking_id} updated successfully! ✓",
                level="success"
            )
        else:
            self.message_user(
                request,
                f"New shipment {obj.tracking_id} created successfully! 🎉",
                level="success"
            )