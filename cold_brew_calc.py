import re

from typing import override, Optional

ML_TO_OZ_RATIO = 29.574
G_TO_OZ_RATIO = 28.35
# Water absorption factor - 2.5 grams of water is absorbed to every gram of coffee used
WAF = 2.5
DEFAULT_TOTAL_RATIO = 17


class ColdBrew:
    def __init__(self, desired_volume: int, ratio: int):
        self._ratio = ratio
        self._desired_volume = desired_volume

    def print(self):
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
    def print(self):
        print(f"""
        Cold Brew - {int(self._desired_volume)}ml or {int(self._desired_volume / ML_TO_OZ_RATIO)}oz
        Coffee/Water Ratio: 1:{int(self._ratio)}
        ---------------------
        Concentrate: {int(self._concentrate_volume)}ml or {int(self._concentrate_volume / ML_TO_OZ_RATIO)}oz
            Coffee: {int(self._coffee)}g or {int(self._coffee / G_TO_OZ_RATIO)}oz
            Water: {int(self._concentrate_water)}ml or {int(self._concentrate_water / ML_TO_OZ_RATIO)}oz
            Coffee/Water Ratio: 1:{self._concentrate_ratio}
        Water: {int(self._rest_of_water)}ml or {int(self._rest_of_water / ML_TO_OZ_RATIO)}oz
        Concentrate/Water Ratio: 1:{self._concentrate_to_water_ratio}
        """)


class NonConcentrate(ColdBrew):
    def __init__(self, desired_volume, ratio):
        super().__init__(desired_volume, ratio)
        self._coffee = desired_volume / (ratio - WAF)
        self._total_water = self._coffee * ratio

    @override
    def print(self):
        print(f"""
        Cold Brew - {int(self._desired_volume)}ml or {int(self._desired_volume / ML_TO_OZ_RATIO)}oz
        Coffee/Water Ratio: 1:{int(self._ratio)}
        ---------------------
        Coffee: {int(self._coffee)}g or {int(self._coffee / G_TO_OZ_RATIO)}oz
        Total Water: {int(self._total_water)}ml or {int(self._total_water / ML_TO_OZ_RATIO)}oz
        """)


def get_inputs(concentrate: Optional[re.Match]):
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


def print_value_error(incorrect_value):
    print(f"'{incorrect_value}' value not type 'integer' or 'float'")


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
                print_value_error(concentrate_ratio)
                return None
        return volume, ratio
    except ValueError:
        print_value_error(ratio)
        return None


def input_loop():
    while True:
        concentrate_input = input('Do you want to use concentrate? [Y]/N: ')
        if not re.fullmatch(r'[Nn]|[Yy]|', concentrate_input):
            print('Invalid entry.')
            continue

        use_concentrate = re.fullmatch(r'[Yy]|', concentrate_input)
        cleaned_inputs = clean_inputs(*get_inputs(use_concentrate))
        if not cleaned_inputs:
            continue

        cold_brew = Concentrate(*cleaned_inputs) if use_concentrate else NonConcentrate(*cleaned_inputs)
        cold_brew.print()

        calc_again = input('Do you want to calculate again? Y/[N]: ')
        if re.fullmatch(r'[Yy]', calc_again):
            continue
        elif re.fullmatch(r'[Nn]|', calc_again):
            break
        else:
            break


if __name__ == '__main__':
    input_loop()
