"use client"

import { useEffect, useState } from "react";

export function useGetCookie(cookieName) {
    const [cookies, setCookies] = useState("");

    // Only load cookie if on the client
    useEffect(() => {
        setCookies(document.cookie.split(';'));
    }, [])

    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();

        if (cookie.startsWith(`${cookieName}=`)) {
            let value = cookie.substring(cookieName.length + 1);

            // Remove extra double quotes from the start and end, if present
            if (value.startsWith('"') && value.endsWith('"')) {
                value = value.slice(1, -1);
            }

            return value;
        }
    }

    // Return null if the cookie is not found or if not on the client side
    return null;
}