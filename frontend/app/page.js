"use client"

import Image from "next/image";
import camera from "./components/Camera";
import { useRef } from "react";

export default function Home() {
  const inputFile = useRef(null) 
  const onButtonClick = () => {
    // `current` points to the mounted file input element
    console.log("Thing happend!")
    inputFile.current.click();
    console.log(inputFile)
  };
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="bg-black text-white">
      {inputFile.toString()}
      </div>
      <button 
        className="p-4 rounded-full bg-slate-400"
        onClick={onButtonClick}
      >
        Hello Button!
        <input type="file" accept="image/*" id="file" capture="camera" ref={inputFile} style={{display: 'none'}} />
      </button>
    </main>
  );
}
