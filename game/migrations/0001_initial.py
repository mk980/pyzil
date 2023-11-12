# Generated by Django 4.2.6 on 2023-11-12 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnswersSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_answer', models.CharField(max_length=128)),
                ('incorrect_answer1', models.CharField(max_length=128)),
                ('incorrect_answer2', models.CharField(max_length=128)),
                ('incorrect_answer3', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('answer_set', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='game.answersset')),
                ('difficulty_level', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.game')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.question'),
        ),
    ]
