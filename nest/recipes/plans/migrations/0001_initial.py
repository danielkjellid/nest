# Generated by Django 4.2.7 on 2024-06-14 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('homes', '0001_initial'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipePlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='modified time')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField()),
                ('from_date', models.DateTimeField(blank=True, null=True)),
                ('home', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='homes.home')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RecipePlanItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='modified time')),
                ('ordering', models.PositiveIntegerField(verbose_name='ordering')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_items', to='recipes.recipe')),
                ('recipe_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_items', to='recipes_plans.recipeplan')),
            ],
            options={
                'ordering': ('ordering',),
            },
        ),
    ]
