from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VaccineData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(choices=[('brasil', 'Brasil'), ('portugal', 'Portugal'), ('italia', 'Itália'), ('usa', 'Estados Unidos')], max_length=20)),
                ('state_or_region', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField()),
                ('vaccinated', models.IntegerField(default=0)),
                ('deaths', models.IntegerField(default=0)),
                ('population', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.AddConstraint(
            model_name='vaccinedata',
            constraint=models.UniqueConstraint(fields=['country', 'state_or_region', 'date'], name='unique_country_state_date'),
        ),
    ]
