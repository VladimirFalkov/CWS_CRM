# Generated by Django 4.2.2 on 2023-07-12 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("team", "0002_plan_team_plan"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="team",
            name="plan",
        ),
    ]
