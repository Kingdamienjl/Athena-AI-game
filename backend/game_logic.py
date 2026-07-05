# backend/game_logic.py 
class GameStateManager: 
     def __init__(self): 
         self.players = {} 
 
     def assign_role(self, client_id, role): 
         roles = { 
             "husk": {"name": "Husk Stage 1", "hp": 550, "xp": 0, "objective": "Evolve", "location": "The Sump", "weapon": "Rusty Scalpel"}, 
             "hacker": {"name": "Analogue Hacker", "hp": 300, "xp": 0, "objective": "Infiltrate Zenith", "location": "Underground", "weapon": "Data Spike"}, 
             "dominion": {"name": "Severed Dominion", "hp": 700, "xp": 0, "objective": "Recover Memory", "location": "Deep Space", "weapon": "Void Rifle"}, 
             "spider": {"name": "Sentinel Spider", "hp": 200, "xp": 0, "objective": "Serve Athena", "location": "Zenith Spire", "weapon": "Optical Sensor"} 
         } 
         self.players[client_id] = roles.get(role, roles["husk"]) 
         self.players[client_id]['current_npc'] = 'Athena (GM)' 
 
     def get_player_data(self, client_id): 
         return self.players.get(client_id) 
 
     def process_ai_response(self, dialogue, player_data): 
         # Placeholder for future logic to parse [XP:X] or <<DMG:X>> tags 
         return dialogue, player_data, None 
 
     def save_game(self, client_id): 
         pass 