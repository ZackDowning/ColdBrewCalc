import re

from typing import override, Optional

ML_TO_OZ_RATIO = 29.574
G_TO_OZ_RATIO = 28.35
# Water absorption factor - 2.5 grams of water is absorbed to every gram of coffee used
WAF = 2.5
DEFAULT_TOTAL_RATIO = 17
WELCOME_BANNER = """
  _____     __   _____                 _____     __
 / ___/__  / /__/ / _ )_______ _    __/ ___/__ _/ /___
/ /__/ _ \\/ / _  / _  / __/ -_) |/|/ / /__/ _ `/ / __/
\\___/\\___/_/\\_,_/____/_/  \\__/|__,__/\\___/\\_,_/_/\\__/
"""


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

    @override
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

    @override
    def get_recipe(self):
        return f"""{self._shared_recipe}
    Coffee: {int(self._coffee)}g or {int(self._coffee / G_TO_OZ_RATIO)}oz
    Total Water: {int(self._total_water)}ml or {int(self._total_water / ML_TO_OZ_RATIO)}oz
    """


def get_inputs(concentrate: bool):
    volume = input('Enter total desired volume (add "ml" or "oz" to end with no space): ')
    total_ratio = input('Enter "x" value for total coffee-water ratio "1:x" (Press enter for 1:17): ')
    if concentrate:
        concentrate_ratio = input('Enter "x" value for concentrate coffee-water ratio "1:x": ')
        return volume, concentrate_ratio, total_ratio
    return volume, total_ratio


def get_volume(volume_input: str):
    if 'oz' in volume_input:
        return float(volume_input.strip('oz')) * ML_TO_OZ_RATIO
    elif 'ml' in volume_input:
        return float(volume_input.strip('ml'))
    else:
        print(f"'{volume_input}' doesn't contain 'ml' or 'oz'")
        return None


def get_ratio(ratio: Optional[str]):
    return int(ratio) if ratio else DEFAULT_TOTAL_RATIO


def get_value_error(incorrect_value):
    return f"'{incorrect_value}' value not type 'integer' or 'float'"


def clean_inputs(volume, ratio, concentrate_ratio=None):
    try:
        volume = get_volume(volume)
        if not volume:
            return None
        ratio = get_ratio(ratio)
        if concentrate_ratio:
            try:
                return volume, ratio, int(concentrate_ratio)
            except ValueError:
                print(get_value_error(concentrate_ratio))
                return None
        return volume, ratio
    except ValueError:
        print(get_value_error(ratio))
        return None


def get_yes_or_no_bool(message: str, yes_default: bool = True) -> bool:
    while True:
        output = input(message)
        if re.fullmatch(r'[Nn]|[Yy]|', output):
            if yes_default:
                return True if output.lower() == "y" or not output else False
            return True if output.lower() == "y" else False
        print("Invalid entry.")


def input_loop():
    while True:
        use_concentrate = get_yes_or_no_bool("Do you want to use concentrate? [Y]/N: ")
        cleaned_inputs = clean_inputs(*get_inputs(use_concentrate))
        if not cleaned_inputs:
            continue

        cold_brew = Concentrate(*cleaned_inputs) if use_concentrate else NonConcentrate(*cleaned_inputs)
        recipe = cold_brew.get_recipe()
        print(recipe)

        calc_again = get_yes_or_no_bool("Do you want to calculate again? Y/[N]: ", False)
        if not calc_again:
            break


def main():
    print(WELCOME_BANNER)
    input_loop()


if __name__ == '__main__':
    main()
