

import Image from 'next/image'
import Link from 'next/link'
import { useState, useEffect } from 'react';
import ViewScrap from './ViewScrap';

export default function ScrapPage({ children }) {
    const [scraps, setScraps] = useState([])
    useEffect(() => {
        console.log("Getting Scraps")
        fetch(`/api/scribbles/`, {
            method: 'GET',
        })
            .then(response => response.json())
            .then(data => {setScraps(data)})
            .catch(error => {
                // Handle error
                console.error('Error:', error);
            });
        console.log("Got Scraps")
    }, []);

    return (
        <div>
            {[...scraps].reverse().map(scrap => {
                return (
                    <div className="border-b-4 border-blue-800 pb-4">
                        <ViewScrap scrapID={scrap}/>
                    </div>
                )
            })}
        </div>
    )
}