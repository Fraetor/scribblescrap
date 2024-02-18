import Image from "next/image";
import HeathBar from "./healthBar";
import Canvas from "./Canvas";
import { useState, useEffect } from "react";
import ShareButton from "./ShareButton";


export default function ViewScrap({ scrapID }) {
    const [scrapObject, setScrapObject] = useState(null)

    useEffect(() => {
        if (scrapID == null) return

        fetch(`/api/scribble/`+scrapID.trimEnd()+"/info", {
            method: 'GET',
        })
            .then(response => response.json())
            .then(data => {
                console.log("got info data", data)
                setScrapObject(data)
            })
            .catch(error => {
                // Handle error
                console.error('Error:', error);
            });
    }, [scrapID]);



    if (scrapObject == null) {
        return (
            <div className="text-black"></div>
        )
    }

    let arms = []
    for (var arm of scrapObject.arms) {
        arms.push({
            "rx": arm.limb_anchor[0],
            "ry": arm.limb_anchor[1],
            "ox": arm.body_anchor[0] - 256,
            "oy": arm.body_anchor[1] - 256,
            "rot": arm.direction
        })
    }

    let legs = []
    for (var leg of scrapObject.legs) {
        legs.push({
            "rx": leg.limb_anchor[0],
            "ry": leg.limb_anchor[1],
            "ox": leg.body_anchor[0] - 256,
            "oy": leg.body_anchor[1] - 256,
            "rot": leg.direction
        })
    }

    const draw_conf = {
        "scrap_img_url": scrapObject.image,
        "arm_img_url": "arm.png",
        "eye_img_url": "eye.png",
        "leg_img_url": "leg.png",
        "sway_dist": 0.05,
        "sway_speed": 3,
        "arm_sway_dist": 0.1,
        "arm_sway_speed": 10,
        "leg_sway_dist": 0.1,
        "leg_sway_speed": 7,
        "arms": arms,
        "legs": legs,
        "eyes": [
            {
                "x": -80,
                "y": -55
            },
            {
                "x": 80,
                "y": -65
            }
        ]
    }

    return (
        <div className="w-full pb-2">
            <div className="text-yellow-500 text-center text-4xl mb-2 mt-4">You've found a {scrapObject.name || "???"}!</div>
            <div className="text-orange-500 text-center text-4xl mb-2 italic font-bold">{scrapObject.nickname || "???"}</div>
            <div className="grid grid-cols-4 gap-2" >
            <div className="text-md bg-red-800 p-2 rounded-full">
                <div className="text-center text-lg">Might</div>
                <div className="text-center text-2xl font-bold">{scrapObject.stats ? scrapObject.stats.might : "?"}</div>
            </div>
            <div className="text-md bg-yellow-500 p-2 rounded-full">
                <div className="text-center text-lg">Speed</div>
                <div className="text-center text-2xl font-bold">{scrapObject.stats ? scrapObject.stats.speed : "?"}</div>
            </div>
            <div className="text-md bg-pink-600 p-2 rounded-full">
                <div className="text-center text-lg">Health</div>
                <div className="text-center text-2xl font-bold">{scrapObject.stats ? scrapObject.stats.health : "?"}</div>
            </div>
            <div className="text-md bg-blue-500 p-2 rounded-full">
                <div className="text-center text-lg">Defence</div>
                <div className="text-center text-2xl font-bold">{scrapObject.stats ? scrapObject.stats.defence : "?"}</div>
            </div>
            </div>

            {(scrapObject.types && scrapObject.types.length === 1) && (
                <div className="flex">
                <span className="text-xl text-black px-2">Class:</span>
                <div
                    className="mt-1 text-center rounded-full px-2 text-black w-16 border-black border"
                    style={{ backgroundColor: scrapObject.types[0].colour }}
                >
                    {scrapObject.types[0].name}
                </div>
                </div>
            )}
            {(scrapObject.types && scrapObject.types.length === 2) && (
                <div className="flex">
                <span className="text-xl text-black px-2">Classes:</span>
                <div className="flex text-center gap-1 pt-1">
                    <div
                        className="rounded-full px-2 text-black w-16 border-black border"
                        style={{ backgroundColor: scrapObject.types[0].colour }}
                    >
                        {scrapObject.types[0].name}
                    </div>
                    <div
                        className="rounded-full px-2 text-black w-16 border-black border"
                        style={{ backgroundColor: scrapObject.types[1].colour }}
                    >
                        {scrapObject.types[1].name}
                    </div>
                </div>
                </div>
            )}
            <ShareButton url="google.com" text={"Look at my scrap "+scrapObject.nickname} title={"Look at my scrap "+scrapObject.nickname}/>
            <div className="relative aspect-square">
                <div className="absolute translate-y-[70%]">
                    <div className="w-full overflow-hidden brightness-125 aspect-square">
                        <Image
                            src="/shadow.gif"
                            width={512}
                            height={512}
                            className="scale-150 opacity-65"
                            alt=""
                        />
                        <div className="bg-slate-200">

                        </div>
                    </div>
                </div>
                <div className="absolute flex justify-center mt-4 w-full -translate-y-[10%]">

                    <Canvas width={512} height={512} conf={draw_conf} />
                </div>
            </div>
            <div className="text-blue-600 mt-10 mx-4">{scrapObject.description}</div>

        </div>
    );
}
