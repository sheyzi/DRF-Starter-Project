# Generated by Django 4.2.7 on 2024-02-21 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_verificationtoken_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlacklistedToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=500)),
                ('blacklisted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='VerificationToken',
        ),
    ]
