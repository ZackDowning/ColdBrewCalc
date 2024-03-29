from re import fullmatch
from typing import Optional

ML_TO_OZ_RATIO = 29.574
G_TO_OZ_RATIO = 28.35
# Water absorption factor - 2.5 grams of water is absorbed to every gram of coffee used
WAF = 2.5
WELCOME_BANNER = """
  _____     __   _____                 _____     __
 / ___/__  / /__/ / _ )_______ _    __/ ___/__ _/ /___
/ /__/ _ \\/ / _  / _  / __/ -_) |/|/ / /__/ _ `/ / __/
\\___/\\___/_/\\_,_/____/_/  \\__/|__,__/\\___/\\_,_/_/\\__/
"""
NUMBER_INPUT_ERROR = "'{}' value not type 'integer' or 'float'"


class ColdBrew:
    def __init__(self, desired_volume: int, ratio: int):
        self._shared_recipe = f"""
    =====================
    Recipe
    =====================
    Cold Brew - {int(desired_volume)}ml or {int(desired_volume / ML_TO_OZ_RATIO)}oz
    Coffee/Water Ratio: 1:{int(ratio)}
    ---------------------"""

    def get_recipe(self) -> str:
        pass


class Concentrate(ColdBrew):
    def __init__(self, desired_volume, ratio, concentrate_ratio: int):
        super().__init__(desired_volume, ratio)
        self._concentrate_ratio = concentrate_ratio
        self._concentrate_to_water_ratio = (ratio - concentrate_ratio) / concentrate_ratio

        self._concentrate_volume = desired_volume / (ratio / concentrate_ratio)
        self._rest_of_water = desired_volume - self._concentrate_volume

        self._coffee = self._concentrate_volume / (concentrate_ratio - WAF)

        self._concentrate_water = self._coffee * concentrate_ratio

    def get_recipe(self):
        return f"""{self._shared_recipe}
    Concentrate: {int(self._concentrate_volume)}ml or {int(self._concentrate_volume / ML_TO_OZ_RATIO)}oz
        Coffee: {int(self._coffee)}g or {int(self._coffee / G_TO_OZ_RATIO)}oz
        Water: {int(self._concentrate_water)}ml or {int(self._concentrate_water / ML_TO_OZ_RATIO)}oz
        Coffee/Water Ratio: 1:{self._concentrate_ratio}
    Water: {int(self._rest_of_water)}ml or {int(self._rest_of_water / ML_TO_OZ_RATIO)}oz
    Concentrate/Water Ratio: 1:{self._concentrate_to_water_ratio}
    """


class NonConcentrate(ColdBrew):
    def __init__(self, desired_volume, ratio):
        super().__init__(desired_volume, ratio)
        self._coffee = desired_volume / (ratio - WAF)
        self._total_water = self._coffee * ratio

    def get_recipe(self):
        return f"""{self._shared_recipe}
    Coffee: {int(self._coffee)}g or {int(self._coffee / G_TO_OZ_RATIO)}oz
    Total Water: {int(self._total_water)}ml or {int(self._total_water / ML_TO_OZ_RATIO)}oz
    """


def input_volume():
    while True:
        volume_input = input("Enter total desired volume (add 'ml' or 'oz' to end with no space): ")
        try:
            if "oz" in volume_input:
                return float(volume_input.strip("oz")) * ML_TO_OZ_RATIO
            elif "ml" in volume_input:
                return float(volume_input.strip("ml"))
            else:
                print(f"'{volume_input}' doesn't contain 'ml' or 'oz'")
        except ValueError:
            print(NUMBER_INPUT_ERROR.format(volume_input))


def input_ratio(input_msg: str, default=Optional[int]):
    while True:
        ratio = input(input_msg)
        try:
            if default:
                return int(ratio) if ratio else default
            return int(ratio)
        except ValueError:
            print(NUMBER_INPUT_ERROR.format(ratio))


def get_cold_brew_inputs(concentrate: bool):
    default_ratio = 17
    total_ratio_message = f"Enter 'x' value for total coffee-water ratio '1:x' (Press enter for 1:{default_ratio}): "

    volume = input_volume()
    total_ratio = input_ratio(total_ratio_message, default_ratio)
    if concentrate:
        concentrate_ratio = input_ratio("Enter 'x' value for concentrate coffee-water ratio '1:x': ")
        return volume, total_ratio, concentrate_ratio
    return volume, total_ratio


def input_yes_or_no(message: str, yes_default: bool = True) -> bool:
    while True:
        output = input(message)
        if fullmatch(r"[Nn]|[Yy]|", output):
            if yes_default:
                return True if output.lower() == "y" or not output else False
            return True if output.lower() == "y" else False
        print("Invalid entry.")


def main():
    print(WELCOME_BANNER)
    while True:
        use_concentrate = input_yes_or_no("Do you want to use concentrate? [Y]/N: ")
        inputs = get_cold_brew_inputs(use_concentrate)

        cold_brew = Concentrate(*inputs) if use_concentrate else NonConcentrate(*inputs)
        recipe = cold_brew.get_recipe()
        print(recipe)

        calc_again = input_yes_or_no("Do you want to calculate again? Y/[N]: ", False)
        if not calc_again:
            break


if __name__ == "__main__":
    main()
