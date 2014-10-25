from datetime import datetime

class ExampleBaseClass():
    def helloworld(self):
        print("Hello World! ", self.stvar)

class ExampleClassFactory(type):
    @staticmethod
    def create_class(class_name, stvar):
        return type(class_name, (ExampleBaseClass,), {"stvar":stvar})

# create new ExampleBaseClass subclass
ExampleSubclass = ExampleClassFactory.create_class("ExampleSubclass", datetime.now())

# create new ExampleSubclass instance
inst = ExampleSubclass()
inst.helloworld()
