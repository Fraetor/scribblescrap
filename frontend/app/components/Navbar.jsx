import Image from 'next/image'
import Link from 'next/link'
import Login from './Login'

export default function Navbar({ children }) {
    return (
        <div className="w-full h-fit py-4 h-16 bg-green-700 flex justify-between content-center">
            <Link href="/">
                <span
                    className="text-4xl flex font-bold italic ml-4 self-center text-yellow-500"
                >
                    <span>
                        <Image
                            src="/orange.png"
                            width={64}
                            height={64}
                            className="h-fit"
                            alt=""
                        />
                    </span>
                <span className="self-center">
                    <div>Scribble</div>
                    <div>Scrap</div>
                </span>



                </span>
            </Link>
            <span className="text-white self-center mr-6">
                <Login/>
            </span>
        </div>
    )
}