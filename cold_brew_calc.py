import re

ML_TO_OZ_RATIO = 29.574
G_TO_OZ_RATIO = 28.35
# Water absorption factor - 2.5 grams of water is absorbed to every gram of coffee used
WAF = 2.5


class Concentrate:
    def __init__(self, desired_volume, concentrate_ratio, ratio):
        self.concentrate_ratio = concentrate_ratio
        self.ratio = ratio
        self.desired_volume = desired_volume
        self.concentrate_to_water_ratio = ratio / concentrate_ratio

        # 1 here accounts for simplifying this formula: Total volume = (concentrate ratio * concentrate) + concentrate
        self.concentrate_volume = desired_volume / self.concentrate_to_water_ratio + 1
        self.rest_of_water = desired_volume - self.concentrate_volume

        self.coffee = (self.concentrate_volume * (WAF * concentrate_ratio)) / (concentrate_ratio * concentrate_ratio)

        self.concentrate_water = self.coffee * concentrate_ratio


class ColdBrew:
    def __init__(self, desired_volume, ratio):
        self.ratio = ratio
        self.desired_volume = desired_volume
        self.coffee = desired_volume / 15.33
        self.total_water = self.coffee * ratio


if __name__ == '__main__':
    while True:
        if_concentrate = input('Do you want to use concentrate? [Y]/N: ')
        if re.fullmatch(r'[Yy]|', if_concentrate):
            v = input('Enter total desired volume (add "ml" or "oz" to end with no space): ')
            cr = input('Enter "x" value for concentrate coffee-water ratio "1:x": ')
            r = input('Enter "x" value for total coffee-water ratio "1:x" (Press enter for 1:17): ')
            try:
                if 'oz' in v:
                    v = float(v.strip('oz')) * ML_TO_OZ_RATIO
                elif 'ml' in v:
                    v = float(v.strip('ml'))
                else:
                    print(f"'{v}' doesn't contain 'ml' or 'oz'")
                    continue
                cr = int(cr)
                if r == '':
                    r = 17
                else:
                    r = int(r)
            except ValueError:
                print(f"'{cr}' or '{r}' value not type 'integer' or 'float'")
                continue
            concentrate = Concentrate(v, cr, r)
            print(f"""
Cold Brew - {int(concentrate.desired_volume)}ml or {int(concentrate.desired_volume / ML_TO_OZ_RATIO)}oz
Coffee/Water Ratio: 1:{int(concentrate.ratio)}
---------------------
Concentrate: {int(concentrate.concentrate_volume)}ml or {int(concentrate.concentrate_volume / ML_TO_OZ_RATIO)}oz
    Coffee: {int(concentrate.coffee)}g or {int(concentrate.coffee / G_TO_OZ_RATIO)}oz
    Water: {int(concentrate.concentrate_water)}ml or {int(concentrate.concentrate_water / ML_TO_OZ_RATIO)}oz
    Coffee/Water Ratio: 1:{cr}
Water: {int(concentrate.rest_of_water)}ml or {int(concentrate.rest_of_water / ML_TO_OZ_RATIO)}oz
Concentrate/Water Ratio: 1:{concentrate.concentrate_to_water_ratio}
""")
        elif re.fullmatch(r'[Nn]', if_concentrate):
            v = input('Enter total desired volume (add "ml" or "oz" to end with no space): ')
            r = input('Enter "x" value for total coffee-water ratio "1:x" (Press enter for 1:17): ')
            try:
                if 'oz' in v:
                    v = float(v.strip('oz')) * ML_TO_OZ_RATIO
                elif 'ml' in v:
                    v = float(v.strip('ml'))
                else:
                    print(f"'{v}' doesn't contain 'ml' or 'oz'")
                    continue
                if r == '':
                    r = 17
                else:
                    r = int(r)
            except ValueError:
                print(f"'{r}' value not type 'integer' or 'float'")
                continue
            cold_brew = ColdBrew(v, r)
            print(f"""
Cold Brew - {int(cold_brew.desired_volume)}ml or {int(cold_brew.desired_volume / ML_TO_OZ_RATIO)}oz
Coffee/Water Ratio: 1:{int(cold_brew.ratio)}
---------------------
Coffee: {int(cold_brew.coffee)}g
Total Water: {int(cold_brew.total_water)}ml or {int(cold_brew.total_water / ML_TO_OZ_RATIO)}oz
""")
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
