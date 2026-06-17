
import React from 'react';

const commands = [
    {
        category: 'Character & Session',
        commands: [
            {
                name: '/role [class_name]',
                description: 'Selects your character class at the start of a session. This can only be done once.',
                parameters: '`class_name`: The name of the class you want to play. Must be one of the available starting roles.',
                example: '`/role husk`',
                permissions: 'Can only be used before a role has been chosen.'
            },
            {
                name: '/stats',
                description: 'Displays your current character sheet, including your name, level, XP, stats, and inventory.',
                parameters: 'None',
                example: '`/stats`',
                permissions: 'Requires a character role to be selected.'
            },
            {
                name: '/lookaround',
                description: 'Triggers a detailed description of your immediate surroundings from the AI Game Master.',
                parameters: 'None',
                example: '`/lookaround`',
                permissions: 'Requires a character role to be selected.'
            }
        ]
    },
    {
        category: 'Interaction & Gameplay',
        commands: [
            {
                name: '/use [item_name]',
                description: 'Uses a consumable item from your inventory, applying its effects.',
                parameters: '`item_name`: The exact name of the item from your inventory, including underscores (e.g., `system_reboot_can`).',
                example: '`/use bio-gel_pack`',
                permissions: 'Item must be in your inventory.'
            },
            {
                name: 'Natural Language',
                description: 'Describe your actions, speech, or intentions using plain English. The AI Game Master will interpret your input and narrate the outcome.',
                parameters: 'None',
                example: '`I pick up the datapad and check for recent logs.`',
                permissions: 'Always available after selecting a role.'
            }
        ]
    },
    {
        category: 'Character Progression',
        commands: [
            {
                name: '/evolve',
                description: "Specific to the Husk class. Triggers your character's evolution to the next stage.",
                parameters: 'None',
                example: '`/evolve`',
                permissions: 'Only available to the Husk class at level 10 or higher.'
            }
        ]
    },
    {
        category: 'System (Admin)',
        commands: [
            {
                name: '/admin_grant [item_name]',
                description: 'Grants a specified item directly to your inventory. This is a hidden administrative command for testing.',
                parameters: '`item_name`: The exact name of the item to grant.',
                example: '`/admin_grant corporate_id_badge`',
                permissions: 'Admin only.'
            }
        ]
    }
];

const CommandReference: React.FC<{ onClose: () => void }> = ({ onClose }) => {
    return (
        <div className="fixed inset-0 bg-black bg-opacity-85 flex items-center justify-center z-50" onClick={onClose}>
            <div className="bg-gray-900 border border-amber-400 p-8 rounded-lg text-white max-w-5xl w-full h-3/4 overflow-y-auto" onClick={e => e.stopPropagation()}>
                <h2 className="text-3xl font-bold mb-6 text-amber-400">SYSTEM COMMAND REFERENCE</h2>
                {commands.map(category => (
                    <div key={category.category} className="mb-8">
                        <h3 className="font-bold text-xl text-cyan-400 mb-4 border-b border-cyan-700 pb-2">{category.category}</h3>
                        {category.commands.map(cmd => (
                            <div key={cmd.name} className="mb-6 pl-4">
                                <p className="font-bold text-lg text-green-400">{cmd.name}</p>
                                <p className="text-sm text-gray-300 mt-1">{cmd.description}</p>
                                <div className="mt-2 text-xs text-gray-400">
                                    <p><span className="font-bold text-gray-200">Parameters:</span> {cmd.parameters}</p>
                                    <p><span className="font-bold text-gray-200">Example:</span> <code className="bg-gray-800 p-1 rounded">{cmd.example}</code></p>
                                    <p><span className="font-bold text-gray-200">Permissions:</span> {cmd.permissions}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CommandReference;
