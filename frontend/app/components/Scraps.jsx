import Image from "next/image";
import HeathBar from "./healthBar";

export default function Scrap ({ scrap }) {

    const scrapObject = scrap;

    const openModal = () => {
      setIsOpen(true);
    };

    return (
      <div className="w-full">
        <div className="text-yellow-500 text-lg">{scrapObject.name}:</div>
        <HeathBar currentHealth={scrapObject.currentHealth} maxHealth={scrapObject.maxHealth}/>
        {(scrap.types.length === 1) && (
            <div
                className="rounded-full px-2 text-black w-16 border-black border"
                style={{backgroundColor: scrapObject.types[0].colour }}
            >
                {scrapObject.types[0].name}
            </div>
        )}
        {(scrap.types.length === 2) && (
            <div className="flex text-center gap-1 pt-1">
                <div
                    className="rounded-full px-2 text-black w-16 border-black border"
                    style={{backgroundColor: scrapObject.types[0].colour }}
                >
                    {scrapObject.types[0].name}
                </div>
                <div
                    className="rounded-full px-2 text-black w-16 border-black border"
                    style={{backgroundColor: scrapObject.types[1].colour }}
                >
                    {scrapObject.types[1].name}
                </div>
            </div> 
        )}
        <div className="flex justify-center mt-4 w-full">
            <Image
                src={scrapObject.image}
                width={512}
                height={512}
                className="z-10 drop-shadow-2xl"
                alt=""
            />
        </div>
        <div className="scale-y-50 -translate-y-1/2">
            <div className="w-full rounded-full overflow-hidden brightness-125 aspect-square">
                <Image
                    src="/dirt.jpg"
                    width={512}
                    height={512}
                    className="z-10"
                    alt=""
                />
                <div className="bg-slate-200">

                </div>
            </div>    
        </div>
      </div>
    );
}