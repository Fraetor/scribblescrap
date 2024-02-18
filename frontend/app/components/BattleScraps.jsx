import Image from "next/image";
import HeathBar from "./healthBar";
import Canvas from "./Canvas";
import { useState, useEffect } from "react";


export default function BattleScrap({ scrapID }) {

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
        return <div></div>
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
        <div className="w-full">
            <div className="text-red-800 text-2xl translate-y-2">{scrapObject.nickname}:</div>
            <div className="text-yellow-800 text-xl">{scrapObject.name}</div>
            <HeathBar currentHealth={scrapObject.health.current} maxHealth={scrapObject.health.max} />
            {(scrapObject.types.length === 1) && (
                <div
                    className="mt-1 rounded-full px-2 text-black border-black border"
                    style={{ backgroundColor: scrapObject.types[0].colour }}
                >
                    {scrapObject.types[0].name}
                </div>
            )}
            {(scrapObject.types.length === 2) && (
                <div className="flex text-center gap-1 pt-1">
                    <div
                        className="rounded-full px-2 text-black border-black border"
                        style={{ backgroundColor: scrapObject.types[0].colour }}
                    >
                        {scrapObject.types[0].name}
                    </div>
                    <div
                        className="rounded-full px-2 text-black border-black border"
                        style={{ backgroundColor: scrapObject.types[1].colour }}
                    >
                        {scrapObject.types[1].name}
                    </div>
                </div>
            )}
            <div className="relative aspect-square">
                <div className="absolute translate-y-[100%]">
                    <div className="w-full overflow-hidden brightness-125">
                        <Image
                            src="/shadow.gif"
                            width={512}
                            height={512}
                            className="scale-150 opacity-45"
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
        </div>
    );
}
