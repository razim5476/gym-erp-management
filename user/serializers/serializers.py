"""
User serializers.
"""

import uuid

from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers

from core.models import Country, State
from core.utils import generate_unique_id
from user.models import (
    Address,
    Attendance,
    Gallery,
    LoginLog,
    Permission,
    Role,
    Trainer,
    User,
    UserProfile,
)


ID_PREFIXES = {
    "User": "USER",
    "LoginLog": "LOGIN",
    "Address": "ADDR",
    "Attendance": "ATT",
    "Role": "ROLE",
    "Permission": "PERM",
}


def make_model_id(model_name, prefix, request=None):
    """
    Generate a branch based id when possible, otherwise use a compact uuid.
    """

    user = getattr(request, "user", None)
    branch = getattr(user, "branch", None)
    created_by = getattr(user, "id", None)

    if branch:
        value = generate_unique_id(
            branch=branch,
            model_name=model_name,
            string=prefix,
            created_by=created_by,
        )
        if value:
            return value

    return f"{prefix}-{uuid.uuid4().hex[:10].upper()}"


class AuditModelSerializer(serializers.ModelSerializer):
    """
    Base serializer for models using CustomModel fields.
    """

    def _stamp_create(self, validated_data):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if user and user.is_authenticated:
            validated_data.setdefault("created_by", user)

        return validated_data

    def _stamp_update(self, validated_data):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if user and user.is_authenticated:
            validated_data["updated_by"] = user

        return validated_data


class CombinedMembershipSerializer(serializers.Serializer):
    """
    Serializer combined with User, Address and UserProfile models.
    """

    user_id = serializers.CharField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    joined_date = serializers.DateTimeField(required=False, read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    height = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    weight = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    email = serializers.EmailField()
    phone_number = serializers.CharField()

    address_id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    address_type = serializers.ChoiceField(
        choices=Address.ADDRESS_TYPES,
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    address_line_1 = serializers.CharField()
    address_line_2 = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )
    address_line_3 = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )
    city = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    pincode = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.filter(is_active=True)
    )
    state = serializers.PrimaryKeyRelatedField(
        queryset=State.objects.filter(is_active=True)
    )
    latitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
        required=False,
        allow_null=True,
    )
    longitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6,
        required=False,
        allow_null=True,
    )

    bio = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    level = serializers.ChoiceField(choices=UserProfile.LEVEL_CHOICES, default=1)
    blood_group = serializers.ChoiceField(
        choices=UserProfile.BLOOD_GROUP_CHOICES,
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    def _get_request_user(self):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            return request.user
        return None

    def _get_request_branch(self):
        user = self._get_request_user()
        branch = getattr(user, "branch", None)

        if not branch:
            raise serializers.ValidationError({
                "branch": "Logged-in user does not have a branch assigned."
            })

        return branch

    def validate_email(self, value):
        queryset = User.objects.filter(email=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("User with this email already exists.")

        return value

    def validate_phone_number(self, value):
        queryset = User.objects.filter(phone_number=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "User with this phone number already exists."
            )

        return value

    def _split_validated_data(self, validated_data):
        address_fields = [
            "name", "address_type", "address_line_1", "address_line_2",
            "address_line_3", "city", "pincode", "country", "state",
            "latitude", "longitude",
        ]
        profile_fields = ["bio", "level", "blood_group"]

        address_data = {
            field: validated_data.pop(field)
            for field in address_fields
            if field in validated_data
        }
        profile_data = {
            field: validated_data.pop(field)
            for field in profile_fields
            if field in validated_data
        }

        return validated_data, address_data, profile_data

    @transaction.atomic
    def create(self, validated_data):
        user_data, address_data, profile_data = self._split_validated_data(
            validated_data
        )
        request = self.context.get("request")
        created_by = self._get_request_user()
        branch = self._get_request_branch()

        user = User.objects.create(
            user_id=make_model_id("User", "MEM", request),
            company=getattr(created_by, "company", None),
            branch=branch,
            **user_data,
        )

        Address.objects.create(
            address_id=make_model_id("Address", "ADDR", request),
            user=user,
            created_by=created_by,
            **address_data,
        )

        UserProfile.objects.create(
            user=user,
            created_by=created_by,
            **profile_data,
        )

        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        user_data, address_data, profile_data = self._split_validated_data(
            validated_data
        )
        updated_by = self._get_request_user()

        for field, value in user_data.items():
            setattr(instance, field, value)
        instance.save()

        address = instance.user_address.first()
        if address is None and address_data:
            address = Address(
                address_id=make_model_id(
                    "Address",
                    "ADDR",
                    self.context.get("request"),
                ),
                user=instance,
                created_by=updated_by,
            )

        if address:
            for field, value in address_data.items():
                setattr(address, field, value)
            address.updated_by = updated_by
            address.save()

        profile, _ = UserProfile.objects.get_or_create(
            user=instance,
            defaults={"created_by": updated_by},
        )
        for field, value in profile_data.items():
            setattr(profile, field, value)
        profile.updated_by = updated_by
        profile.save()

        return instance

    def to_representation(self, instance):
        address = instance.user_address.first()
        profile = getattr(instance, "user_profile", None)

        return {
            "id": instance.id,
            "user_id": instance.user_id,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "date_of_birth": self.fields["date_of_birth"].to_representation(
                instance.date_of_birth
            ),
            "joined_date": self.fields["joined_date"].to_representation(
                instance.joined_date
            ),
            "image": instance.image.url if instance.image else None,
            "height": instance.height,
            "weight": instance.weight,
            "email": instance.email,
            "phone_number": instance.phone_number,
            "address_id": address.address_id if address else None,
            "name": address.name if address else None,
            "address_type": address.address_type if address else None,
            "address_line_1": address.address_line_1 if address else None,
            "address_line_2": address.address_line_2 if address else None,
            "address_line_3": address.address_line_3 if address else None,
            "city": address.city if address else None,
            "pincode": address.pincode if address else None,
            "country": address.country_id if address else None,
            "state": address.state_id if address else None,
            "latitude": self.fields["latitude"].to_representation(
                address.latitude
            ) if address else None,
            "longitude": self.fields["longitude"].to_representation(
                address.longitude
            ) if address else None,
            "bio": profile.bio if profile else None,
            "level": profile.level if profile else None,
            "blood_group": profile.blood_group if profile else None,
        }


MemberSerializer = CombinedMembershipSerializer
MemberSerialzier = MemberSerializer


class LoginSerializer(serializers.Serializer):
    """
    Login serializer that accepts username or email.
    """

    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username") or attrs.get("email")
        password = attrs.get("password")

        if not username:
            raise serializers.ValidationError("Username or email is required.")

        user_obj = User.objects.filter(email=username).first()
        username = user_obj.username if user_obj else username
        user = authenticate(
            request=self.context.get("request"),
            username=username,
            password=password,
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        if not user.is_active:
            raise serializers.ValidationError("User account is inactive.")

        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer.
    """

    class Meta:
        model = User
        fields = [
            "id", "user_id", "first_name", "last_name", "username",
            "password", "date_of_birth", "joined_date", "image", "height",
            "weight", "email", "phone_number", "is_active", "role",
            "company", "branch", "is_staff", "is_superuser", "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id", "user_id", "joined_date", "created_at", "updated_at",
            "is_superuser",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "username": {"required": False},
            "role": {"required": False},
        }

    def create(self, validated_data):
        roles = validated_data.pop("role", [])
        password = validated_data.pop("password", None)
        request = self.context.get("request")

        validated_data.setdefault(
            "user_id",
            make_model_id("User", ID_PREFIXES["User"], request),
        )
        validated_data.setdefault(
            "username",
            validated_data.get("email") or validated_data["user_id"],
        )

        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()

        if roles:
            user.role.set(roles)

        return user

    def update(self, instance, validated_data):
        roles = validated_data.pop("role", None)
        password = validated_data.pop("password", None)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        if password:
            instance.set_password(password)

        instance.save()

        if roles is not None:
            instance.role.set(roles)

        return instance


class LoginLogSerializer(AuditModelSerializer):
    """
    Login log serializer.
    """

    class Meta:
        model = LoginLog
        fields = [
            "id", "login_log_id", "user", "description", "is_active",
            "created_at", "created_by", "updated_at", "updated_by",
        ]
        read_only_fields = [
            "id", "login_log_id", "is_active", "created_at", "created_by",
            "updated_at", "updated_by",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data.setdefault(
            "login_log_id",
            make_model_id("LoginLog", ID_PREFIXES["LoginLog"], request),
        )
        return super().create(self._stamp_create(validated_data))

    def update(self, instance, validated_data):
        return super().update(instance, self._stamp_update(validated_data))


class AddressSerializer(AuditModelSerializer):
    """
    Address serializer.
    """

    class Meta:
        model = Address
        fields = [
            "id", "address_id", "name", "address_type", "address_line_1",
            "address_line_2", "address_line_3", "city", "pincode",
            "country", "state", "latitude", "longitude", "user",
            "is_active", "created_at", "created_by", "updated_at",
            "updated_by",
        ]
        read_only_fields = [
            "id", "address_id", "is_active", "created_at", "created_by",
            "updated_at", "updated_by",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data.setdefault(
            "address_id",
            make_model_id("Address", ID_PREFIXES["Address"], request),
        )
        return super().create(self._stamp_create(validated_data))

    def update(self, instance, validated_data):
        return super().update(instance, self._stamp_update(validated_data))


class AttendanceSerializer(AuditModelSerializer):
    """
    Attendance serializer.
    """

    duration = serializers.DurationField(read_only=True)

    class Meta:
        model = Attendance
        fields = [
            "id", "attendance_id", "attendence_for", "user", "start_time",
            "end_time", "status", "duration", "is_active", "created_at",
            "created_by", "updated_at", "updated_by",
        ]
        read_only_fields = [
            "id", "attendance_id", "start_time", "duration", "is_active",
            "created_at", "created_by", "updated_at", "updated_by",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data.setdefault(
            "attendance_id",
            make_model_id("Attendance", ID_PREFIXES["Attendance"], request),
        )
        return super().create(self._stamp_create(validated_data))

    def update(self, instance, validated_data):
        return super().update(instance, self._stamp_update(validated_data))


class PermissionSerializer(AuditModelSerializer):
    """
    Permission serializer.
    """

    class Meta:
        model = Permission
        fields = [
            "id", "permission_id", "name", "code", "description",
            "is_active", "created_at", "created_by", "updated_at",
            "updated_by",
        ]
        read_only_fields = [
            "id", "permission_id", "is_active", "created_at", "created_by",
            "updated_at", "updated_by",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data.setdefault(
            "permission_id",
            make_model_id("Permission", ID_PREFIXES["Permission"], request),
        )
        return super().create(self._stamp_create(validated_data))

    def update(self, instance, validated_data):
        return super().update(instance, self._stamp_update(validated_data))


class RoleSerializer(AuditModelSerializer):
    """
    Role serializer.
    """

    class Meta:
        model = Role
        fields = [
            "id", "role_id", "name", "descritpiton", "permission",
            "is_active", "created_at", "created_by", "updated_at",
            "updated_by",
        ]
        read_only_fields = [
            "id", "role_id", "is_active", "created_at", "created_by",
            "updated_at", "updated_by",
        ]
        extra_kwargs = {"permission": {"required": False}}

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data.setdefault(
            "role_id",
            make_model_id("Role", ID_PREFIXES["Role"], request),
        )
        return super().create(self._stamp_create(validated_data))

    def update(self, instance, validated_data):
        return super().update(instance, self._stamp_update(validated_data))


class UserProfileSerializer(AuditModelSerializer):
    """
    User profile serializer.
    """

    class Meta:
        model = UserProfile
        fields = [
            "id", "user", "bio", "level", "blood_group", "is_active",
            "created_at", "created_by", "updated_at", "updated_by",
        ]
        read_only_fields = [
            "id", "is_active", "created_at", "created_by", "updated_at",
            "updated_by",
        ]

    def create(self, validated_data):
        return super().create(self._stamp_create(validated_data))

    def update(self, instance, validated_data):
        return super().update(instance, self._stamp_update(validated_data))


class GallerySerializer(AuditModelSerializer):
    """
    Gallery serializer.
    """

    class Meta:
        model = Gallery
        fields = [
            "id", "user", "photos", "is_active", "created_at",
            "created_by", "updated_at", "updated_by",
        ]
        read_only_fields = [
            "id", "is_active", "created_at", "created_by", "updated_at",
            "updated_by",
        ]

    def create(self, validated_data):
        return super().create(self._stamp_create(validated_data))

    def update(self, instance, validated_data):
        return super().update(instance, self._stamp_update(validated_data))


class TrainerSerializer(AuditModelSerializer):
    """
    Trainer serializer.
    """

    class Meta:
        model = Trainer
        fields = [
            "id", "user", "experience", "level", "category",
            "certifiation", "bio", "joined_date", "salary", "on_leave",
            "is_active", "created_at", "created_by", "updated_at",
            "updated_by",
        ]
        read_only_fields = [
            "id", "is_active", "created_at", "created_by", "updated_at",
            "updated_by",
        ]

    def create(self, validated_data):
        return super().create(self._stamp_create(validated_data))

    def update(self, instance, validated_data):
        return super().update(instance, self._stamp_update(validated_data))
