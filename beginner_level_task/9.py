# 9
class MobilePhone:
    def __init__(self, screen="Touch Display", network="4G", is_dual_sim=False,
                 front_cam="8MP", rear_cam="12MP", memory="2GB", storage="16GB"):
        self.screen = screen
        self.network = network
        self.is_dual_sim = is_dual_sim
        self.front_cam = front_cam
        self.rear_cam = rear_cam
        self.memory = memory
        self.storage = storage
    def dial_number(self, number):
        print(f"{self.__class__.__name__} is calling {number}.")
    def incoming_call(self, number):
        print(f"{self.__class__.__name__} is receiving a call from {number}.")
    def capture_photo(self, cam='rear'):
        if cam.lower() == 'front':
            print(f"Photo taken with {self.front_cam} front camera.")
        else:
            print(f"Photo taken with {self.rear_cam} rear camera.")
class Apple(MobilePhone):
    def __init__(self, model_name, **kwargs):
        super().__init__(**kwargs)
        self.brand = "Apple"
        self.model_name = model_name
    def show_info(self):
        print(f"{self.brand} {self.model_name}: {self.memory} RAM, {self.storage} Storage, "
              f"Dual SIM: {self.is_dual_sim}, Front Camera: {self.front_cam}, "
              f"Rear Camera: {self.rear_cam}, Network: {self.network}")
class Samsung(MobilePhone):
    def __init__(self, model_name, **kwargs):
        super().__init__(**kwargs)
        self.brand = "Samsung"
        self.model_name = model_name
    def show_info(self):
        print(f"{self.brand} {self.model_name}: {self.memory} RAM, {self.storage} Storage, "
              f"Dual SIM: {self.is_dual_sim}, Front Camera: {self.front_cam}, "
              f"Rear Camera: {self.rear_cam}, Network: {self.network}")
iphone_15 = Apple(
    model_name="iPhone 15 Pro",
    network="5G",
    is_dual_sim=True,
    front_cam="12MP",
    rear_cam="48MP",
    memory="8GB",
    storage="256GB"
)
iphone_13 = Apple(
    model_name="iPhone 13",
    network="5G",
    is_dual_sim=False,
    front_cam="12MP",
    rear_cam="12MP",
    memory="4GB",
    storage="128GB"
)
galaxy_s24 = Samsung(
    model_name="Galaxy S24 Ultra",
    network="5G",
    is_dual_sim=True,
    front_cam="12MP",
    rear_cam="200MP",
    memory="12GB",
    storage="512GB"
)
galaxy_m32 = Samsung(
    model_name="Galaxy M32",
    network="4G",
    is_dual_sim=True,
    front_cam="20MP",
    rear_cam="64MP",
    memory="6GB",
    storage="128GB"
)
iphone_13.show_info()
iphone_15.dial_number("9876543210")
galaxy_s24.show_info()
galaxy_m32.capture_photo('front')