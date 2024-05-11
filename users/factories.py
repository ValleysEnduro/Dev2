# user/factories.py

import factory
from django.contrib.auth.models import Group, Permission
from .models import CustomUser, Purchase

class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
    
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    avatar = factory.django.ImageField(color='blue')
    
    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for group in extracted:
                self.groups.add(group)
    
    @factory.post_generation
    def user_permissions(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for perm in extracted:
                self.user_permissions.add(perm)

class PurchaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Purchase
    
    user = factory.SubFactory(CustomUserFactory)
    item_name = factory.Faker('word')
    quantity = factory.Faker('random_int', min=1, max=10)
    purchase_date = factory.Faker('date_time_this_year')

# users/tests/factories.py
import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Faker('user_name')
    email = factory.Faker('email')

    @factory.post_generation
    def avatar(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            self.avatar.save(
                extracted.name,
                extracted,
                save=False
            )
        else:
            self.avatar.save(
                'test_avatar.jpg',
                SimpleUploadedFile(
                    name='test_avatar.jpg',
                    content=b'fake-image-content',
                    content_type='image/jpeg'
                ),
                save=False
            )
        self.save()