import re

from typing import override

ML_TO_OZ_RATIO = 29.574
G_TO_OZ_RATIO = 28.35
# Water absorption factor - 2.5 grams of water is absorbed to every gram of coffee used
WAF = 2.5
DEFAULT_TOTAL_RATIO = 17


class ColdBrew:
    def __init__(self, desired_volume, ratio):
        self._ratio = ratio
        self._desired_volume = desired_volume

    def print(self) -> None:
        pass


class Concentrate(ColdBrew):
    def __init__(self, desired_volume, concentrate_ratio, ratio):
        super().__init__(desired_volume, ratio)
        concentrate_ratio = concentrate_ratio
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
            Coffee/Water Ratio: 1:{cr}
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


def get_inputs(conc: bool):
    volume = input('Enter total desired volume (add "ml" or "oz" to end with no space): ')
    total_ratio = input('Enter "x" value for total coffee-water ratio "1:x" (Press enter for 1:17): ')
    if conc:
        conc_ratio = input('Enter "x" value for concentrate coffee-water ratio "1:x": ')
        return volume, conc_ratio, total_ratio
    return volume, total_ratio


def get_volume(volume_input):
    if 'oz' in volume_input:
        return float(volume_input.strip('oz')) * ML_TO_OZ_RATIO
    elif 'ml' in volume_input:
        return float(volume_input.strip('ml'))
    else:
        print(f"'{volume_input}' doesn't contain 'ml' or 'oz'")
        return None


def get_ratio(ratio):
    return DEFAULT_TOTAL_RATIO if ratio == '' else int(ratio)


if __name__ == '__main__':
    while True:
        if_concentrate = input('Do you want to use concentrate? [Y]/N: ')
        if re.fullmatch(r'[Yy]|', if_concentrate):
            v, cr, r = get_inputs(True)
            try:
                v = get_volume(v)
                if not v:
                    continue
                r = get_ratio(r)
                cr = int(cr)
            except ValueError:
                print(f"'{cr}' or '{r}' value not type 'integer' or 'float'")
                continue
            concentrate = Concentrate(v, cr, r)
            concentrate.print()
        elif re.fullmatch(r'[Nn]', if_concentrate):
            v, r = get_inputs(False)
            try:
                v = get_volume(v)
                if not v:
                    continue
                r = get_ratio(r)
            except ValueError:
                print(f"'{r}' value not type 'integer' or 'float'")
                continue
            non_concentrate = NonConcentrate(v, r)
            non_concentrate.print()
        else:
            print('Invalid entry.')
            continue
        calc_again = input('Do you want to calculate again? Y/[N]: ')
        if re.fullmatch(r'[Yy]', calc_again):
            continue
        elif re.fullmatch(r'[Nn]|', calc_again):
            break
        else:
            break
