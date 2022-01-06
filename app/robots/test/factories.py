import factory
from faker import Factory as FakerFactory


faker = FakerFactory.create()


class RobotFactory(factory.django.DjangoModelFactory):
    token = factory.lazy_attribute(lambda x: faker.name())
    serial = factory.lazy_attribute(lambda x: faker.name())

    class Meta:
        model = 'robots.Robot'
