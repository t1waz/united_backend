import factory
from faker import Factory as FakerFactory


faker = FakerFactory.create()


class UserFactory(factory.django.DjangoModelFactory):
    is_active = True
    email = factory.lazy_attribute(lambda x: faker.email())
    username = factory.lazy_attribute(lambda x: faker.name())
    first_name = factory.lazy_attribute(lambda x: faker.name())
    password = factory.lazy_attribute(lambda x: faker.password())
    last_name = factory.lazy_attribute(lambda x: faker.last_name())

    class Meta:
        model = 'users.User'
