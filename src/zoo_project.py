class Zoo:
    def __init__(self,fences: list, zoo_keepers: list):
        self.fences = fences
        self.zoo_keepers = zoo_keepers

    def describe_zoo(self):
        print("Guardiani:")
        for zoo_keeper in self.zoo_keepers:
            print(zoo_keeper)
        print("\nRecinti:")
        for fence in self.fences:
            print(fence)
        print("con animali:")
        for animal in fence.animals:
            print(animal)
        print("\n" + "#" * 30)


class Animal:
    def __init__(self, name: str, species: str, age: float, height: float, width:float, preferred_habitat:str) -> None:
        self.name: str = name
        self.species: str = species
        self.age: float = age
        self.height: float = height
        self.width: float = width
        self.preferred_habitat: str = preferred_habitat
        self.health: float = min(round(100 * (1/self.age), 3), 100)
        self.fence: Fence = None
        
    def area(self):
        return self.height * self.width
    
    def become_bigger(self, factor: float = 0.02) -> tuple[float, float]:
        height = self.height + self.height * factor
        width = self.width + self.width * factor
        return height, width
        
    def become_healthier(self, factor: float = 0.01):
        self.health = min(self.health + self.health * factor, 100)
        
    def __str__(self) -> str:
        return f'Animal(name={self.name}, species={self.species}, age={self.age}, height={round(self.height,3)}'\
            + f', width={round(self.width,3)}, habitat={self.preferred_habitat})'


class Fence:
    def __init__(self, area: float, temperature: float, habitat: str) -> None:
        self.area: float = area
        self.temperature: float = temperature
        self.habitat: str = habitat
        self.animals: list[Animal] = []
        
    def same_habitat(self, animal: Animal) -> bool:
        return animal.preferred_habitat.lower() == self.habitat.lower()
    
    def enough_space(self, animal_area: float) -> bool:
        return animal_area <= self.area
    
    def update_area(self, new_animal_area: float, old_animal_area: float):
        self.area += old_animal_area
        self.area -= new_animal_area
        
    def add_animal(self, animal: Animal):
        animal_area: float = animal.area()
        if self.same_habitat(animal) and self.enough_space(animal_area)\
            and animal not in self.animals:
            self.animals.append(animal)
            # elimino lo spazio del recinto che l'animale occupa
            self.area -= animal_area
            animal.fence = self
            
    def remove_animal(self, animal: Animal):
        if animal in self.animals:
            self.animals.remove(animal)
            animal_area: float = animal.area()
            # ripristino l'area occupata dall'animale
            self.area += animal_area
            animal.fence = None
            
    def feed(self, animal: Animal):
        new_height, new_width = animal.become_bigger()
        if self.enough_space((new_height * new_width) - animal.area()):
            # ripristina l'area vecchia occupata dall'animale
            self.area += animal.area()
            # faccio diventare l'animale più grande
            animal.height = new_height
            animal.width = new_width
            # levare al recinto l'area dell'animale più grande
            self.area -= animal.area()
            # incrementa la salute dell'animale
            animal.become_healthier()  
            
    def __str__(self) -> str:
        s: str = f"Fence(area={round(self.area,3)}, temperature={self.temperature}, habitat={self.habitat})"
        s += "\nWith Animals:\n"
        for animal in self.animals:
            s += animal.__str__() + "\n"
        return s[:-1]



class ZooKeeper:
    
    def __init__(self, name: str, surname: str, id: str) -> None:
        self.name: str = name
        self.surname: str = surname
        self.id: str = id
        
    def add_animal(self, animal: Animal, fence: Fence):
        fence.add_animal(animal)
        
    def remove_animal(self, animal: Animal, fence: Fence):
        fence.remove_animal(animal)
                
    def feed(self, animal: Animal):
        fence: Fence = animal.fence
        if fence:
            fence.feed(animal)
            
    def clean(self, fence: Fence) -> float:
        occupied_area: float = 0
        for animal in fence.animals:
            occupied_area += animal.area()
            
        if fence.area == 0:
            return occupied_area
        else:
            return occupied_area / fence.area
                
    def clean_all(self, zoo) -> float:
        cleaning_time = 0
        for fence in zoo.fences:
            cleaning_time += self.clean(fence)
        return cleaning_time
            
            
    def __str__(self) -> str:
        return f'ZooKeeper(name={self.name}, surname={self.surname}, id={self.id})'