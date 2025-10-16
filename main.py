import json
from db.models import Race, Skill, Guild, Player


def process_race(race_info, nickname):
    """Process race information and return race object."""
    if not race_info:
        print(f"Aviso: Jogador '{nickname}' sem raça")
        return None

    race_name = ""
    race_description = ""

    if isinstance(race_info, dict):
        race_name = race_info.get("name", "")
        race_description = race_info.get("description", "")
    elif isinstance(race_info, str):
        race_name = race_info

    if not race_name:
        print(f"Aviso: Nome da raça vazio para jogador '{nickname}'")
        return None

    race, _ = Race.objects.get_or_create(
        name=race_name,
        defaults={"description": race_description}
    )
    return race


def process_skills(race_info, race):
    """Process skills for a race."""
    if not isinstance(race_info, dict):
        return

    skills = race_info.get("skills", [])
    if not isinstance(skills, list):
        return

    for skill_data in skills:
        if isinstance(skill_data, dict):
            skill_name = skill_data.get("name")
            skill_bonus = skill_data.get("bonus", "")

            if skill_name:
                Skill.objects.get_or_create(
                    name=skill_name,
                    defaults={
                        "bonus": skill_bonus,
                        "race": race
                    }
                )


def process_guild(guild_info):
    """Process guild information and return guild object."""
    guild = None
    if guild_info and isinstance(guild_info, dict):
        guild_name = guild_info.get("name")
        guild_description = guild_info.get("description")

        if guild_name:
            guild, _ = Guild.objects.get_or_create(
                name=guild_name,
                defaults={"description": guild_description}
            )
    return guild


def process_player(nickname, player_data):
    """Process individual player data."""
    if not isinstance(player_data, dict):
        msg = f"Dados do jogador '{nickname}' ignorados"
        print(f"{msg} - não são um dicionário: {player_data}")
        return

    # Process race
    race_info = player_data.get("race")
    race = process_race(race_info, nickname)
    if not race:
        return

    # Process skills
    process_skills(race_info, race)

    # Process guild
    guild_info = player_data.get("guild")
    guild = process_guild(guild_info)

    # Create player
    email = player_data.get("email")
    bio = player_data.get("bio", "")

    Player.objects.get_or_create(
        nickname=nickname,
        defaults={
            "email": email,
            "bio": bio,
            "race": race,
            "guild": guild,
        }
    )

    print(f"Jogador '{nickname}' processado com sucesso")


def main():
    """Main function to process players from JSON file."""
    try:
        # 1️⃣ Ler o arquivo JSON
        with open("players.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        # Verificar se data é um dicionário (objeto JSON)
        if not isinstance(data, dict):
            print("Erro: O JSON deve ser um objeto com jogadores")
            return

        # 2️⃣ Iterar pelos jogadores
        for nickname, player_data in data.items():
            try:
                process_player(nickname, player_data)
            except Exception as e:
                print(f"Erro ao processar jogador '{nickname}': {e}")

    except FileNotFoundError:
        print("Erro: Arquivo players.json não encontrado")
    except json.JSONDecodeError:
        print("Erro: Arquivo JSON inválido")
    except Exception as e:
        print(f"Erro inesperado: {e}")


if __name__ == "__main__":
    main()
