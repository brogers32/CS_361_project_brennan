# Generated by Django 4.2.7 on 2023-12-13 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('course_name', models.CharField(max_length=255)),
                ('course_description', models.CharField(max_length=1000)),
                ('course_code', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('section_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('section_type', models.CharField(max_length=50)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supercreative.course')),
            ],
        ),
        migrations.CreateModel(
            name='SectionType',
            fields=[
                ('section_type_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('section_type_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=255)),
                ('skills', models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('role_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('role_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserCourseAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supercreative.course')),
                ('section_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='supercreative.section')),
                ('section_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='supercreative.sectiontype')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supercreative.user')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='role_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='supercreative.userrole'),
        ),
    ]
