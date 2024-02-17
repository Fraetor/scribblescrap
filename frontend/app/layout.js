import { Inter } from 'next/font/google'
import Navbar from './components/Navbar'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

//👇 Import Open Sans font
import { Patrick_Hand } from 'next/font/google'

//👇 Configure our font object
const openSans = Patrick_Hand({
  subsets: ['latin'],
  display: 'swap',
  weight: '400'
})

export const metadata = {
  title: 'Scribble Scrap',
  description: 'Scribble Scrap',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={openSans.className}>
        <div className="bg-yellow-100 h-full">
          <Navbar/>
          <div className="flex justify-center">
            <div className="max-w-screen-lg w-full">
              {children}
            </div>
          </div>
        </div>
      </body>
    </html>
  )
}