
import React, { useState, useEffect, useRef } from 'react';
import clash01 from '../assets/images/clash_01.png';
import CommandReference from './CommandReference';
import PlayersGuide from './PlayersGuide';

const clientId = Math.random().toString(36).substring(7);

const imageAssets: { [key: string]: string } = {
    'CLASH_01': clash01,
    'Hint_Breached_Server': clash01, 
};

interface InventoryItem {
    name: string;
    image: string | null;
}

interface ChatMessage {
    sender: string;
    content: string | object;
    imageUrl?: string | null;
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

const ASCII_AVATARS: { [key: string]: string } = {
    "The Hacker": `
    [010101]
    [101010]
    [010101]
    `,
    "The Husk": `
    (####)
    (####)
    (####)
    `,
    "The Severed Unit": `
    O-|-O
    O-|-O
    O-|-O
    `,
    "The Sentinel": `
    /\\_//\\    \\\\_\\/_//
    / /  \\\\ \\\\
    `,
    "Aegis Enforcer": `
    |-[+]-|
    |-[+]-|
    |-[+]-|
    `,
    "Ghost Root Acolyte": `
    ~*~*~
    *~*~*
    ~*~*~
    `,
};

const CommandMenu: React.FC<{ onClose: () => void }> = ({ onClose }) => (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50" onClick={onClose}>
        <div className="bg-gray-900 border border-green-500 p-8 rounded-lg text-white max-w-4xl w-full" onClick={e => e.stopPropagation()}>
            <h2 className="text-2xl font-bold mb-4 text-cyan-400">COMMAND GLOSSARY</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                    <h3 className="font-bold text-cyan-400 mb-2">1. CORE COMMANDS</h3>
                    <ul className="mb-4 text-sm">
                        <li className="mb-1"><span className="font-bold">/stats</span> &gt; View your current stats, level, XP, and inventory.</li>
                        <li className="mb-1"><span className="font-bold">/use [item name]</span> &gt; Consume an item from your inventory (e.g., /use system_reboot_can).</li>
                        <li className="mb-1"><span className="font-bold">/evolve</span> &gt; If you are a Husk at level 10, use this to evolve.</li>
                    </ul>

                    <h3 className="font-bold text-cyan-400 mb-2">2. GAMEPLAY</h3>
                    <ul className="mb-4 text-sm">
                        <li className="mb-1">- Type naturally to narrate actions (e.g., "I check the console for access logs").</li>
                        <li className="mb-1">- The AI Game Master narrates the world's reaction.</li>
                        <li className="mb-1">- When the GM asks you to "Roll a d20", it means the outcome is uncertain.</li>
                    </ul>
                </div>

                <div>
                    <h3 className="font-bold text-cyan-400 mb-2">3. AVAILABLE ROLES (/role [name])</h3>
                    <p className="text-xs mb-2 text-gray-400">Select one to begin your session.</p>
                    <ul className="text-sm grid grid-cols-2 gap-x-4">
                        <li>hacker</li>
                        <li>husk</li>
                        <li>severed_unit</li>
                        <li>sentinel</li>
                        <li>aegis_enforcer</li>
                        <li>ghost_root_acolyte</li>
                        <li>chroma_key</li>
                        <li>echo_runner</li>
                        <li>titan_pilot</li>
                        <li>neural_weaver</li>
                        <li>aethelgard_knight</li>
                        <li>solargarden_thorn</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
);

const EquippedWeapon: React.FC<{ playerData: PlayerData }> = ({ playerData }) => {
    const weapon = playerData.inventory.find(item => item.name === playerData.equipped_weapon);

    if (!weapon || !weapon.image) {
        return null;
    }

    return (
        <div className="mt-4 p-2 border border-amber-400 rounded">
            <h3 className="font-bold text-amber-400">EQUIPPED</h3>
            <img src={weapon.image} alt={weapon.name} className="w-full h-auto mt-2" />
            <p className="text-center text-sm mt-1">{weapon.name}</p>
        </div>
    );
};

const LocationImage: React.FC<{ playerData: PlayerData | null, onClose: () => void }> = ({ playerData, onClose }) => {
    if (!playerData || !playerData.location_image) {
        return null;
    }

    return (
        <div className="fixed inset-0 bg-black bg-opacity-85 flex items-center justify-center z-50" onClick={onClose}>
            <div className="bg-gray-900 border border-amber-400 p-8 rounded-lg text-white max-w-4xl w-full" onClick={e => e.stopPropagation()}>
                <h2 className="text-2xl font-bold mb-4 text-amber-400">{playerData.location}</h2>
                <img src={playerData.location_image} alt={playerData.location} className="w-full h-auto" />
            </div>
        </div>
    );
};

const Sidebar: React.FC<{ playerData: PlayerData | null }> = ({ playerData }) => {
    const renderPortrait = () => {
        if (!playerData) {
            return <div className="text-amber-400">NO CORE DETECTED</div>;
        }
        return <pre className="text-green-400">{ASCII_AVATARS[playerData.name] || "NO AVATAR"}</pre>;
    };

    return (
        <div className="w-1/4 bg-black p-4 border-l border-green-700 flex flex-col">
            <p className="text-amber-400 mb-4">CURRENT LOCATION: {playerData ? `[${playerData.location}]` : '[Unknown]'}</p>
            <div className="w-[120px] h-[120px] border-2 border-green-500 mx-auto mb-4 flex items-center justify-center">
                {renderPortrait()}
            </div>
            {playerData && (
                <div className="text-sm">
                    <h2 className="text-xl font-bold mb-2 text-cyan-400">{playerData.name}</h2>
                    <div className="mb-4 p-2 border border-amber-400 rounded">
                        <h3 className="font-bold text-amber-400">CURRENT OBJECTIVE</h3>
                        <p className="text-sm text-green-300 mt-1">{playerData.objective || "Establish contact."}</p>
                    </div>
                    <p>Level: {playerData.level}</p>
                    <p>HP: {playerData.hp}</p>
                    <p>XP: {playerData.xp} / 1000</p>
                    <h3 className="font-bold mt-4 mb-2 text-cyan-400">Inventory</h3>
                    <ul>
                        {playerData.inventory.map((item, i) => <li key={i}>{item.name}</li>)}
                    </ul>
                    <EquippedWeapon playerData={playerData} />
                </div>
            )}
        </div>
    );
};

const Home: React.FC = () => {
    const [inputValue, setInputValue] = useState('');
    const [chatLog, setChatLog] = useState<ChatMessage[]>([]);
    const [playerData, setPlayerData] = useState<PlayerData | null>(null);
    const [isGlossaryOpen, setIsGlossaryOpen] = useState(false);
    const [isReferenceOpen, setIsReferenceOpen] = useState(false);
    const [isGuideOpen, setIsGuideOpen] = useState(false);
    const [isLocationOpen, setIsLocationOpen] = useState(false);
    const ws = useRef<WebSocket | null>(null);

    useEffect(() => {
        ws.current = new WebSocket(`ws://localhost:8282/ws/${clientId}`);

        ws.current.onopen = () => {
            console.log('connected');
        };

        ws.current.onmessage = (event) => {
            const messageData = JSON.parse(event.data);
            if (messageData.sender === "PlayerData") {
                setPlayerData(messageData.content);
            } else {
                setChatLog(prev => [...prev, messageData]);
            }
        };

        ws.current.onclose = () => {
            console.log('disconnected');
        };

        return () => {
            ws.current?.close();
        };
    }, []);

    const sendMessage = (event: React.FormEvent) => {
        event.preventDefault();
        if (inputValue && ws.current) {
            ws.current.send(inputValue);
            setInputValue('');
        }
    };

    const renderMessage = (msg: ChatMessage, index: number) => {
        const isGMSender = msg.sender === 'Athena (GM)' || msg.sender === 'System';
        const alignmentClass = isGMSender ? 'text-left' : 'text-right';
        
        let messageText = typeof msg.content === 'string' ? msg.content : JSON.stringify(msg.content);
        let imageUrl: string | null = null;

        if (msg.imageUrl) {
            imageUrl = msg.imageUrl;
        }

        const imageMatch = messageText.match(/\[RENDER_IMG: (.*?)\]/);
        if (imageMatch) {
            const imageName = imageMatch[1];
            imageUrl = imageAssets[imageName] || imageUrl;
            messageText = messageText.replace(/\[RENDER_IMG: (.*?)\]/, '');
        }

        return (
            <div key={index} className={`mb-2 ${alignmentClass}`}>
                <p style={{ whiteSpace: 'pre-wrap' }}><span className="text-cyan-400">{msg.sender || 'User'}:</span> {messageText}</p>
                {imageUrl && (
                    <img src={imageUrl} alt={imageMatch ? imageMatch[1] : 'Game Image'} className="mt-2 w-full max-w-md mx-auto" />
                )}
            </div>
        );
    };

    return (
        <div className="flex h-screen bg-gray-900 text-green-400 font-mono">
            {isGlossaryOpen && <CommandMenu onClose={() => setIsGlossaryOpen(false)} />}
            {isReferenceOpen && <CommandReference onClose={() => setIsReferenceOpen(false)} />}
            {isGuideOpen && <PlayersGuide playerData={playerData} onClose={() => setIsGuideOpen(false)} />}
            {isLocationOpen && <LocationImage playerData={playerData} onClose={() => setIsLocationOpen(false)} />}
            <div className="flex-grow flex flex-col p-4 w-3/4">
                <div className="absolute top-4 left-4 z-20 flex space-x-4">
                    <button onClick={() => setIsGlossaryOpen(true)} className="text-3xl">≡</button>
                    <button onClick={() => setIsGuideOpen(true)} className="text-3xl">📖</button>
                </div>
                <div className="absolute top-4 right-4 z-20 flex space-x-4">
                    <button onClick={() => setIsLocationOpen(true)} className="text-3xl">🌍</button>
                </div>
                <div className="flex-grow overflow-y-auto mb-4 pt-12">
                    {chatLog.map(renderMessage)}
                </div>
                <div className="absolute bottom-4 right-4 z-20">
                    <button onClick={() => setIsReferenceOpen(true)} className="text-3xl bg-gray-800 border border-green-500 rounded-full w-12 h-12 flex items-center justify-center">?</button>
                </div>
                <form onSubmit={sendMessage} className="flex">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        className="flex-1 bg-gray-800 text-green-400 p-3 rounded outline-none border border-green-500 z-10 relative"
                        autoFocus
                    />
                </form>
            </div>
            <Sidebar playerData={playerData} />
        </div>
    );
};

export default Home;
