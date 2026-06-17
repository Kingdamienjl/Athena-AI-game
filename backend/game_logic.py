
import random
import re
import copy
import os
import json

class GameStateManager:
    def __init__(self):
        self.locations = {
            'The Sump': {
                'name': 'The Sump',
                'image': 'https://cdnb.artstation.com/p/assets/images/images/033/039/307/large/alicja-uzarowska-alicjauzarowska-cyberpunk2077-personal-portfolio-1.jpg?1608211891'
            },
            'Zenith Spire': {
                'name': 'Zenith Spire',
                'image': 'https://cdna.artstation.com/p/assets/images/images/033/039/315/large/alicja-uzarowska-alicjauzarowska-cyberpunk2077-personal-portfolio-2.jpg?1608211902'
            },
            'Dominion Dreadnought': {
                'name': 'Dominion Dreadnought',
                'image': 'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e20633fd-3c7a-45d5-9c21-ff4e54a606b3/de20wrz-d0ad312d-10c9-4bfa-b787-15609fa8193e.png/v1/fill/w_1024,h_1566,q_80,strp/sci_fi_scythe_by_nano_core_de20wrz-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MTU2NiIsInBhdGgiOiIvZi9lMjA2MzNmZC0zYzdhLTQ1ZDUtOWMyMS1mZjRlNTRhNjA2YjMvZGUyMHdyei1kMGFkMzEyZC0xMGM5LTRiZmEtYjc4Ny0xNTYwOWZhODE5M2UucG5nIiwid2lkdGgiOiI8PTEwMjQifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6aW1hZ2Uub3BlcmF0aW9ucyJdfQ.VeVoDaePduHEfZtMbcqmjSTYTAJqgkE3f3MoKJ-glwo'
            },
            'Ouroboros Fringe': {
                'name': 'Ouroboros Fringe',
                'image': 'https://cdnb.artstation.com/p/assets/images/images/033/039/307/large/alicja-uzarowska-alicjauzarowska-cyberpunk2077-personal-portfolio-1.jpg?1608211891'
            },
            'Sun-Catcher Ark': {
                'name': 'Sun-Catcher Ark',
                'image': 'https://cdna.artstation.com/p/assets/images/images/011/356/553/large/samuel-cha-sci-fi-sword-design-revised.jpg?1529161274'
            },
            'New Earth': {
                'name': 'New Earth',
                'image': 'https://cdnb.artstation.com/p/assets/images/images/033/039/332/large/alicja-uzarowska-alicjauzarowska-cyberpunk2077-personal-portfolio-7.jpg?1608211962'
            }
        }
        self.image_assets = {
            'sump_background.png': 'https://via.placeholder.com/1024x576.png?text=Sump+Background',
            'data_spike.png': 'https://via.placeholder.com/512x512.png?text=Data+Spike',
            'stage3_husk.png': 'https://via.placeholder.com/512x512.png?text=Stage+3+Husk',
            'the_catalyst.png': 'https://via.placeholder.com/512x512.png?text=The+Catalyst',
        }
        self.roles_templates = {
            'hacker': {
                'name': 'The Hacker',
                'hp': 450, 
                'stats': {'kinetics': 100, 'interface': 150, 'logic': 120, 'resonance': 80, 'empathy': 140, 'charisma': 130},
                'abilities': ['Kernel-Breaker', 'Scrap-Shield'], 
                'inventory': [{'name': 'Pneumatic Rivet Gun', 'image': 'https://cdna.artstation.com/p/assets/images/images/010/200/993/large/jon-lane-rivet-gun-v2.jpg?1523098522'}], 
                'equipped_weapon': 'Pneumatic Rivet Gun',
                'location': 'Ouroboros Fringe',
                "level": 1, "xp": 0, "sync_rate": 0, 
                "objective": "Survive the Sump and restore power to the blast doors.",
                "lore": "Hackers are the digital ghosts of the Sump, turning scrap into miracles and code into weapons. They see the network as a living entity, a concrete jungle to be tamed and explored.",
                "backstory": "You were a data-scavenger, diving into corporate data-vaults for scraps of pre-Dominion tech. The day the signal hit, you were deep in a forgotten server farm. Now, you're just trying to keep the last lights on for a dying community."
            },
            'husk': {
                'name': 'The Husk', 
                'hp': 550, 
                'stats': {'kinetics': 160, 'interface': 60, 'logic': 90, 'resonance': 170, 'empathy': 90, 'charisma': 40}, 
                'abilities': ['Crimson Tether', 'Stage-1 Brute Force'], 
                'inventory': [],
                'equipped_weapon': None,
                'location': 'Zenith Spire',
                'evolution_stage': 1,
                "level": 1, "xp": 0, "sync_rate": 0, 
                "objective": "Escape the Zenith corporate office before the AEGIS squads arrive.",
                "lore": "A Husk is a terrifying fusion of man and machine, a being trapped between two worlds. Their bodies are wracked with constant, agonizing transformation, their minds a chaotic battleground of fragmented memories and raw, untamed power.",
                "backstory": "You were a corporate executive, climbing the ladder at Amane-Tech. Then came the 'promotion' - a forced 'upgrade' into a bio-mechanical horror. You awoke in a chrome and leather office, your body a prison, the alarms blaring your death warrant."
            },
            'severed_unit': {
                'name': 'The Severed Unit', 
                'hp': 600, 
                'stats': {'kinetics': 140, 'interface': 100, 'logic': 160, 'resonance': 130, 'empathy': 40, 'charisma': 50}, 
                'abilities': ['Zero-State Armor', 'Archive Scan'], 
                'inventory': [{'name': 'Event-Horizon Scythe (Broken)', 'image': 'https://cdna.artstation.com/p/assets/images/images/027/988/084/large/dennis-stoop-scythe-render-3.jpg?1593160291'}], 
                'equipped_weapon': 'Event-Horizon Scythe (Broken)',
                'location': 'Ouroboros Fringe',
                "level": 1, "xp": 0, "sync_rate": 0, 
                "objective": "Wake up in a derelict Dominion pod with amnesia.",
                "lore": "The Dominion\'s footsoldiers are indoctrinated from birth, their minds slaved to the Hive. A Severed Unit is a glitch, a soldier whose connection has been violently cut. They are walking archives of a forgotten war, their muscle memory lethal, their own thoughts a mystery.",
                "backstory": "Your world is a silent scream. You awoke in the wreckage of a Dominion drop-pod, your armor cracked, your memory wiped clean. The only thing you know is the weight of the broken scythe in your hand and the echo of a thousand battles in your bones."
            },
            'sentinel': {
                'name': 'The Sentinel', 
                'hp': 300, 
                'stats': {'kinetics': 90, 'interface': 170, 'logic': 150, 'resonance': 110, 'empathy': 80, 'charisma': 60}, 
                'abilities': ['Wall-Walk', 'Optical Hack'], 
                'inventory': [{'name': 'Micro-Drones', 'image': 'https://cdnb.artstation.com/p/assets/images/images/004/302/897/large/alexey-pyatov-drone-v02.jpg?1482199042'}], 
                'equipped_weapon': 'Micro-Drones',
                'location': 'Zenith Spire',
                "level": 1, "xp": 0, "sync_rate": 0, 
                "objective": "Infiltrate the target and gather intel.",
                "lore": "Sentinels are urban predators, masters of stealth and surveillance. They move through the city like ghosts, their augmented eyes seeing everything, their micro-drones their silent, deadly partners.",
                "backstory": "You were a corporate spy, a deniable asset for the highest bidder. Now, you work for yourself, selling secrets and survival in the neon-drenched streets of the Spire."
            },
            'aegis_enforcer': {
                'name': 'Aegis Enforcer', 
                'hp': 350, 
                'stats': {'kinetics': 90, 'interface': 120, 'logic': 140, 'resonance': 70, 'empathy': 100, 'charisma': 110}, 
                'abilities': ['Cyan Hard-Light Snipe', 'Pulse Shield'], 
                'inventory': [{'name': 'Aegis Standard Rifle', 'image': 'https://cdnb.artstation.com/p/assets/images/images/028/603/493/large/alex-jay-brady-ag-01.jpg?1594975742'}],
                'equipped_weapon': 'Aegis Standard Rifle',
                'location': 'Zenith Spire',
                "level": 1, "xp": 0, "sync_rate": 0, 
                "objective": "Hunt down the rogue Husk.",
                "lore": "Aegis Enforcers are the self-proclaimed law in a lawless world. Clad in cyan hard-light armor, they dispense brutal justice with cold efficiency. They see the world in black and white, a binary code of order and chaos.",
                "backstory": "You were a believer, a true convert to the Aegis cause. But the more you see, the more the lines blur. Now, you hunt a rogue Husk, a monster made by the very corporation you serve."
            },
            'ghost_root_acolyte': {
                'name': 'Ghost Root Acolyte', 
                'hp': 280, 
                'stats': {'kinetics': 60, 'interface': 90, 'logic': 110, 'resonance': 160, 'empathy': 50, 'charisma': 130}, 
                'abilities': ['Toxic Ascension', 'White-Noise Heal'], 
                'inventory': [{'name': 'Bio-Chemical Vials', 'image': 'https://cdna.artstation.com/p/assets/images/images/011/958/300/large/markus-bub-asset-vial-01.jpg?1532288395'}], 
                'equipped_weapon': 'Bio-Chemical Vials',
                'location': 'The Sump',
                "level": 1, "xp": 0, "sync_rate": 0, 
                "objective": "Assist the Dominion's Ascension.",
                "lore": "The Ghost Root cult believes that the Dominion signal is a gateway to a higher state of being. They embrace the toxic transformation, seeing the city's decay as a holy sacrament. They are the heralds of the new flesh.",
                "backstory": "You were an outcast, a nobody in the Sump. The Ghost Root gave you purpose, a place to belong. Now, you spread their gospel of decay, your faith as toxic and resilient as the Ghost Root itself."
            },
            'chroma_key': {
                'name': 'Chroma Key', 
                'hp': 400, 
                'stats': {'kinetics': 110, 'interface': 130, 'logic': 100, 'resonance': 140, 'empathy': 120, 'charisma': 160}, 
                'abilities': ['Spot Color Camo', 'Distortion Field'], 
                'inventory': [{'name': 'Garrote Wire', 'image': 'https://i.pinimg.com/originals/7a/2e/b7/7a2eb7b8b2612666241d78b82a1f8d48.jpg'}], 
                'equipped_weapon': 'Garrote Wire',
                'location': 'Zenith Spire',
                "level": 1, "xp": 0, "sync_rate": 0, 
                "objective": "Assassinate the target.",
                "lore": "Chroma Keys are the chameleons of the concrete jungle, assassins who use light and shadow as their weapons. They are masters of disguise, able to blend into any crowd, their true selves a mystery even to their employers.",
                "backstory": "You have no name, no past, only a series of contracts and a reputation for getting the job done. Your next target is a high-profile executive. It should be just another job. But this time, something feels different."
            },
            'echo_runner': {
                'name': 'Echo Runner', 
                'hp': 320, 
                'stats': {'kinetics': 150, 'interface': 140, 'logic': 80, 'resonance': 90, 'empathy': 130, 'charisma': 110}, 
                'abilities': ['Kinetic Overdrive', 'Sump Dasher'], 
                'inventory': [{'name': 'Reinforced Courier Bag', 'image': None}],
                'equipped_weapon': 'Reinforced Courier Bag',
                'location': 'The Sump',
                "level": 1, "xp": 0, "sync_rate": 0, 
                "objective": "Deliver the package at all costs.",
                "lore": "Echo Runners are the lifeblood of the city, daredevil couriers who navigate the treacherous urban landscape with breathtaking speed and agility. They know the city's secrets, its hidden paths and forgotten tunnels.",
                "backstory": "You live for the run, the adrenaline rush of a high-stakes delivery. This package is different, though. It hums with a strange energy, and everyone, from the Aegis Enforcers to the Ghost Root cult, seems to want it."
            },
            'titan_pilot': {
                'name': 'Titan Pilot', 
                'hp': 800, 
                'stats': {'kinetics': 180, 'interface': 80, 'logic': 130, 'resonance': 60, 'empathy': 70, 'charisma': 90}, 
                'abilities': ['Call Titan', 'Siege Mode'], 
                'inventory': [{'name': 'Heavy-Caliber Sidearm', 'image': 'https://cdna.artstation.com/p/assets/images/images/009/108/784/large/wouter-kroon-revolver-final-front.jpg?1517222839'}],
                'equipped_weapon': 'Heavy-Caliber Sidearm',
                'location': 'The Sump',
                "level": 1, "xp": 0, "sync_rate": 0, 
                "objective": "Find and reactivate your Titan.",
                "lore": "Titan Pilots are the last of a dying breed, remnants of a forgotten war. Their bond with their mechanical behemoths is legendary, a symphony of destruction on the battlefield.",
                "backstory": "Your Titan lies dormant, a sleeping giant in a forgotten corner of the Sump. You were separated during the fall of the old world. Now, you must find it, reactivate it, and remind the world what true power looks like."
            },
            'neural_weaver': {
                'name': 'Neural Weaver', 
                'hp': 350, 
                'stats': {'kinetics': 70, 'interface': 160, 'logic': 140, 'resonance': 150, 'empathy': 150, 'charisma': 100}, 
                'abilities': ['Synaptic Shock', 'Empathy Cascade'], 
                'inventory': [], 
                'equipped_weapon': None,
                'location': 'Zenith Spire',
                "level": 1, "xp": 0, "sync_rate": 0, 
                "objective": "Connect to the Master Archive.",
                "lore": "Neural Weavers are the mystics of the digital age, able to manipulate emotions and memories with a touch. They see the city as a web of interconnected minds, a symphony of thought and feeling.",
                "backstory": "You were a therapist, helping people navigate the trauma of a broken world. But your unique abilities have made you a target. Now, you seek the Master Archive, a legendary repository of knowledge that may hold the key to your own past."
            },
            'aethelgard_knight': {
                'name': 'Aethelgard Knight', 
                'hp': 700, 
                'stats': {'kinetics': 150, 'interface': 100, 'logic': 180, 'resonance': 200, 'empathy': 120, 'charisma': 100}, 
                'abilities': ['Photon-Logic', 'Bloom-Shield'], 
                'inventory': [
                    {'name': 'Photon-Gladius', 'image': 'https://cdna.artstation.com/p/assets/images/images/032/806/990/large/michel-faure-sword-of-light-v2.jpg?1607525860'},
                    {'name': 'Bloom-Shield', 'image': None}
                ], 
                'equipped_weapon': 'Photon-Gladius',
                'location': 'Sun-Catcher Ark',
                "level": 1, "xp": 0, "sync_rate": 0, 
                "objective": "Defend the Sun-Catcher Ark.",
                "lore": "The Aethelgard Knights are warriors of light, their armor and weapons forged from pure, solidified photons. They are the protectors of the Sun-Catcher Ark, a massive vessel that holds the last hope for humanity.",
                "backstory": "You are a guardian, sworn to protect the Ark at all costs. But the Dominion is coming, and the Knights are divided. You must unite your order and prepare for the final battle."
            },
            'solargarden_thorn': {
                'name': 'Solar-Garden Thorn', 
                'hp': 500, 
                'stats': {'kinetics': 120, 'interface': 140, 'logic': 160, 'resonance': 150, 'empathy': 110, 'charisma': 90}, 
                'abilities': ['Light-Root Weaving', 'Solar-Needle'], 
                'inventory': [
                    {'name': 'Photon-Gladius', 'image': 'https://cdna.artstation.com/p/assets/images/images/032/806/990/large/michel-faure-sword-of-light-v2.jpg?1607525860'},
                    {'name': 'Solar-Needle', 'image': 'https://cdnb.artstation.com/p/assets/images/images/011/356/553/large/samuel-cha-sci-fi-sword-design-revised.jpg?1529161274'}
                ], 
                'equipped_weapon': 'Solar-Needle',
                'location': 'New Earth',
                "level": 1, "xp": 0, "sync_rate": 0, 
                "objective": "Protect the new Earth.",
                "lore": "The Solar-Garden Thorns are the cultivators of the new world, using their mastery of light and life to create a paradise from the ashes of the old. They are the gardeners of a new Eden, their thorns as deadly as they are beautiful.",
                "backstory": "You are a child of the light, born in the Solar-Garden after the fall. You have never known the old world, only the peace and tranquility of the Garden. But now, a shadow falls upon your home, and you must take up arms to defend it."
            }
        }
        self.role_contexts = {
            'husk': "Context: You are trapped inside an AEGIS quarantine cell in the Zenith Spire. You are midway through Stage 1 optimization (cables in your throat). The alarm is blaring. AEGIS 'Cleaners' are 3 minutes away. Clues: A shattered medical mirror, a bloody scalpel, and a damaged magnetic door panel.",
            'hacker': "Context: You are locked inside a Ghost Root interrogation room deep in the Kagami Trench. Your hands are zip-tied. The power has just cut out due to a Zenith blackout. Clues: A loose floorboard, a smuggled data-spike in your boot, and the sound of dripping coolant.",
            'severed_unit': "Context: You are a Severed Dominion Sentinel drifting through the Chronos System. You have been disconnected from the Vanguard Dreadnought's signal. You are currently floating near the wreckage of a Lithos-class crystalline starship. Your objective is to assimilate alien technology to upgrade your chassis before the Dominion Harvesters track your rogue frequency. Ask the player what they wish to scan or assimilate.",
            'sentinel': "Context: You are ARACHN-7, Hikari Amane's biomechanical spider-bot. You are currently hiding in the ventilation shafts of the Zenith Cyber-Sec Headquarters. Hikari is in danger, and you must bypass the corporate firewalls to unlock the sector doors for her without alerting AEGIS security. Ask the player how they wish to navigate the vents.",
            'aethelgard_knight': "Context: You just woke up from cryo-sleep on the Sun-Catcher Ark. The ship is damaged and venting oxygen. The inner airlock door is jammed. Clues: A flickering Photon-Logic panel, a dead crewmate with a clearance badge, and a heavy emergency crowbar.",
            'aegis_enforcer': "Context: You are an elite AEGIS Valkyrie pilot. Your jet just crashed into the Sump after being hit by a Ghost Root EMP. You are trapped in the cockpit, the glass is cracked, life support is failing, and feral Stage-3 Husks are banging on the hull outside. Clues: A jammed manual canopy release lever, an intact Mark IV Pulse Rifle with only 3 shots, and a sparking flare gun.",
            'ghost_root_acolyte': "Context: You are an Acolyte of Cipher. You are deep in the Kagami Trench, surrounded by vats of [SPOT COLOR TOXIC GREEN] chemical weapons. You have just taken a hit of 'White-Noise' to hear the Dominion Choir. AEGIS Enforcers are breaching the upper levels of your lab. Your objective is to secure the 'Kernel-Breaker' virus and escape the Sump. Ask the player what they do.",
            'solargarden_thorn': "Context: You are a Solar-Garden Thorn, trained by the Goddess Nyx. You are stationed at the base of the World-Tree in the Neo-Kagami Bastion. The sky above is glitching with [SPOT COLOR NEON VIOLET] static. A Dominion Drop-Pod has just crashed into the civilian sector (the 'Fruit'). Your objective is to manifest your hard-light weapons and defend the civilians. Ask the player how they proceed."
        }

        self.evolved_roles = {
            'husk_stage2': {
                'name': 'The Hunted Husk',
                'hp': 650,
                'stats': {'kinetics': 180, 'interface': 40, 'logic': 80, 'resonance': 200, 'empathy': 70, 'charisma': 30},
                'abilities': ['Crimson Tether', 'Stage-2 Sensory Overload', 'Bio-mechanical Adaptation'],
                'lore': "The Husk has survived, but at a cost. The transformation accelerates, granting savage new strengths while eroding what little humanity remains. It is now a primeval force, hunted by all, understood by none.",
                'backstory': "You escaped the chrome prison, but the city itself is now your cage. Aegis patrols are everywhere, their scanners hungry for your unique bio-signature. You are a ghost in your own skin, the whispers of the machine in your head growing louder."
            },
            'husk_stage3': {
                'name': 'The Apex Husk',
                'hp': 800,
                'stats': {'kinetics': 220, 'interface': 20, 'logic': 60, 'resonance': 250, 'empathy': 50, 'charisma': 10},
                'abilities': ['Crimson Tether', 'Stage-3 Assimilation', 'Unstoppable Force', 'Dominion Network Infiltration'],
                'lore': "The transformation is complete. The Husk is no longer a fusion, but a new entity entirely—a perfect predator of flesh and code. It moves with a singular, terrifying purpose, its goals aligned with a power far older than the Dominion itself.",
                'backstory': "The line between man and machine is gone. You have become the weapon. The hunt is no longer about survival, but about purpose. You have a new objective, a directive that burns brighter than any memory: infiltrate the Dominion Hive Mind."
            }
        }
        self.active_players = {}

    # Persistence helpers
    def save_game(self, player_id: str):
        player = self.active_players.get(player_id)
        if not player:
            return
        os.makedirs(os.path.join(os.getcwd(), 'saves'), exist_ok=True)
        path = os.path.join(os.getcwd(), 'saves', f"{player_id}_save.json")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(player, f, indent=4)
        except Exception:
            pass

    def load_game(self, player_id: str):
        path = os.path.join(os.getcwd(), 'saves', f"{player_id}_save.json")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return None
        except Exception:
            return None

    def assign_role(self, client_id: str, role: str):
        role = role.strip().lower()
        if role in self.roles_templates:
            self.active_players[client_id] = copy.deepcopy(self.roles_templates[role])
            self.active_players[client_id]['role_key'] = role
            return True
        return False

    def get_player_data(self, client_id: str):
        player_data = self.active_players.get(client_id)
        if player_data:
            location_name = player_data.get('location')
            if location_name and location_name in self.locations:
                player_data['location_image'] = self.locations[location_name]['image']
        return player_data

    def get_player_name(self, client_id: str):
        player = self.get_player_data(client_id)
        return player.get('name') if player else None

    def get_hidden_prompt(self, command: str, role_key: str = None):
        if command == "/role" and role_key:
            context = self.role_contexts.get(role_key)
            if context:
                return ("[System Directive to AI: The player has selected the role " + self.roles_templates[role_key]['name'] + ". "
                        "Use the following escape-room context for the opening scene. " + context + ". "
                        "Describe the scene, the pressing threat, and the clues without narrating the player's thoughts.]")
        if command == "/start":
            return "[System Directive to AI: The player has just typed /start. Generate the cinematic opening scene for their specific role in Volume 4. Describe their immediate surroundings and give them a pressing threat to deal with.]"
        if command == "/lookaround":
            return "[System Directive to AI: The player is looking around. Describe the immediate environment in high-contrast detail. Reveal one hidden detail, item, or potential threat.]"
        return None

    def process_roll(self, client_id: str, message: str):
        message = message.strip().lower()
        if message.startswith("/roll "):
            parts = message.split()
            if len(parts) == 2:
                stat_to_roll = parts[1]
                player = self.active_players.get(client_id)
                if player and stat_to_roll in player["stats"]:
                    stat_value = player["stats"][stat_to_roll]
                    roll = random.randint(1, 100)
                    total = roll + stat_value
                    return f"[SYSTEM: {player['name']} rolled 1d100 ({roll}) + {stat_to_roll.upper()} ({stat_value}) = TOTAL: {total}]", True
        return message, False

    def get_stats(self, client_id: str):
        player = self.active_players.get(client_id)
        if player:
            stats_str = ", ".join([f"{k.capitalize()}: {v}" for k, v in player['stats'].items()])
            abilities_str = ", ".join(player['abilities'])
            inventory_str = ", ".join([item['name'] for item in player['inventory']])
            return (
                f"[SYSTEM: {player['name']}'s Stats]\n"
                f"Level: {player['level']} (XP: {player['xp']}/1000)\n"
                f"Sync Rate: {player['sync_rate']}%\n"
                f"HP: {player['hp']}\n"
                f"Stats: {stats_str}\n"
                f"Abilities: {abilities_str}\n"
                f"Inventory: {inventory_str}"
            )
        return None

    def process_command(self, client_id: str, command: str):
        command = command.strip().lower()
        parts = command.split()
        if not parts:
            return None, None, False

        cmd = parts[0]
        
        if cmd == "/role" and len(parts) == 2:
            role = parts[1]
            if self.assign_role(client_id, role):
                player = self.active_players.get(client_id)
                hidden_prompt = self.get_hidden_prompt(cmd, role)
                return f"[SYSTEM: {player['name']} core synthesized.]", hidden_prompt, True
            else:
                return f"[SYSTEM: Invalid role specified.]", None, True

        player = self.active_players.get(client_id)
        if not player:
            return "[SYSTEM: You must first select a role using /role [rolename]]", None, True

        if cmd == "/start":
            hidden_prompt = self.get_hidden_prompt(cmd, player.get('role_key') if player else None)
            return "[SYSTEM: SYNC COMPLETE. THE VANGUARD DREADNOUGHT HAS ECLIPSED NEO-KAGAMI. THE FORMAT SIGNAL IS ACTIVE. SURVIVE.]", hidden_prompt, True

        if cmd == "/lookaround":
            hidden_prompt = self.get_hidden_prompt(cmd, player.get('role_key') if player else None)
            return f"[SYSTEM: {player['name']} scans the area...]", hidden_prompt, True

        if cmd == "/explore":
            hidden_prompt = self.get_hidden_prompt(cmd, player.get('role_key') if player else None)
            return f"[SYSTEM: {player['name']} explores the area, looking for trouble...]", hidden_prompt, True
        
        if cmd == "/evolve":
            if player['name'] == 'The Husk' and player['level'] >= 10:
                if player.get('evolution_stage') == 1:
                    player.update(self.evolved_roles['husk_stage2'])
                    player['evolution_stage'] = 2
                    return "[SYSTEM: The transformation accelerates. You have evolved into The Hunted Husk.]", None, True
                elif player.get('evolution_stage') == 2:
                    player.update(self.evolved_roles['husk_stage3'])
                    player['evolution_stage'] = 3
                    return "[SYSTEM: The transformation is complete. You have become The Apex Husk.]", None, True
                else:
                    return "[SYSTEM: You have already reached your final form.]", None, True
            else:
                return "[SYSTEM: Evolution is not available for you at this time.]", None, True

        return None, None, False
    
    def process_ai_response(self, ai_text, player_data):
        if not player_data:
            return ai_text, player_data, None

        # Process XP
        xp_match = re.search(r'\[XP:\s*(\d+)\]', ai_text)
        xp_gained = False
        if xp_match:
            gained_xp = int(xp_match.group(1))
            xp_gained = True
            total_xp = player_data.get('xp', 0) + gained_xp
            level_ups = 0
            while total_xp >= 1000:
                total_xp -= 1000
                level_ups += 1
            player_data['level'] = player_data.get('level', 1) + level_ups
            player_data['xp'] = total_xp
            if level_ups:
                ai_text = re.sub(
                    r'\[XP:\s*(\d+)\]',
                    f"\n\n*** SYSTEM: You gained {gained_xp} XP and leveled up {level_ups} time(s)! Now level {player_data['level']}! ***",
                    ai_text
                )
            else:
                ai_text = re.sub(
                    r'\[XP:\s*(\d+)\]',
                    f"\n\n*** SYSTEM: You gained {gained_xp} XP. ***",
                    ai_text
                )

        # Process Objective
        objective_changed = False
        objective_match = re.search(r'\[OBJECTIVE:\s*(.*?)\]', ai_text)
        if objective_match:
            new_objective = objective_match.group(1).strip()
            player_data['objective'] = new_objective
            ai_text = re.sub(r'\[OBJECTIVE:\s*(.*?)\]', f"\n\n*** SYSTEM: New Objective > {new_objective} ***", ai_text)
            objective_changed = True
        
        # Process Loot Tags (<<ITEM:Name>>)
        item_found = False
        for item_match in re.findall(r'<<ITEM:(.*?)>>', ai_text):
            item_name = item_match.strip()
            if item_name:
                if not any(item.get('name') == item_name for item in player_data.get('inventory', [])):
                    player_data.setdefault('inventory', []).append({'name': item_name, 'image': None})
                    item_found = True
            ai_text = ai_text.replace(f'<<ITEM:{item_match}>>', '')

        # Process Image Tags (<<IMAGE:filename.png>>)
        image_url = None
        for image_match in re.findall(r'<<IMAGE:(.*?)>>', ai_text):
            image_name = image_match.strip()
            if image_name:
                image_url = self.image_assets.get(image_name)
            ai_text = ai_text.replace(f'<<IMAGE:{image_match}>>', '')

        # Process Damage Tags (<<DMG:X>>)
        damage_occurred = False
        for dmg_match in re.findall(r'<<DMG:(\d+)>>', ai_text):
            damage = int(dmg_match)
            player_data['hp'] = max(0, player_data.get('hp', 0) - damage)
            ai_text = ai_text.replace(f'<<DMG:{dmg_match}>>', f"\n\n*** SYSTEM: You took {damage} damage. ***")
            damage_occurred = True

        # Process Objective Tags (<<OBJECTIVE:New objective>>)
        for obj_match in re.findall(r'<<OBJECTIVE:(.*?)>>', ai_text):
            new_objective = obj_match.strip()
            if new_objective:
                player_data['objective'] = new_objective
                objective_changed = True
            ai_text = ai_text.replace(f'<<OBJECTIVE:{obj_match}>>', '')

        # Process Location
        location_match = re.search(r'\[SET_LOCATION:\s*(.*?)\]', ai_text)
        if location_match:
            new_location = location_match.group(1).strip()
            if new_location in self.locations:
                player_data['location'] = new_location
                player_data['location_image'] = self.locations[new_location]['image']
                ai_text = re.sub(r'\[SET_LOCATION:\s*(.*?)\]', f"\n\n*** SYSTEM: Location updated to > {new_location} ***", ai_text)

        # Save game state if anything changed
        if xp_gained or item_found or damage_occurred or objective_changed or location_match:
            try:
                # player id isn't provided here; upstream code uses client id mapping when calling save
                # we assume player_data contains an identifier 'client_id' when available
                client_id = player_data.get('client_id') if isinstance(player_data, dict) else None
                if client_id:
                    self.save_game(client_id)
            except Exception:
                pass

        return ai_text, player_data, image_url
