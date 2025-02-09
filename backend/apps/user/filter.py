from django_filters import rest_framework as filters

from apps.user.serializers import UserSerializer


class UserFilter(filters.FilterSet):
    first_name_starts_with = filters.CharFilter(field_name='profile__first_name', lookup_expr='startswith')
    first_name_ends_with = filters.CharFilter(field_name='profile__first_name', lookup_expr='endswith')
    first_name_contains = filters.CharFilter(field_name='profile__first_name', lookup_expr='contains')

    last_name_starts_with = filters.CharFilter(field_name='profile__last_name', lookup_expr='startswith')
    last_name_ends_with = filters.CharFilter(field_name='profile__last_name', lookup_expr='endswith')
    last_name_contains = filters.CharFilter(field_name='profile__last_name', lookup_expr='contains')

    email_contains = filters.CharFilter(field_name='email', lookup_expr='contains')

    age_gt = filters.NumberFilter(field_name='profile__age', lookup_expr='gt')
    age_gte = filters.NumberFilter(field_name='profile__age', lookup_expr='gte')
    age_lt = filters.NumberFilter(field_name='profile__age', lookup_expr='lt')
    age_lte = filters.NumberFilter(field_name='profile__age', lookup_expr='lte')

    order = filters.OrderingFilter(
        fields=UserSerializer.Meta.fields
    )
