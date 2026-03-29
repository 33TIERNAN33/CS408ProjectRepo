import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Donor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("anonymous", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Survivor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("contact_info", models.TextField(blank=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True)),
                ("category", models.CharField(blank=True, max_length=80)),
                ("storage_location", models.CharField(blank=True, max_length=120)),
                ("image_path", models.CharField(blank=True, max_length=255)),
                ("status", models.CharField(choices=[("available", "Available"), ("distributed", "Distributed")], default="available", max_length=20)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("assigned_to", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="assigned_items", to="hello.survivor")),
                ("donor", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="items", to="hello.donor")),
            ],
            options={
                "ordering": ["name", "-created_date"],
                "indexes": [
                    models.Index(fields=["name"], name="hello_item_name_933bb1_idx"),
                    models.Index(fields=["status"], name="hello_item_status_c5360e_idx"),
                    models.Index(fields=["created_date"], name="hello_item_created_5e3eff_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(choices=[("public", "Public"), ("donor", "Donor"), ("survivor", "Survivor"), ("volunteer", "Volunteer"), ("staff", "Staff")], default="public", max_length=20)),
                ("is_approved", models.BooleanField(default=False)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "user profile",
                "verbose_name_plural": "user profiles",
                "ordering": ["user__username"],
            },
        ),
        migrations.CreateModel(
            name="ItemRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("request_date", models.DateTimeField(auto_now_add=True)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("approved", "Approved"), ("denied", "Denied")], default="pending", max_length=20)),
                ("item", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="requests", to="hello.item")),
                ("requester", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="item_requests", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-request_date"],
                "indexes": [
                    models.Index(fields=["requester"], name="hello_itemr_request_fdf11f_idx"),
                    models.Index(fields=["item"], name="hello_itemr_item_id_9a61e3_idx"),
                    models.Index(fields=["status"], name="hello_itemr_status_009a74_idx"),
                ],
            },
        ),
    ]
