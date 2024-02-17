"use client"

import Image from "next/image";
import camera from "./components/Camera";
import { useRef } from "react";
import Scrap from "./components/Scraps";

export default function Home() {
  const inputFile = useRef(null) 
  const testScrap = {
    image: "/orange.png",
    currentHealth: 4,
    maxHealth: 20,
    name: "Orange",
    types: [
      { name: "plant", colour:"#9ACD32"},
      { name: "food", colour:"#FFFF99"},
    ]
  }
  const onButtonClick = () => {
    // `current` points to the mounted file input element
    console.log("Thing happend!")
    inputFile.current.click();
    console.log(inputFile)
  };
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-12">
      <div className="w-full flex justify-center gap-4">
        <div className="w-2/3">
          <Scrap
            scrap={testScrap}
          />
        </div>
        <div className="w-1/3">
          <Scrap
            scrap={testScrap}
          />
        </div>
        
        
      </div>
      <button 
        className="p-4 rounded-full bg-slate-400"
        onClick={onButtonClick}
      >
        Hello Button!
        <input type="file" accept="image/jpeg" id="file" capture="camera" ref={inputFile} style={{display: 'none'}} />
      </button>
    </main>
  );
}
