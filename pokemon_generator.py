import csv
import random

# List of sample Pokemon names
pokemon_names = [
    "Pikachu", "Charizard", "Bulbasaur", "Squirtle", "Jigglypuff", "Gengar", "Mewtwo",
    "Eevee", "Machop", "Gyarados", "Snorlax", "Vaporeon", "Machamp", "Dragonite",
    "Arcanine", "Lapras", "Alakazam", "Kangaskhan", "Rhydon", "Lugia", "Articuno",
    "Zapdos", "Moltres", "Raikou", "Entei", "Suicune", "Tyranitar", "Ho-Oh", "Celebi",
    "Sceptile", "Blaziken", "Swampert", "Gardevior", "Breloom", "Slaking", "Gardevoir",
    "Exploud", "Swalot", "Sharpedo", "Wailord", "Milotic", "Torterra", "Empoleon", "Infernape",
    "Staraptor", "Bibarel", "Kricketune", "Luxray", "Roselia"
]

# Create a CSV file with 50 Pokemon entries
def create_pokemon_csv(filename, num_entries=50):
    # Pokemon data headers
    headers = ["name", "level", "power", "is_legendary"]

    with open(filename, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)  # Write headers to the CSV file

        for _ in range(num_entries):
            name = random.choice(pokemon_names)
            level = random.randint(1, 100)
            power = round(random.uniform(1.0, 100.0), 2)
            is_legendary = random.choice([True, False])

            # Write Pokemon data to the CSV file
            writer.writerow([name, level, power, is_legendary])

if __name__ == "__main__":
    create_pokemon_csv("pokemon_50.csv")
