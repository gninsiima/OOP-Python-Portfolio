from src.district import DistrictPopulation

def load_all_districts():
    years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
    
    return {
        "Kampala": DistrictPopulation("Kampala", years, [1200, 1250, 1300, 1350, 1420, 1500, 1580, 1650, 1720, 1800]),
        "Wakiso": DistrictPopulation("Wakiso", years, [950, 1000, 1070, 1150, 1220, 1300, 1390, 1480, 1570, 1670]),
        "Gulu": DistrictPopulation("Gulu", years, [320, 330, 345, 360, 375, 390, 410, 430, 455, 480]),
        "Jinja": DistrictPopulation("Jinja", years, [470, 485, 500, 520, 540, 560, 585, 610, 635, 660]),
        "Mbarara": DistrictPopulation("Mbarara", years, [450, 465, 480, 500, 520, 545, 570, 595, 620, 650])
    }