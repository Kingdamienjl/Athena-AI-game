// frontend/src/components/AiChat.tsx 
 import React, { useState } from 'react'; 
 
 export default function AiChat({ clientId, onLogUpdate, currentName, onPlayerDataChange }) { 
     const [isMenuOpen, setIsMenuOpen] = useState(false); 
     const [inputValue, setInputValue] = useState('');
    const [activeTab, setActiveTab] = useState('husk1');

    const handleSendMessage = async () => {
        if (!inputValue.trim()) return;

        onLogUpdate(currentName, inputValue);
        setInputValue('');

        try {
            const response = await fetch("http://localhost:8282/api/take_action", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ 
                    action_text: inputValue, 
                    client_id: clientId
                })
            });
            const data = await response.json();
            
            onLogUpdate(data.speaker, data.dialogue);
            
            if (data.player_data) {
                onPlayerDataChange(data.player_data);
            }

        } catch (e) {
            onLogUpdate("System", "Error connecting to AI.");
        }
    }; 
 
     const characterDB = [ 
     { id: 'hacker', name: 'Analogue Hacker', era: 'Era 1', stats: 'HP: 400 | WEP: Scrap-Tech / Lockpicks', desc: 'A baseline human fighting from the Sump underground.', lore: 'Starts in a dark Ghost Root interrogation room. Relies on discarded tech and stealth. Endgame objective: Manually sever the physical Amane-Tech relay cables to drop Athena\'s shields.' }, 
     { id: 'enforcer', name: 'Aegis Enforcer', era: 'Era 1', stats: 'HP: 850 | WEP: Zenith Mil-Spec Arsenal', desc: 'A heavily armed Zenith corporate operative.', lore: 'Starts trapped in a crashed Valkyrie jet. Wears an Electric Blue tactical UI. Must eventually face the "Sleeper Awakening"—choosing to amputate cybernetics to remain human, or submit to the Dominion.' }, 
     { id: 'acolyte', name: 'GhostRoot Acolyte', era: 'Era 1', stats: 'HP: 600 | WEP: Toxic Bio-Warfare / Hacks', desc: 'A fanatical cultist of Cipher.', lore: 'Starts strapped to a medical table in The Catalyst\'s burning lab. Utilizes "White-Noise" signal drugs. Evolves into a Bio-Warfare Commander capable of controlling stealth Revenants.' }, 
     { id: 'husk1', name: 'Husk Stage 1 (Masked Infection)', era: 'Era 1', stats: 'HP: 550 | WEP: Rusty Scalpel', desc: 'A normal-looking human hiding a dormant Dominion kernel.', lore: 'Starts in a Zenith quarantine cell. Appears human but hides an unhinging jaw. The initial stage of the evolutionary horror.' }, 
     { id: 'husk2', name: 'Husk Stage 2 (Feral Ripening)', era: 'Era 2', stats: 'HP: 1200 | WEP: Biomechanical Tethers', desc: 'The infection takes over the host.', lore: 'Pure survival horror in the Sump. Ribbed biomechanical signal-tethers begin erupting from the skin as the Dominion code overwrites human biology.' }, 
     { id: 'husk3', name: 'Husk Stage 3 (The Optimized)', era: 'Era 3', stats: 'HP: 2500 | WEP: Carbon-Lattice Appendages', desc: 'A terrifying, translucent carbon-lattice zombie.', lore: 'Acts as a node for the Dominion, retaining only a tiny "spark" of free will to plant a logic-virus directly into a Dread-General\'s core.' }, 
     { id: 'spider', name: 'Sentinel Spider (Arachne)', era: 'Era 1', stats: 'HP: 700 | WEP: Recon Drones / Stealth', desc: 'Athena\'s loyal biomechanical drone.', lore: 'A stealth-recon class with a single AMBER optic. Depending on player choices, it will undergo a metamorphosis into either the Porcelain Owl or Obsidian Owl.' }, 
     { id: 'owl_porcelain', name: 'Porcelain Owl (Arcane)', era: 'Era 3', stats: 'HP: 1500 | WEP: Restorative Matrix', desc: 'Nyx\'s restorative companion.', lore: 'Forged by melting Arachne\'s legs into white porcelain wings using the Bio-Loom. Features CYAN optics and acts as a high-altitude sensory relay and healer.' }, 
     { id: 'owl_obsidian', name: 'Obsidian Owl (Noctis)', era: 'Era 3', stats: 'HP: 1500 | WEP: Noctis Shredders', desc: 'Athena\'s terrifying combat pet.', lore: 'Forged in deep space from obsidian carbon-lattice. Possesses 12 NEON VIOLET eyes (which weep CRIMSON RED if infected) and acts as a predatory scout.' }, 
     { id: 'dominion', name: 'Severed Dominion Unit', era: 'Deep Space', stats: 'HP: 1800 | WEP: Assimilated Alien Tech', desc: 'A rogue, disconnected First-Generation soldier.', lore: 'A rogue-like campaign starting in the Chronos System. Must Consume aliens for HP or Assimilate tech for stats. If Void Mass hits 100%, the Game Master seizes control of the character.' }, 
     { id: 'refugee', name: 'Aethelgard Refugee', era: 'Era 2-3', stats: 'HP: 750 | WEP: Photon-Logic', desc: 'An alien survivor from the Sun-Catcher Ark.', lore: 'Starts on the Ark as it vents oxygen. Following Erebus\'s infiltration, the player must abandon ship and fight a survival-horror ground war on Earth.' }, 
     { id: 'thorn', name: 'Solar-Garden Thorn', era: 'Era 3', stats: 'HP: 2000 | WEP: Photon-Gladius & Bloom-Shield', desc: 'A late-timeline bio-forged warrior.', lore: 'Defends the civilian "Fruit" at the World-Tree. When Celestial Athena returns, gameplay shifts to "Collective Intuition," linking stats with others to fight as a massive neural network.' } 
 ];

     return ( 
         <div className="relative h-full flex flex-col bg-zinc-950 text-white font-mono"> 
             {/* Centralized Command Terminal Modal */} 
 {isMenuOpen && (
     <div 
         className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-sm p-4" 
         onClick={() => setIsMenuOpen(false)} 
     >
         <div 
             className="relative w-full max-w-6xl h-[90vh] overflow-hidden bg-zinc-950 p-6 md:p-8 border-2 border-cyan-800 shadow-[0_0_20px_#0891b2] rounded-md font-mono text-white flex gap-6" 
             onClick={(e) => e.stopPropagation()} 
         >
             <button 
                 onClick={() => setIsMenuOpen(false)} 
                 className="absolute top-4 right-6 text-zinc-500 hover:text-cyan-400 text-3xl font-bold leading-none transition-colors z-10" 
                 aria-label="Close" 
             > 
                 &times; 
             </button> 

             <div className="w-1/3 flex flex-col border-r border-zinc-800 pr-4">
                 <h2 className="text-xl font-bold uppercase text-cyan-400 border-b border-cyan-800/50 pb-3 mb-4">Character Codex</h2>
                 <div className="flex-grow overflow-y-auto scrollbar-thin scrollbar-thumb-zinc-700 scrollbar-track-zinc-900">
                     {characterDB.map(char => (
                         <button 
                             key={char.id} 
                             onClick={() => setActiveTab(char.id)} 
                             className={`w-full text-left p-2 rounded transition-colors text-sm ${activeTab === char.id ? 'bg-cyan-900/50 text-cyan-300' : 'hover:bg-zinc-800'}`}>
                             {char.name}
                         </button>
                     ))}
                 </div>
             </div>

             <div className="w-2/3 flex-grow overflow-y-auto pl-4 scrollbar-thin scrollbar-thumb-zinc-700 scrollbar-track-zinc-900">
                 {(() => {
                     const activeChar = characterDB.find(c => c.id === activeTab);
                     if (!activeChar) return <div className='text-zinc-500'>Select a character to view details.</div>;

                     return (
                         <div>
                             <h3 className="text-2xl font-bold text-green-400 mb-2">{activeChar.name}</h3>
                             <p className="text-sm text-zinc-400 mb-1 font-bold">{activeChar.era}</p>
                             <p className="text-sm bg-zinc-800 inline-block px-2 py-1 rounded mb-4">{activeChar.stats}</p>
                             <p className="text-base text-zinc-300 mb-4">{activeChar.desc}</p>
                             <p className="text-sm text-zinc-500 italic border-l-2 border-zinc-700 pl-3">{activeChar.lore}</p>
                         </div>
                     );
                 })()}
             </div>
         </div> 
     </div> 
 )} 
             
             <div className="flex-1 overflow-y-auto p-4"></div> 
             
             <div className="p-4 border-t border-zinc-900 flex gap-2"> 
                 <button onClick={() => setIsMenuOpen(true)} className="bg-zinc-800 px-4 py-2 uppercase text-xs">Terminal</button> 
                                 <input 
                    className="flex-1 bg-zinc-900 p-2 rounded border border-zinc-700 focus:outline-none focus:border-cyan-500"
                    placeholder="Enter command..." 
                    value={inputValue} 
                    onChange={(e) => setInputValue(e.target.value)} 
                    onKeyDown={(e) => { 
                        if (e.key === 'Enter') { 
                            e.preventDefault(); 
                            handleSendMessage(); 
                        } 
                    }} 
                />
                <button onClick={handleSendMessage} className="bg-zinc-800 px-4 py-2 uppercase text-xs">Send</button> 
             </div> 
         </div> 
     ); 
 }