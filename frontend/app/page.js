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
  const [scrapID, setScrapID] = useState("cb93a105-ca2e-4d09-a1c8-c7243907eb62")
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
    <main className="flex min-h-screen flex-col items-center justify-between p-12">
      <Camera setJson={setScrapID} />
      <div className="w-full flex justify-center gap-4">
        <ViewScrap scrapID={scrapID} />
        {/* <div className="w-2/3">
          <BattleScrap
            scrap={scrapID}
          />
        </div> */}
        {/*
        <div className="w-1/3">
          <BattleScrap
            scrap={testRScrap}
          />
        </div> */}
        <ScrapPage/>


      </div>


    </main>
  );
}
