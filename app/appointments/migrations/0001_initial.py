# Generated by Django 4.1.4 on 2022-12-30 17:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, null=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('status', models.TextField(choices=[('Sc', 'Scheduled'), ('St', 'Started'), ('Co', 'Completed'), ('Re', 'Referred')], default='Sc')),
                ('started', models.DateTimeField(null=True)),
                ('completed', models.DateTimeField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_patient', to='users.user')),
                ('psychologist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_psychologist', to='users.user')),
            ],
        ),
    ]
