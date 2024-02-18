"use client"

import { useRef, useState } from "react";
import ViewScrap from "../components/ViewScrap";
import { useEffect } from "react";
import { useSearchParams } from 'next/navigation'


export default function ScribbleLooker() {
    const searchParams = useSearchParams()
    const scrapID = searchParams.get('id')

    return (
        <main className="flex min-h-screen flex-col items-center pt-0 p-12">
            <ViewScrap scrapID={scrapID} />
        </main>
    );
}
