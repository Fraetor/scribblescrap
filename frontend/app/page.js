"use client"

import Image from "next/image";
import Camera from "./components/Camera";
import { useRef, useState } from "react";
import BattleScrap from "./components/BattleScraps";
import ViewScrap from "./components/ViewScrap";
import { useGetCookie } from "./components/getCookie";
import { useEffect } from "react";
import ScrapPage from "./components/ScrapPage";


export default function Home() {
  const [mode, setMode] = useState("box")
  const [scrapID, setScrapID] = useState(null)
  const inputFile = useRef(null)
  const [username, setUsername] = useState('');

  const cookie = useGetCookie('username');

  useEffect(() => {
    console.log(cookie)
    if (cookie) {
      setUsername(cookie);
    }
  }, [cookie]);

  if (username === "") {
    console.log(username)
    return (
      <div className="text-black w-full text-center text-4xl pt-4">Please Login</div>
    )
  }

  return (
    <main className="flex min-h-screen flex-col items-center pt-0 p-12">
      <div className="grid grid-cols-2">
        <button className={`p-4 rounded-bl-lg ${(mode == "box") ? "bg-orange-600" : "bg-orange-800"} text-white font-lg`} onClick={() => {setMode("cam")}}>New Scraps!</button>
        <button className={`p-4 rounded-br-lg ${(mode == "cam") ? "bg-orange-600" : "bg-orange-800"} text-white font-lg`} onClick={() => {setMode("box")}}>Scrap Book!</button>
      </div>
      <div className="w-full mb-4 flex justify-center gap-4">
        {(mode === "box") && (
          <ScrapPage/>
        )}
        {(mode === "cam") && (
          <div className="">
            <Camera setJson={setScrapID} />
            <ViewScrap scrapID={scrapID} />
          </div>
        )}
      </div>


    </main>
  );
}
