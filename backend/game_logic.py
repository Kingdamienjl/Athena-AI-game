import random
import re

class GameStateManager:
    def __init__(self):
        self.locations = {
            'The Sump': {'name': 'The Sump', 'base_asset': 'Location_The_Sump'},
            'Zenith Spire': {'name': 'Zenith Spire', 'base_asset': 'Location_Zenith_Spire'},
            'Dominion Dreadnought': {'name': 'Dominion Dreadnought', 'base_asset': 'Location_Dominion_Dreadnought'}
        }
        self.roles = {
            "husk_stage_1": {
                "name": "Husk Stage 1", "hp": 500, "asset": "Player_Husk_Stage1"
            },
            "husk_stage_2": {
                "name": "Husk Stage 2", "hp": 600, "asset": "Player_Husk_Stage2"
            },
            "husk_stage_3": {
                "name": "Husk Stage 3", "hp": 700, "asset": "Player_Husk_Stage3"
            },
            "analogue_hacker": {
                "name": "Analogue Hacker", "hp": 350, "asset": "Player_Analogue_Hacker"
            },
            "severed_dominion": {
                "name": "Severed Dominion", "hp": 450, "asset": "Player_Severed_Dominion"
            },
            "sentinel_spider": {
                "name": "Sentinel Spider", "hp": 400, "asset": "Player_Sentinel_Spider"
            },
            "aegis_enforcer": {
                "name": "Aegis Enforcer", "hp": 550, "asset": "Player_Aegis_Enforcer"
            },
            "ghostroot_acolyte": {
                "name": "GhostRoot Acolyte", "hp": 300, "asset": "Player_GhostRoot_Acolyte"
            },
            "aethelgard_refugee": {
                "name": "Aethelgard Refugee", "hp": 380, "asset": "Player_Aethelgard_Refugee"
            },
            "solargarden_thorn": {
                "name": "SolarGarden Thorn", "hp": 420, "asset": "Player_SolarGarden_Thorn"
            }
        }
        self.players = {}

    def _get_random_asset_variant(self, base_name: str) -> str:
        variant_idx = random.randint(1, 4)
        return f"{base_name}_0000{variant_idx}.png"

    def get_player_data(self, client_id: str):
        return self.players.get(client_id)

    def assign_role(self, client_id: str, role_name: str):
        normalized_role = role_name.strip().lower().replace(" ", "_")
        role_data = self.roles.get(normalized_role)

        if not role_data:
            return

        self.players[client_id] = {
            'client_id': client_id,
            'name': role_data['name'],
            'hp': role_data['hp'],
            'asset': self._get_random_asset_variant(role_data['asset']),
            'level': 1,
            'xp': 0,
            'inventory': [],
            'objective': 'Establish network synchronization protocols.',
            'location': 'The Sump',
            'location_image': self._get_random_asset_variant('Location_The_Sump'),
            'equipped_weapon': 'None',
            'lore': 'Core diagnostic active.',
            'backstory': 'Data register blank.'
        }

    def process_ai_response(self, ai_text: str, player_data: dict):
        if not player_data:
            return ai_text, player_data, ""

        xp_gained = 0
        xp_match = re.search(r'<<XP:(\d+)>>', ai_text)
        if xp_match:
            xp_gained = int(xp_match.group(1))
            player_data['xp'] += xp_gained
            if player_data['xp'] >= 1000:
                player_data['level'] += 1
                player_data['xp'] -= 1000
            ai_text = re.sub(r'<<XP:\d+>>', f'\n\n*** SYSTEM: +{xp_gained} DATA CORRELATION INDEX COPIED ***', ai_text)

        for item_match in re.findall(r'<<ITEM:(.*?)>>', ai_text):
            item_name = item_match.strip()
            if item_name:
                player_data['inventory'].append({
                    'name': item_name,
                    'image': f"Item_{item_name.replace(' ', '_')}.png"
                })
            ai_text = ai_text.replace(f'<<ITEM:{item_match}>>', f'\n\n*** LEAD ENCOUNTER: Acquired {item_name} ***')

        location_match = re.search(r'\[SET_LOCATION:\s*(.*??)\]', ai_text)
        if location_match:
            new_loc = location_match.group(1).strip()
            if new_loc in self.locations:
                player_data['location'] = new_loc
                player_data['location_image'] = self._get_random_asset_variant(self.locations[new_loc]['base_asset'])
            ai_text = re.sub(r'\[SET_LOCATION:\s*(.*??)\]', '', ai_text)

        return ai_text, player_data, player_data.get('location_image', '')

    def save_game(self, client_id: str):
        pass