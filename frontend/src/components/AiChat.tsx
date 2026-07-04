import React, { useState } from 'react';

interface AiChatProps {
    clientId: string;
    playerData: any;
    onPlayerDataChange: (newPlayerData: any) => void;
    onLogUpdate: (sender: string, text: string) => void;
    currentName: string;
}

export default function AiChat({ clientId, playerData, onPlayerDataChange, onLogUpdate, currentName }: AiChatProps) {
    const [input, setInput] = useState("");
    const [showMenu, setShowMenu] = useState(false);

    const sendMessage = async () => {
        if (!input.trim()) return;

        onLogUpdate(currentName, input);
        setInput("");

        try {
            const response = await fetch("http://localhost:8282/api/take_action", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ 
                    action_text: input, 
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

    return (
        <div className="relative border-t border-zinc-900 bg-black/50 p-4">
            <button onClick={() => setShowMenu(!showMenu)} className="absolute -top-10 right-4 z-10 bg-zinc-800 text-xs uppercase tracking-widest px-3 py-1 text-white hover:bg-green-500 hover:text-black transition-colors duration-200">
                Commands Menu
            </button>
            
            {showMenu && (
                <div className="absolute inset-0 bg-black/95 p-6 z-20 overflow-y-auto text-white">
                    <h2 className="text-xl font-bold mb-4 text-cyan-400">Game Commands & Roles</h2>
                    <p className="mb-2"><strong className="text-cyan-400">Roles:</strong> Husk, Hacker, Dominion, Spider...</p>
                    <p className="mb-2"><strong className="text-cyan-400">Commands:</strong> /lookaround, /explore, /roll [Stat]</p>
                    <p className="mt-4 italic text-zinc-400">Tip: You can speak freely to the Game Master.</p>
                    <button onClick={() => setShowMenu(false)} className="mt-6 bg-green-500 text-black font-bold px-4 py-2 hover:bg-green-400 transition-colors duration-200">Close</button>
                </div>
            )}

            <div className="flex items-center bg-zinc-950 border border-zinc-800 focus-within:border-green-500 transition-all duration-200">
                <input 
                    type="text" 
                    value={input} 
                    onChange={(e) => setInput(e.target.value)} 
                    onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder={`Type your action as ${currentName}...`}
                    className="flex-1 bg-transparent text-zinc-200 text-sm p-3 outline-none"
                />
                <button 
                    onClick={sendMessage} 
                    className="text-xs uppercase tracking-widest bg-zinc-800 text-zinc-400 hover:bg-green-500 hover:text-black font-bold p-3 transition-colors duration-200"
                >
                    Send
                </button>
            </div>
        </div>
    );
}