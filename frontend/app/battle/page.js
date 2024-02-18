"use client"

import BattleScrap from "../components/BattleScraps"

export default function BattlePage() {
    return (
        <div className="min-h-screen flex flex-col p-4">
            <div className="flex flex-row gap-2">
                <div className="w-3/5">
                    <BattleScrap
                        scrapID="fc8c8e5d-cf7e-4cdd-8dd6-a88375cdf6be"
                    />
                </div>
                <div className="w-2/5">
                    <BattleScrap
                        scrapID="fc8c8e5d-cf7e-4cdd-8dd6-a88375cdf6be"
                    />
                </div>
            </div>
            <div className="h-16"></div>
            <div className="grid columns-1">
                <button className="rounded-lg border-black bg-orange-600 hover:bg-orange-800 cursor-pointer p-4 text-white text-2xl">Action 1</button>
            </div>
        </div>
    );
}
