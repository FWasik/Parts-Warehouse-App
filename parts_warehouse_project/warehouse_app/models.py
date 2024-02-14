from mongoengine import (
    Document,
    StringField,
    IntField,
    FloatField,
    DictField,
)


class Category(Document):
    name = StringField(max_length=100, unique=True, required=True)
    parent_name = StringField(max_length=100, required=False, null=True)

    def can_be_deleted(self, children_to_delete):
        if Part.objects(category=self.name).count() > 0:
            return False
        for child in Category.objects(parent_name=self.name).filter():
            if not child.can_be_deleted(children_to_delete):
                return False

            children_to_delete.append(child)
        return True

    def is_child(self, category):
        if category == self:
            return True
        for child in Category.objects(parent_name=self.name).filter():
            if child.is_child(category):
                return True

        return False


class Part(Document):
    serial_number = StringField(max_length=100, unique=True, required=True)
    name = StringField(max_length=100, required=True)
    description = StringField(required=True)
    category = StringField(max_length=100, required=True)
    quantity = IntField(required=True, min_value=0)
    price = FloatField(required=True, min_value=0)
    location = DictField(required=True)
