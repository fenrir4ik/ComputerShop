from abc import ABC


class BaseService(ABC):
    instance_class = None

    def __init__(self, instance):
        if not self.instance_class:
            raise ValueError("Missing instance_class, set it in child class of BaseService")
        if instance is None:
            raise ValueError("Missing instance in constructor")
        elif not isinstance(instance, self.instance_class):
            raise ValueError(f"Instance should be of type {self.instance_class}, but type {type(instance)} given")
        self.instance = instance
