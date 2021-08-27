from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
from django.db import models

from search.subjects import SubjectName, Language


class Voivodeship(models.TextChoices):
    D = "dolnośląskie"
    C = "kujawsko-pomorskie"
    L = "lubelskie"
    F = "lubuskie"
    E = "łódzkie"
    K = "małopolskie"
    W = "mazowieckie"
    O = "opolskie"
    R = "podkarpackie"
    B = "podlaskie"
    G = "pomorskie"
    S = "śląskie"
    T = "świętokrzyskie"
    N = "warmińsko-mazurskie"
    P = "wielkopolskie"
    Z = "zachodniopomorskie"


class Address(models.Model):
    voivodeship = models.CharField(max_length=20, choices=Voivodeship.choices)
    town = models.TextField()
    postcode = models.CharField(
        max_length=6,
        validators=[RegexValidator(regex="^\\d\\d-\\d\\d\\d$")],
        blank=True,
    )
    district = models.TextField(blank=True)
    street = models.TextField(blank=True)
    building = models.TextField(blank=True)
    apt = models.TextField(blank=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    def __str__(self):
        return f"{self.town} {self.street} {self.building} {self.postcode}"


class ContactData(models.Model):
    website = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.CharField(EmailValidator(), max_length=320, blank=True)

    def __str__(self):
        return f"web: {self.website}, tel: {self.phone}, e-mail: {self.email}"


class SchoolType(models.TextChoices):
    LO = "liceum ogólnokształcące"
    TECH = "technikum"
    BRAN = "szkoła branżowa I stopnia"
    SPEC = "szkoła specjalna przysposabiająca do pracy"
    PRZED = "przedszkole"
    SP = "szkoła podstawowa"
    SPART = "szkoła podstawowa artystyczna"
    POLIC = "szkoła policealna"


class School(models.Model):
    name = models.TextField(unique=True)  # full school name
    displayed_name = models.TextField(
        blank=True
    )  # displayed name with eg. abbreviations
    type = models.CharField(max_length=100, choices=SchoolType.choices)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True
    )
    contact = models.ForeignKey(
        ContactData, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_public = models.BooleanField()
    is_special_needs_school = models.BooleanField(default=False)
    for_adults = models.BooleanField(default=False)
    data = models.JSONField(default=dict)

    def __str__(self):
        return self.displayed_name if self.displayed_name else self.name


class LOClassType(models.TextChoices):
    O = "O", "ogólnodostępny"
    MS = "MS", "mistrzostwa sportowego"
    D = "D", "dwujęzyczny"
    M = "M", "międzynarodowy"
    DW = "DW", "wstępny"
    S = "S", "sportowy"
    IO = "I-o", "integracyjny cz. ogólnodostępna"
    II = (
        "I-i",
        "integracyjny cz. dla kandydatów z orzeczeniem o potrzebie kształcenia specjalnego",
    )
    PW = "PW", "przygotowania wojskowego"


class LOClass(models.Model):
    type = models.CharField(choices=LOClassType.choices, max_length=3)
    name = models.TextField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    year_start = models.IntegerField()
    year_end = models.IntegerField()
    advanced_subjects = models.JSONField(default=list)
    languages = models.JSONField(default=list)

    def _validate_languages(self):
        for value in self.languages:
            Language.from_dict(value)

    def _validate_subjects(self):
        for value in self.advanced_subjects:
            if value not in SubjectName.values():
                raise ValidationError(
                    f"Value: {value} is not one of: {SubjectName.values()}."
                )

    def clean(self):
        self._validate_languages()
        self._validate_subjects()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class LOStats(models.Model):
    lo_class = models.ForeignKey(LOClass, on_delete=models.CASCADE)
    round = models.IntegerField()  # tura rekrutacji
    points_min = models.FloatField()
    points_max = models.FloatField()
    points_avg = models.FloatField()
    with_test = models.BooleanField(default=False)
