// frontend/src/components/AiChat.tsx 
 import React, { useState } from 'react'; 
 
 export default function AiChat({ clientId, onLogUpdate, currentName }) { 
     const [isMenuOpen, setIsMenuOpen] = useState(false); 
 
     return ( 
         <div className="relative h-full flex flex-col bg-zinc-950 text-white font-mono"> 
             {/* Centralized Command Terminal Modal */} 
 {isMenuOpen && ( 
     <div 
         /* 1. This creates the dark, clickable background that covers the whole screen */ 
         className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-sm p-4" 
         onClick={() => setIsMenuOpen(false)} 
     > 
         <div 
             /* 2. This is the actual menu box. It stops the click from closing the menu if you click inside it */ 
             className="relative w-full max-w-4xl max-h-[90vh] overflow-y-auto bg-zinc-950 p-6 md:p-8 border-2 border-cyan-800 shadow-[0_0_20px_#0891b2] rounded-md font-mono text-white" 
             onClick={(e) => e.stopPropagation()} 
         > 
             {/* 3. The Top-Right 'X' Close Button */} 
             <button 
                 onClick={() => setIsMenuOpen(false)} 
                 className="absolute top-4 right-6 text-zinc-500 hover:text-cyan-400 text-3xl font-bold leading-none transition-colors" 
                 aria-label="Close" 
             > 
                 &times; 
             </button> 
 
             <h2 className="text-2xl font-bold uppercase mb-6 text-cyan-400 border-b border-cyan-800/50 pb-3"> 
                 Athena Universe: Command Terminal 
             </h2> 
             
             <div className="grid grid-cols-1 md:grid-cols-2 gap-4"> 
                 {/* Example Content Card */} 
                 <div className="border border-zinc-800 bg-zinc-900/50 p-4 rounded"> 
                     <h3 className="text-green-400 font-bold mb-1">Husk Stage 1</h3> 
                     <p className="text-sm text-zinc-300">HP: 550 | Weapon: Rusty Scalpel</p> 
                     <p className="text-xs text-zinc-500 mt-2">Objective: Evolve</p> 
                 </div> 
                 
                 {/* Commands Reference */} 
                 <div className="border border-zinc-800 bg-zinc-900/50 p-4 rounded"> 
                     <h3 className="text-cyan-400 font-bold mb-1">System Commands</h3> 
                     <ul className="text-sm text-zinc-300 space-y-1"> 
                         <li><span className="text-yellow-400">/role [name]</span> - Switch character</li> 
                         <li><span className="text-yellow-400">/help</span> - Open this terminal</li> 
                     </ul> 
                 </div> 
             </div> 
 
             {/* Bottom Close Button for easy access */} 
             <div className="mt-8 flex justify-end border-t border-zinc-800/50 pt-4"> 
                 <button 
                     onClick={() => setIsMenuOpen(false)} 
                     className="bg-red-900/80 hover:bg-red-700 px-6 py-2 uppercase tracking-wider text-sm font-bold border border-red-500 transition-colors rounded" 
                 > 
                     Close Terminal 
                 </button> 
             </div> 
         </div> 
     </div> 
 )} 
             
             <div className="flex-1 overflow-y-auto p-4"></div> 
             
             <div className="p-4 border-t border-zinc-900 flex gap-2"> 
                 <button onClick={() => setIsMenuOpen(true)} className="bg-zinc-800 px-4 py-2 uppercase text-xs">Terminal</button> 
                 <input className="flex-1 bg-zinc-900 p-2" placeholder="Enter command..." /> 
             </div> 
         </div> 
     ); 
 }