"use client"

import Image from "next/image";
import Camera from "./components/Camera";
import { useRef } from "react";
import BattleScrap from "./components/BattleScraps";
import ViewScrap from "./components/ViewScrap";


export default function Home() {
  const inputFile = useRef(null)
  const testScrap = {
    image: "/border_orange.png",
    currentHealth: 10,
    maxHealth: 20,
    name: "Orange",
    types: [
      { name: "plant", colour: "#9ACD32" },
      { name: "food", colour: "#FFFF99" },
    ],
    stats: {
      might: 1,
      speed: 2,
      health: 4,
      defence: 3
  },
  }

  const testRScrap = {
    image: "/rock.png",
    currentHealth: 18,
    maxHealth: 20,
    name: "Rock",
    types: [
      { name: "rock", colour: "#B8860B" },
    ],
    stats: {
      might: 1,
      speed: 2,
      health: 4,
      defence: 3
  },
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-12">
      <div className="w-full flex justify-center gap-4">
        {/* <div className="w-2/3">
          <BattleScrap
            scrap={testScrap}
          />
        </div>
        <div className="w-1/3">
          <BattleScrap
            scrap={testRScrap}
          />
        </div> */}

      <ViewScrap scrap={testScrap}/>
      
      </div>
      <Camera />
      
    </main>
  );
}
