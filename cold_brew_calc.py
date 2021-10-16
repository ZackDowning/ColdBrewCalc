import re


class Restart(Exception):
    pass


class ColdBrew:
    def __init__(self, total_volume, concentrate_ratio, ratio):
        self.concentrate_ratio = concentrate_ratio
        self.ratio = ratio
        self.concentrate_to_water_ratio = (ratio - concentrate_ratio) / concentrate_ratio
        self.concentrate_volume = total_volume / self.concentrate_to_water_ratio
        self.coffee = self.concentrate_volume / (concentrate_ratio - 1.67)
        self.concentrate_water = self.coffee * concentrate_ratio
        self.rest_of_water = total_volume - self.concentrate_volume
        self.total_volume = total_volume


if __name__ == '__main__':
    while True:
        try:
            v = input('Enter total volume (add "ml" or "oz" to end with no space): ')
            cr = input('Enter "x" value for concentrate coffee-water ratio "1:x": ')
            r = input('Enter "x" value for total coffee-water ratio "1:x" (Press enter for 1:17): ')
            try:
                if 'oz' in v:
                    v = float(v.strip('oz')) * 29.574
                elif 'ml' in v:
                    v = float(v.strip('ml'))
                else:
                    print(f"'{v}' doesn't contain 'ml' or 'oz'")
                    raise Restart
                cr = int(cr)
                if r == '':
                    r = 17
                else:
                    r = int(r)
            except ValueError:
                print(f"'{cr}' or '{r}' value not type 'integer' or 'float'")
                raise Restart
            cold_brew = ColdBrew(v, cr, r)
            print(f"""
Cold Brew - {int(cold_brew.total_volume)}ml or {int(cold_brew.total_volume / 29.574)}oz
Coffee/Water Ratio: 1:{int(cold_brew.ratio)}
---------------------
Concentrate: {int(cold_brew.concentrate_volume)}ml or {int(cold_brew.concentrate_volume / 29.574)}oz
    Coffee: {int(cold_brew.coffee)}g
    Water: {int(cold_brew.concentrate_water)}ml or {int(cold_brew.concentrate_water / 29.574)}oz
    Coffee/Water Ratio: 1:{cr}
Water: {int(cold_brew.rest_of_water)}ml or {int(cold_brew.rest_of_water / 29.574)}oz
Concentrate/Water Ratio: 1:{cold_brew.concentrate_to_water_ratio}
""")
            more_cmds = input('Do you calculate again? Y/[N]: ')
            if re.fullmatch(r'[Yy]', more_cmds):
                continue
            elif re.fullmatch(r'[Nn]|', more_cmds):
                break
            else:
                break
        except Restart:
            continue
