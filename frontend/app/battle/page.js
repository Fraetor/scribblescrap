"use client"

import BattleScrap from "../components/BattleScraps"
import { useSearchParams } from 'next/navigation'
import { useRouter } from 'next/navigation';
import { useState } from "react";
import { useEffect, useRef } from "react";
import { useInterval } from "./utils";

export default function BattlePage() {
    const searchParams = useSearchParams()
    const battleID = searchParams.get("id")
    const router = useRouter()
    const [battle, setBattle] = useState()
    const [thisScribble, setThisScribble] = useState()

    useEffect(() => {
        if (battleID == null) {
            router.push("/")
        }

        let scribbleID = null

        fetch(`/api/`+battleID+"/status", {
            method: 'GET',
        })
            .then(response => response.json())
            .then(data => {
                console.log("got battle data", data)
                setBattle(data)
                scribbleID = data.player1.scribble_id

                 fetch(`/api/scribble/${scribbleID}/info`, {
                    method: "GET",
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log("got this scribble:", data)
                        setThisScribble(data)
                    })
                    .catch(error => {
                        console.error("Error:", error)
                    })
            })
            .catch(error => {
                // Handle error
                console.error('Error:', error);
            })

    }, []);

    useInterval(() => {
        fetch(`/api/`+battleID+"/status", {
            method: 'GET',
        })
            .then(response => response.json())
            .then(data => {
                console.log("got battle data", data)
                setBattle(data)
                console.log("new data=", data)
            })
            .catch(error => {
                // Handle error
                console.error('Error:', error);
            })
    }, 1000)

    if (battle == null) {
        return <div>Loading...</div>
    }

    if (battle.player2) {
        return (
            <div className="min-h-screen flex flex-col p-4">
                <div className="flex flex-row gap-2">
                    <div className="w-3/5">
                        <BattleScrap
                            scrapID={battle.player1.scribble_id}
                        />
                    </div>
                    <div className="w-2/5">
                        <BattleScrap
                            scrapID={battle.player2.scribble_id}
                        />
                    </div>
                </div>
                <div className="h-16"></div>
                <div className="grid columns-1 gap-4">
                    <button className="rounded-lg border-black bg-orange-600 hover:bg-orange-800 cursor-pointer p-4 text-white text-2xl">
                        {thisScribble ? thisScribble.attack_1_name : "..."} ({thisScribble ? thisScribble.attack_1 : "..."})
                    </button>
                    <button className="rounded-lg border-black bg-orange-600 hover:bg-orange-800 cursor-pointer p-4 text-white text-2xl">
                        {thisScribble ? thisScribble.attack_2_name : "..."} ({thisScribble ? thisScribble.attack_2 : "..."})
                    </button>
                </div>
            </div>
        );
    } else {
        return (
            <div className="min-h-screen flex flex-col p-4">
                <div className="flex flex-row gap-2">
                    <div className="w-1/3">
                        <BattleScrap
                            scrapID={battle.player1.scribble_id}
                        />
                    </div>
                    <div className="w-2/3">
                        <img className="w-full" src={`/api/${battle.battle_id}/qr`} />
                        <div className="text-center text-5xl">
                            Join with the QR code ⚔️
                        </div>
                    </div>
                </div>
                <div className="h-16"></div>
                <div className="grid columns-1 gap-4">
                    <button className="rounded-lg border-black bg-orange-600 hover:bg-orange-800 cursor-pointer p-4 text-white text-2xl">
                        {thisScribble ? thisScribble.attack_1_name : "..."} ({thisScribble ? thisScribble.attack_1 : "..."})
                    </button>
                    <button className="rounded-lg border-black bg-orange-600 hover:bg-orange-800 cursor-pointer p-4 text-white text-2xl">
                        {thisScribble ? thisScribble.attack_2_name : "..."} ({thisScribble ? thisScribble.attack_2 : "..."})
                    </button>
                </div>
            </div>
        );
    }
}
