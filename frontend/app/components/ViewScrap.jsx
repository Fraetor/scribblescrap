import Image from "next/image";
import HeathBar from "./healthBar";
import Canvas from "./Canvas";


export default function ViewScrap({ scrap }) {

    const scrapObject = scrap;

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
            <div className="text-yellow-500 text-center text-4xl mb-1">You've found a {scrapObject.name}!</div>
            <div className="grid grid-cols-4 gap-2" >
            <div className="grid grid-cols-2 text-md bg-red-800 p-2 rounded-full">
                <div className="text-right">might:</div>
                <div className="text-center">{scrapObject.stats.might}</div>
            </div>
            <div className="grid grid-cols-2 text-md bg-yellow-500 p-2 rounded-full">
                <div className="text-right">speed:</div>
                <div className="text-center">{scrapObject.stats.speed}</div>
            </div>
            <div className="grid grid-cols-2 text-md bg-pink-600 p-2 rounded-full">
                <div className="text-right">health:</div>
                <div className="text-center">{scrapObject.stats.health}</div>
            </div>
            <div className="grid grid-cols-2 text-md bg-blue-500 p-2 rounded-full">
                <div className="text-right">defence:</div>
                <div className="text-center">{scrapObject.stats.defence}</div>
            </div>
            </div>

            {(scrap.types.length === 1) && (
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
            {(scrap.types.length === 2) && (
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
            <div className="relative">
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

        </div>
    );
}
