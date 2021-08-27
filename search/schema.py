from graphene import ObjectType, relay, Schema
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from search.models import (
    School,
    Address,
    ContactData,
    LOClass,
)


class ContactDataNode(DjangoObjectType):
    class Meta:
        model = ContactData
        fields = ("website", "phone", "email")
        filter_fields = ("website", "phone", "email")
        interfaces = (relay.Node,)


class AddressNode(DjangoObjectType):
    class Meta:
        model = Address
        fields = (
            "voivodeship",
            "town",
            "postcode",
            "street",
            "district",
            "building",
            "apt",
            "lng",
            "lat",
        )
        filter_fields = (
            "voivodeship",
            "town",
            "postcode",
            "street",
            "district",
            "building",
            "apt",
            "lng",
            "lat",
        )
        interfaces = (relay.Node,)


class LOClassNode(DjangoObjectType):
    class Meta:
        model = LOClass
        fields = (
            "type",
            "name",
            "school",
            "year_start",
            "year_end",
            "advanced_subjects",
            "languages",
        )
        filter_fields = ("type", "name", "school", "year_start", "year_end")
        interfaces = (relay.Node,)


class SchoolNode(DjangoObjectType):
    class Meta:
        model = School
        fields = (
            "name",
            "displayed_name",
            "type",
            "address",
            "contact",
            "is_public",
            "is_special_needs_school",
            "for_adults",
            "data",
        )
        filter_fields = (
            "name",
            "displayed_name",
            "type",
            "address",
            "contact",
            "is_public",
            "is_special_needs_school",
            "for_adults",
        )
        interfaces = (relay.Node,)


class Query(ObjectType):
    address = relay.Node.Field(AddressNode)
    contact = relay.Node.Field(ContactDataNode)

    school = relay.node.Field(SchoolNode)
    all_schools = DjangoFilterConnectionField(SchoolNode)

    lo_class = relay.Node.Field(LOClassNode)
    all_lo_classes = DjangoFilterConnectionField(LOClassNode)


schema = Schema(query=Query)
