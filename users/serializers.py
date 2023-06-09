from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ('id', 'username', 'email', 'first_name', 'last_name', 'profile_image', 'description', 'is_active',
                 'date_joined')
        read_only_fields = ('id', 'is_active', 'date_joined')


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'confirm_password', 'profile_image')
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate(self, attrs):
        # check if password is strong enough
        validate_password(attrs.get('password'))

        # checking if password and confirm password are the same
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('password and confirm password does NOT match!')

        return attrs

    @staticmethod
    def clean_validated_data(validated_data):
        # deleting confirm password because we don't need it anymore
        validated_data.pop('confirm_password')

        return validated_data

    def create(self, validated_data):
        # create user with given data
        user = self.Meta.model.objects.create(**self.clean_validated_data(validated_data))

        # set password for user
        user.set_password(validated_data.get('password'))

        # save user into database
        user.save()

        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('current_password', 'new_password', 'confirm_password')

    def validate(self, attrs):
        # check if password is strong enough
        validate_password(attrs.get('new_password'))

        # checking if password and confirm password are the same
        if attrs.get('new_password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('password and confirm password does NOT match!')

        return attrs


class UserFollowingsSerializer(serializers.ModelSerializer):
    followings = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'followings')

    def get_followings(self, obj):
        return [user.username for user in obj.followings.all()]


class UserFollowersSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'followers')

    def get_followers(self, obj):
        return [user.username for user in obj.followings.all()]
