import Image from "next/image";
import HeathBar from "./healthBar";
import Canvas from "./Canvas";


export default function BattleScrap({ scrap }) {

    const scrapObject = scrap;

    const draw_conf = {
        "scrap_img_url": scrapObject.image,
        "arm_img_url": "arm.png",
        "eye_img_url": "eye.png",
        "leg_img_url": "leg.png",
        "sway_dist": 0.05,
        "sway_speed": 4,
        "arm_sway_dist": 0.1,
        "arm_sway_speed": 10,
        "leg_sway_dist": 0.1,
        "leg_sway_speed": 7,
        "arms": [
            {
                "rx": 10,
                "ry": 10,
                "ox": 154,
                "oy": -15,
                "rot": -0.1
            },
            {
                "rx": 10,
                "ry": 10,
                "ox": -154,
                "oy": -15,
                "rot": Math.PI + 0.1
            },
        ],
        "legs": [
            {
                "rx": 10,
                "ry": 30,
                "ox": 70,
                "oy": 130,
                "rot": Math.PI / 2 - 0.1
            },
            {
                "rx": 10,
                "ry": 30,
                "ox": -70,
                "oy": 120,
                "rot": Math.PI / 2 + 0.1
            },
        ],
        "eyes": [
            {
                "x": -60,
                "y": -45
            },
            {
                "x": 60,
                "y": -55
            }
        ]
    }

    return (
        <div className="w-full">
            <div className="text-yellow-500 text-lg">{scrapObject.name}:</div>
            <HeathBar currentHealth={scrapObject.currentHealth} maxHealth={scrapObject.maxHealth} />
            {(scrap.types.length === 1) && (
                <div
                    className="mt-1 rounded-full px-2 text-black w-16 border-black border"
                    style={{ backgroundColor: scrapObject.types[0].colour }}
                >
                    {scrapObject.types[0].name}
                </div>
            )}
            {(scrap.types.length === 2) && (
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