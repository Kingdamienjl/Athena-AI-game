
import React, { useState } from 'react';

interface PlayerData {
    name: string;
    objective: string;
    lore: string;
    backstory: string;
}

interface PlayersGuideProps {
    playerData: PlayerData | null;
    onClose: () => void;
}

const campaignData: { [key: string]: { title: string, timeline: string } } = {
    'The Hacker': { title: 'Campaign A: The Analogue Hacker', timeline: 'Earth Survival' },
    'The Husk': { title: 'Campaign B: The Evolving Husk', timeline: 'The Inside Job' },
    'The Severed Unit': { title: 'Campaign C: Severed Dominion Unit', timeline: 'Space Rogue-like' }
};

const PlayersGuide: React.FC<PlayersGuideProps> = ({ playerData, onClose }) => {
    const [isLoreExpanded, setIsLoreExpanded] = useState(false);

    if (!playerData) {
        return null; // Or a loading/error state
    }

    const characterCampaign = campaignData[playerData.name];

    return (
        <div className="fixed inset-0 bg-black bg-opacity-85 flex items-center justify-center z-50" onClick={onClose}>
            <div className="bg-gray-900 border border-amber-400 p-8 rounded-lg text-white max-w-2xl w-full" onClick={e => e.stopPropagation()}>
                <h2 className="text-2xl font-bold mb-2 text-amber-400">OBJECTIVE LOG</h2>
                {characterCampaign && (
                    <div className="mb-6">
                        <h3 className="font-bold text-lg text-cyan-400">{characterCampaign.title}</h3>
                        <p className="text-sm text-gray-400 italic">Timeline: {characterCampaign.timeline}</p>
                    </div>
                )}
                <div className="mb-6">
                    <h4 className="font-bold text-green-400">CURRENT DIRECTIVE:</h4>
                    <p className="text-lg text-gray-200 mt-1">{playerData.objective || 'Objective not set.'}</p>
                </div>

                <div className="border-t border-gray-700 pt-4 mt-4">
                    <button 
                        onClick={() => setIsLoreExpanded(!isLoreExpanded)}
                        className="text-cyan-400 font-bold hover:text-cyan-300 transition-colors duration-200"
                    >
                        {isLoreExpanded ? 'Hide' : 'Show'} Character Dossier
                    </button>
                    {isLoreExpanded && (
                        <div className="mt-4 animate-fade-in-down">
                            <h4 className="font-bold text-amber-400 mb-2">LORE:</h4>
                            <p className="text-gray-300 italic mb-4">{playerData.lore}</p>
                            <h4 className="font-bold text-amber-400 mb-2">BACKSTORY:</h4>
                            <p className="text-gray-300">{playerData.backstory}</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default PlayersGuide;
