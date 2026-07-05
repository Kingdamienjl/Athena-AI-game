import React, { useState } from 'react';
import CommandReference from './CommandReference';
import PlayersGuide from './PlayersGuide';
import AiChat from '../components/AiChat';

const clientId = Math.random().toString(36).substring(7);

interface InventoryItem {
    name: string;
    image: string | null;
}

interface PlayerData {
    name: string;
    hp: number;
    level: number;
    xp: number;
    inventory: InventoryItem[];
    objective: string;
    lore: string;
    backstory: string;
    equipped_weapon: string;
    location: string;
    location_image: string;
}

interface LogMessage {
    sender: string;
    text: string;
    timestamp: string;
}

const ASCII_AVATARS: { [key: string]: string } = {
    "Husk Stage 1": "(####)\n(####)\n(####)",
    "Husk Stage 2": "(####)\n(####)\n(####)",
    "Husk Stage 3": "(####)\n(####)\n(####)",
    "Analogue Hacker": "[010101]\n[101010]\n[010101]",
    "Severed Dominion": "O-|-O\nO-|-O\nO-|-O",
    "Sentinel Spider": "/\\_//\\\n\\\\_\\/_//",
    "Aegis Enforcer": "|-[+]-|\n|-[+]-|\n|-[+]-|",
    "GhostRoot Acolyte": "~*~*~\n*~*~*\n~*~*~",
    "Aethelgard Refugee": "(o.o)\n(o.o)\n(o.o)",
    "SolarGarden Thorn": "\"\"\"\n(*)\
\"\"\""
};

const roles = [
    'Husk Stage 1',
    'Husk Stage 2',
    'Husk Stage 3',
    'Analogue Hacker',
    'Severed Dominion',
    'Sentinel Spider',
    'Aegis Enforcer',
    'GhostRoot Acolyte',
    'Aethelgard Refugee',
    'SolarGarden Thorn'
];

export default function Home() {
    const [playerData, setPlayerData] = useState<PlayerData | null>(null);
    const [isGlossaryOpen, setIsGlossaryOpen] = useState(false);
    const [isReferenceOpen, setIsReferenceOpen] = useState(false);
    const [isGuideOpen, setIsGuideOpen] = useState(false);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [modalContent, setModalContent] = useState('');
    
    // Unified Game Log State holding text history + metadata
    const [gameLog, setGameLog] = useState<LogMessage[]>([
        { sender: "System", text: "Core initialized. Awaiting network synchronization...", timestamp: new Date().toLocaleTimeString() }
    ]);

    const addLogEntry = (sender: string, text: string) => {
        setGameLog(prev => [...prev, {
            sender,
            text,
            timestamp: new Date().toLocaleTimeString()
        }]);
    };

    return (
        <div className="flex h-screen w-full bg-black text-green-500 font-mono overflow-hidden select-none">
            {isModalOpen && (
                <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-sm p-4" onClick={() => setIsModalOpen(false)}>
                    <div className="relative w-full max-w-2xl max-h-[90vh] overflow-y-auto bg-zinc-950 p-6 md:p-8 border-2 border-cyan-800 shadow-[0_0_20px_#0891b2] rounded-md font-mono text-white" onClick={(e) => e.stopPropagation()}>
                        <button onClick={() => setIsModalOpen(false)} className="absolute top-4 right-6 text-zinc-500 hover:text-cyan-400 text-3xl font-bold leading-none transition-colors" aria-label="Close">
                            &times;
                        </button>
                        <div className="text-sm text-zinc-300 space-y-1 whitespace-pre-wrap">
                            {modalContent}
                        </div>
                    </div>
                </div>
            )}
            
            
            {/* MAIN GAMEPLAY PANEL */}
            <div className="flex-grow flex flex-col w-3/4 border-r border-zinc-900 bg-black relative">
                
                {/* Visual Background Asset Layer */}
                {playerData && playerData.location_image && (
                    <div className="absolute inset-0 z-0 opacity-25 transition-opacity duration-1000 pointer-events-none">
                        <img 
                            src={playerData.location_image} 
                            alt={playerData.location} 
                            className="w-full h-full object-cover filtering-grayscale"
                            onError={(e) => {
                                // Fallback handling for local vs absolute web URLs
                                if(!playerData.location_image.startsWith('http')) {
                                    e.currentTarget.src = `/game_assets/${playerData.location_image}`;
                                }
                            }}
                        />
                    </div>
                )}

                {/* Top Terminal Header */}
                <div className="flex justify-between items-center p-4 border-b border-zinc-900 bg-black bg-opacity-80 z-10">
                    
                    <div className="flex gap-4">
                        <button 
                            onClick={() => {setModalContent("Current Objective: " + (playerData ? playerData.objective : 'No objective assigned')); setIsModalOpen(true);}} 
                            className="bg-zinc-800 text-white p-2 rounded"
                        > 
                            Objectives 
                        </button> 
                        <button 
                            onClick={() => {setModalContent("Commands: /lookaround, /explore, /roll [skill], /role [name]"); setIsModalOpen(true);}} 
                            className="bg-zinc-800 text-white p-2 rounded"
                        > 
                            Commands 
                        </button> 
                    </div>
                    <div className="text-sm border border-zinc-800 px-3 py-1 bg-zinc-950 uppercase tracking-widest text-zinc-400">
                        LOC: <span className="text-green-400">{playerData ? playerData.location : "UNLINKED"}</span>
                    </div>
                </div>

                {/* Unified Terminal Main Stream Output Log */}
                <div className="flex-1 overflow-y-auto p-6 relative z-10 bg-gradient-to-b from-transparent to-black/70 space-y-4 scrollbar-thin">
                    {gameLog.map((msg, i) => (
                        <div key={i} className="border-l-2 border-zinc-900 pl-4 py-1 animate-fade-in">
                            <div className="flex items-center space-x-3 text-xs mb-1">
                                <span className="text-zinc-600 font-bold">[{msg.timestamp}]</span>
                                <span style={{ 
                                    color: msg.sender === 'Player' || msg.sender === playerData?.name ? '#888' : 
                                           msg.sender === 'System' ? '#ff3333' : '#00ffff' 
                                }} className="font-bold tracking-wider uppercase">
                                    {msg.sender}
                                </span>
                            </div>
                            <p className="text-zinc-200 text-sm leading-relaxed tracking-wide whitespace-pre-wrap">{msg.text}</p>
                        </div>
                    ))}
                    
                    <button 
                        onClick={() => setIsReferenceOpen(true)} 
                        className="fixed bottom-32 right-[27%] z-20 text-lg bg-zinc-950 border border-zinc-800 hover:border-green-500 text-zinc-400 hover:text-white rounded-full w-10 h-12 flex items-center justify-center transition-all duration-200 shadow-xl"
                    >
                        ?
                    </button>
                </div>

                {/* Integrated Input Interface Component Wrapper */}
                <div className="w-full shrink-0 z-20">
                    <AiChat 
                        clientId={clientId} 
                        playerData={playerData} 
                        onPlayerDataChange={(newData) => setPlayerData(newData)}
                        onLogUpdate={addLogEntry}
                        currentName={playerData?.name ? playerData.name : "Player"}
                    />
                </div>
            </div>

            {/* PERSISTENT SIDEBAR STATUS DIAGNOSTIC */}
            <div className="w-1/4 min-w-[300px] bg-black border-l border-zinc-900 flex flex-col p-4 z-10">
                <h2 className="text-md font-bold tracking-widest text-zinc-500 uppercase border-b border-zinc-900 pb-2 mb-4">Diagnostic Module</h2>
                <div className="bg-zinc-950 border border-zinc-900 p-4 mb-4">
                    <pre className="text-green-500 text-center text-xs leading-tight font-bold">{playerData ? (ASCII_AVATARS[playerData.name] || "UNKNOWN CORE") : "NO CORE CONNECTED\nInitialize via chat Input."}</pre>
                </div>
                
                {playerData && (
                    <div className="space-y-3 text-sm flex-grow">
                        <div className="flex justify-between border-b border-zinc-950 pb-1"><span className="text-zinc-500">IDENTITY:</span><span className="text-cyan-400 font-bold">{playerData.name}</span></div>
                        <div className="flex justify-between border-b border-zinc-950 pb-1"><span className="text-zinc-500">VITALITY STATUS:</span><span className="text-red-500 font-bold">{playerData.hp} HP</span></div>
                        <div className="flex justify-between border-b border-zinc-950 pb-1"><span className="text-zinc-500">RUNTIME LEVEL:</span><span className="text-amber-500 font-bold">LVL {playerData.level}</span></div>
                        <div className="flex justify-between border-b border-zinc-950 pb-1"><span className="text-zinc-500">MEMORY INDEX:</span><span className="text-blue-400 font-bold">{playerData.xp} / 1000 XP</span></div>
                        
                        <div className="pt-4">
                            <h3 className="text-xs font-bold text-zinc-500 uppercase tracking-widest mb-2">Inventory Ledger</h3>
                            <ul className="text-xs space-y-1 bg-zinc-950 p-2 border border-zinc-950 max-h-32 overflow-y-auto">
                                {playerData.inventory.length === 0 ? (
                                    <li className="text-zinc-700 italic">Empty register</li>
                                ) : (
                                    playerData.inventory.map((item, idx) => (
                                        <li key={idx} className="text-zinc-300 font-bold">- {item.name.replace(/_/g, ' ')}</li>
                                    ))
                                )}
                            </ul>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}