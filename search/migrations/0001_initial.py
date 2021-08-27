# Generated by Django 3.2.6 on 2021-08-27 12:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "voivodeship",
                    models.CharField(
                        choices=[
                            ("dolnośląskie", "D"),
                            ("kujawsko-pomorskie", "C"),
                            ("lubelskie", "L"),
                            ("lubuskie", "F"),
                            ("łódzkie", "E"),
                            ("małopolskie", "K"),
                            ("mazowieckie", "W"),
                            ("opolskie", "O"),
                            ("podkarpackie", "R"),
                            ("podlaskie", "B"),
                            ("pomorskie", "G"),
                            ("śląskie", "S"),
                            ("świętokrzyskie", "T"),
                            ("warmińsko-mazurskie", "N"),
                            ("wielkopolskie", "P"),
                            ("zachodniopomorskie", "Z"),
                        ],
                        max_length=20,
                    ),
                ),
                ("town", models.TextField()),
                (
                    "postcode",
                    models.CharField(
                        blank=True,
                        max_length=6,
                        validators=[
                            django.core.validators.RegexValidator(
                                regex="^\\d\\d-\\d\\d\\d$"
                            )
                        ],
                    ),
                ),
                ("district", models.TextField(blank=True)),
                ("street", models.TextField(blank=True)),
                ("building", models.TextField(blank=True)),
                ("apt", models.TextField(blank=True)),
                ("lng", models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ("lat", models.DecimalField(decimal_places=6, max_digits=9, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="ContactData",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("website", models.TextField(blank=True)),
                ("phone", models.CharField(blank=True, max_length=20)),
                (
                    "email",
                    models.CharField(
                        blank=True,
                        max_length=320,
                        verbose_name=django.core.validators.EmailValidator(),
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LOClass",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("O", "ogólnodostępny"),
                            ("MS", "mistrzostwa sportowego"),
                            ("D", "dwujęzyczny"),
                            ("M", "międzynarodowy"),
                            ("DW", "wstępny"),
                            ("S", "sportowy"),
                            ("I-o", "integracyjny cz. ogólnodostępna"),
                            (
                                "I-i",
                                "integracyjny cz. dla kandydatów z orzeczeniem o potrzebie kształcenia specjalnego",
                            ),
                            ("PW", "przygotowania wojskowego"),
                        ],
                        max_length=3,
                    ),
                ),
                ("name", models.TextField()),
                ("year_start", models.IntegerField()),
                ("year_end", models.IntegerField()),
                ("advanced_subjects", models.JSONField(default=list)),
                ("languages", models.JSONField(default=list)),
            ],
        ),
        migrations.CreateModel(
            name="School",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(unique=True)),
                ("displayed_name", models.TextField(blank=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("liceum ogólnokształcące", "Lo"),
                            ("technikum", "Tech"),
                            ("szkoła branżowa I stopnia", "Bran"),
                            ("szkoła specjalna przysposabiająca do pracy", "Spec"),
                            ("przedszkole", "Przed"),
                            ("szkoła podstawowa", "Sp"),
                            ("szkoła podstawowa artystyczna", "Spart"),
                            ("szkoła policealna", "Polic"),
                        ],
                        max_length=100,
                    ),
                ),
                ("is_public", models.BooleanField()),
                ("is_special_needs_school", models.BooleanField(default=False)),
                ("for_adults", models.BooleanField(default=False)),
                ("data", models.JSONField(default=dict)),
                (
                    "address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="search.address",
                    ),
                ),
                (
                    "contact",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="search.contactdata",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LOStats",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("round", models.IntegerField()),
                ("points_min", models.FloatField()),
                ("points_max", models.FloatField()),
                ("points_avg", models.FloatField()),
                ("with_test", models.BooleanField(default=False)),
                (
                    "lo_class",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="search.loclass"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="loclass",
            name="school",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="search.school"
            ),
        ),
    ]
