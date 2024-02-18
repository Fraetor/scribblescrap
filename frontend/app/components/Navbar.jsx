import Image from 'next/image'
import Link from 'next/link'
import Login from './Login'

export default function Navbar({ children }) {
    return (
        <div className="w-full h-fit py-4 h-16 bg-green-700 flex justify-between content-center">
            <Link href="/">
                    <div
                        className="text-4xl flex font-bold italic ml-4 self-center items-center gap-4 text-yellow-500"
                    >

                        <Image
                            src="/orange.png"
                            width={64}
                            height={64}
                            className="h-fit"
                            alt=""
                        />
                        <div className="self-center">
                            <div>Scribble</div>
                            <div>Scrap</div>
                        </div>




                    </div>
            </Link>
            <span className="text-white self-center mr-6">
                <Login />
            </span>
        </div>
    )
}
